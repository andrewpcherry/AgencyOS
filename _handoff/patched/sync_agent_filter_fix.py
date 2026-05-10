#!/usr/bin/env python3
"""
Sync Agent — fix `sf.filter.filters.push` typo to `sf.filter.fields.push`.

Workflow: 8tdPtQWO4qDKEjgq (SmartSuite Sync Agent — Slack /update Parser)
Node: SmartSuite Lookup & Update (Code node)

Bug: code uses `sf.filter.filters.push(...)` in two places (tasks + campaigns
secondary filter). The actual filter array property is `fields` per the
SmartSuite list-filter API spec. Throws `Cannot read properties of undefined
(reading 'push')` the first time /update Tasks task:X or /update Campaigns
campaign:X arrives. Latent because there are 0 task records and 1 test
campaign record — never been triggered in production.

Sequence per memory rule (zombies hide in staticData):
  deactivate → edit → save (PUT) → activate
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

N8N_KEY = os.environ["N8N_KEY"]
BASE = "https://requityai.app.n8n.cloud/api/v1"
WF_ID = "8tdPtQWO4qDKEjgq"


def http(method, path, body=None):
    headers = {"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return r.status, json.loads(txt) if txt else None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def main():
    # 1. GET current workflow
    code, wf = http("GET", f"/workflows/{WF_ID}")
    if code != 200:
        print(f"GET failed: {code}\n{wf}")
        sys.exit(1)
    print(f"Workflow: {wf['name']} | active={wf.get('active')}")

    # 2. Find the Code node and apply fix
    target_node = None
    for n in wf["nodes"]:
        if n["name"] == "SmartSuite Lookup & Update":
            target_node = n
            break
    if not target_node:
        print("Target node not found")
        sys.exit(2)

    code_str = target_node["parameters"]["jsCode"]
    bug_count = code_str.count("sf.filter.filters")
    print(f"Bug occurrences (sf.filter.filters): {bug_count}")
    if bug_count == 0:
        print("Already fixed — nothing to do")
        sys.exit(0)
    new_code = code_str.replace("sf.filter.filters.push", "sf.filter.fields.push")
    target_node["parameters"]["jsCode"] = new_code
    print(f"After fix, occurrences: {new_code.count('sf.filter.filters')}")
    print(f"New 'sf.filter.fields.push' count: {new_code.count('sf.filter.fields.push')}")

    # 3. Save backup of pre-state
    with open(f"_handoff/audit/raw/n8n_{WF_ID}_pre_filter_fix.json", "w") as f:
        json.dump(wf, f, indent=2)
    print(f"Backup saved → _handoff/audit/raw/n8n_{WF_ID}_pre_filter_fix.json")

    # 4. Deactivate (memory rule: zombies hide in staticData)
    print("\nDeactivating...")
    code, _ = http("POST", f"/workflows/{WF_ID}/deactivate")
    print(f"  → {code}")

    # 5. PUT updated workflow.
    # n8n public API rejects unexpected fields. settings only accepts a strict
    # subset (executionOrder, errorWorkflow, timezone, saveData*). Strip Cloud-
    # only keys (binaryMode, callerPolicy, availableInMCP).
    raw_settings = wf.get("settings", {}) or {}
    SETTINGS_ALLOWED = {
        "executionOrder", "errorWorkflow", "timezone",
        "saveDataErrorExecution", "saveDataSuccessExecution",
        "saveExecutionProgress", "saveManualExecutions",
    }
    safe_settings = {k: v for k, v in raw_settings.items() if k in SETTINGS_ALLOWED}
    put_body = {
        "name": wf["name"],
        "nodes": wf["nodes"],
        "connections": wf["connections"],
        "settings": safe_settings,
    }
    if "staticData" in wf and wf["staticData"] is not None:
        put_body["staticData"] = wf["staticData"]
    code, resp = http("PUT", f"/workflows/{WF_ID}", put_body)
    print(f"PUT: {code}")
    if code not in (200, 201):
        print(resp)
        # Try to reactivate anyway so we don't leave it deactivated on failure
        http("POST", f"/workflows/{WF_ID}/activate")
        sys.exit(3)

    # 6. Reactivate
    time.sleep(1)
    print("Activating...")
    code, _ = http("POST", f"/workflows/{WF_ID}/activate")
    print(f"  → {code}")

    # 7. Verify
    code, wf2 = http("GET", f"/workflows/{WF_ID}")
    final_code = next(n for n in wf2["nodes"] if n["name"] == "SmartSuite Lookup & Update")["parameters"]["jsCode"]
    print(f"\nFinal verification:")
    print(f"  active={wf2.get('active')}")
    print(f"  sf.filter.filters count={final_code.count('sf.filter.filters')} (target: 0)")
    print(f"  sf.filter.fields.push count={final_code.count('sf.filter.fields.push')} (target: 2)")


if __name__ == "__main__":
    main()
