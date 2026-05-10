#!/usr/bin/env python3
"""
Phase 3c — n8n cleanup (GREEN-tier per §3.0 rails).

Actions in this script:
  1. Rename `cachedResultName` and node display name "team-tasks" →
     "team-operations" in the 2 active workflows that still have stale UI
     labels (Slack Ops Supervisor, Onboarding Health Monitor). Channel ID
     C0AKWU4835E was always correct — purely cosmetic.
  2. Fix UTF-8 mojibake in workflow names (display chars like `â` that
     should be `→` or `—`). Affects ~7 workflow names.
  3. Lifecycle tags applied to every workflow:
       - "active"          → live, in-cycle workflows (21)
       - "campaign-gated"  → inactive but auto-reactivates on first live
                             campaign (CIA, Decision Router, Windsor)
       - "deprecated"      → superseded by a newer workflow; keep for soak
                             before delete
       - "demo"            → demo / enterprise pitch artifacts
       - "archive-candidate" → 7-day soak then propose delete

Sequence per memory rule: deactivate → edit → save → reactivate (only for
active workflows that need an edit). Tags can be applied without a
deactivation since they don't change runtime behavior.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

N8N_KEY = os.environ["N8N_KEY"]
BASE = "https://requityai.app.n8n.cloud/api/v1"

# Active workflows that need cachedResultName / node-display rename
TEAM_TASKS_RENAME_TARGETS = {
    "5cdMtOByeZVRFS6H": "Slack Ops Supervisor",
    "CqesBe55FnP6oaxA": "Onboarding Health Monitor",
}

# UTF-8 mojibake in workflow names — `â` is mis-decoded `→` or `—`
NAME_RENAMES = {
    "DH5Yx9S2RS6OO6qG": "Task Completed → Auto-Set Completed Date",
    "I599mjvYW4ZdkNRf": "Won Deal → Auto-Create Onboarding Task Chain",
    "KEcx3yQ7kephk0cM": "Daily Data Hygiene Check → Stale Records Alert",
    "QGtGJydvWkR6vSCj": "Client Communication → Onboarding Updates + Campaign Milestones",
    "XGVbY2c8ijPoz54w": "Recurring Maintenance Tasks — Event-Driven (replaces Weekly Skeleton Tasks)",
    "apbdh284pFlCy2hZ": "QA Ready → Create QA Task for Andrew",
    "qYFXgdFG6N9StUkO": "Campaign Review Task Auto-Creator — Every 7 Days from Launch",
    "rtjwykL2X3VwKZxM": "Client Report Auto-Generator — 7-Day Cycle from Launch",
    "Prerequisites Met â Auto-Create Campaign Build Task": None,  # marker - this is uDdwyIl7VDFEWJ8N (active), already handled separately
    "uDdwyIl7VDFEWJ8N": "Prerequisites Met → Auto-Create Campaign Build Task",
    "PJaJYLuesPU2oxc7": "RequityAI Enterprise Demo — Maintenance + Leasing + Slack",
}

# Lifecycle tags (semantic groups)
LIFECYCLE_GROUPS = {
    "active": [
        "15VLgXsxSNGbJIdp", "1LMmEYIxSQHsPZd1", "1g5RRCFJKwWSl5ru",
        "5cdMtOByeZVRFS6H", "8tdPtQWO4qDKEjgq", "A31jYsKR3aETSusC",
        "BegEckXSgXmVffX2", "CqesBe55FnP6oaxA", "D4AvztGc4RCYyE5g",
        "IHEmXUHvz1T034lF", "NFU4jyVpaRSKv4Mj", "Zv2PYFdMiBDCLcZV",
        "ePyAmNK7lpzoXPgo", "ey0cuADK27ntvgMe", "fdUdIRGsBq0HB4jA",
        "lUl2nkA0Bo1k8nbv", "o6A12htwZffpOkbu", "pa7I1FKd50TQRFrV",
        "ra2F0R9zrKMmGEvE", "uDdwyIl7VDFEWJ8N", "ynGKEAco9U6Q0ShI",
    ],
    "campaign-gated": [
        "6TuDo3mqBZSBF667",  # Campaign Intelligence Agent
        "iM5CNWHLS2UIIJ34",  # Decision Router
        "ZwXd0unFysJjWl1M",  # Windsor AI → SmartSuite Metrics
        "OmtNWq7oETDUAjni",  # Creative Fatigue Alert (28-Day Check)
        "VTiPgz0Zem8jiOYx",  # 72hr Review Trigger
        "bhu2yom6iUt1SfSa",  # 72hr Optimization Review Creator
        "gRzeR9zO9xbHMvXG",  # CPL Threshold Alert → DM Andrew
        "TX7laFirjpUrxDoa",  # Optimization Decision → Notify #operations
        "qYFXgdFG6N9StUkO",  # Campaign Review Task Auto-Creator
        "rtjwykL2X3VwKZxM",  # Client Report Auto-Generator
        "whNlFn46NRMswO6D",  # Campaign Goes Live → Set Next Action Date
        "YK0z988p7cqxFqKX",  # Campaign Goes Live - Set Next Review Date
        "9jGs4HGdijkyYB4f",  # Campaign Launch → Notify Client in Slack
    ],
    "deprecated": [
        "dInuMwYxjwcftjSp",  # M2 webhook → replaced by M2b polling Apr 22
        "R4mXec6XM032MMyB",  # Close → SS Pipeline Sync — Close Pipeline retired Apr 19
        "Gly17Kkp8oUTEyGp",  # Close CRM → SS ConvTracker (old) — superseded by M2b
        "HZ18Xb98Szin8OTQ",  # Deal Won → Create Client + Onboarding (Manual) — superseded by M5
        "9pAsoQqBhRT4HHS6",  # Client Onboarding — Create Slack Channels — superseded by M5
        "Ikil2vx4jQNR7yxa",  # M4 — SS No-Show → Calendly Bridge — DUPLICATE of active 1g5RRCFJKwWSl5ru
        "PpfpYaSQRcGrJqLe",  # Weekly Skeleton Tasks — replaced by event-driven XGVbY2c8ijPoz54w
        "7gKYzCvV0zibOWq9",  # Task Blocked - DM Andrew v2 — superseded by ra2F0R9zrKMmGEvE
        "QX0VicX53AzQmHPY",  # M1_ClientOnboarding_Orchestrator — old M1
        "W2GRDMN8xwlQhlqg",  # Client Onboarding — Slack Trigger — superseded
        "SDIWZGNRgXFwg81W",  # Task Notifications v2 — superseded by D4AvztGc4RCYyE5g
        "DH5Yx9S2RS6OO6qG",  # Task Completed - Auto-Set Completed Date — superseded
        "I599mjvYW4ZdkNRf",  # Won Deal - Auto-Create Onboarding Task Chain — superseded by M5
        "KEcx3yQ7kephk0cM",  # Daily Data Hygiene Check — duplicates lUl2nkA0Bo1k8nbv (active "Stale Record Detector")
    ],
    "demo": [
        "PJaJYLuesPU2oxc7",  # Enterprise Demo
    ],
    "experimental": [
        "9fPbvP6pytQslBD1",  # Telnyx Listener Webhook
        "GQwRPVA9iaiZwCQ5",  # AI Maintenance Agent
        "G0ITjfkhRZqKIWX4",  # Windsor Metrics Sync v2 - Daily — duplicate of ZwXd0unFysJjWl1M
        "QGtGJydvWkR6vSCj",  # Client Communication — Onboarding Updates + Campaign Milestones
        "apbdh284pFlCy2hZ",  # QA Ready - Create QA Task for Andrew — possibly superseded by IHEmXUHvz1T034lF
    ],
}

SETTINGS_ALLOWED = {
    "executionOrder", "errorWorkflow", "timezone",
    "saveDataErrorExecution", "saveDataSuccessExecution",
    "saveExecutionProgress", "saveManualExecutions",
}


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


def safe_put(wf, deactivate_first):
    """PUT a workflow with strict-allowlist settings + standard sequence."""
    wid = wf["id"]
    was_active = wf.get("active") and deactivate_first
    if was_active:
        http("POST", f"/workflows/{wid}/deactivate")
        time.sleep(0.3)
    raw_settings = wf.get("settings", {}) or {}
    safe_settings = {k: v for k, v in raw_settings.items() if k in SETTINGS_ALLOWED}
    body = {
        "name": wf["name"],
        "nodes": wf["nodes"],
        "connections": wf["connections"],
        "settings": safe_settings,
    }
    if "staticData" in wf and wf["staticData"] is not None:
        body["staticData"] = wf["staticData"]
    code, resp = http("PUT", f"/workflows/{wid}", body)
    if was_active:
        time.sleep(0.3)
        http("POST", f"/workflows/{wid}/activate")
    return code, resp


def ensure_tag(name):
    """Return the tag id for `name`, creating it if absent."""
    code, resp = http("GET", "/tags?limit=250")
    if code != 200:
        return None
    for t in resp.get("data", []):
        if t["name"] == name:
            return t["id"]
    code, resp = http("POST", "/tags", {"name": name})
    return resp.get("id") if isinstance(resp, dict) else None


def main():
    log = []

    # 1. Cosmetic team-tasks → team-operations rename in 2 active workflows
    for wid, expected_name in TEAM_TASKS_RENAME_TARGETS.items():
        code, wf = http("GET", f"/workflows/{wid}")
        if code != 200:
            log.append(f"  ! {wid}: GET failed {code}"); continue
        changed = False
        for n in wf["nodes"]:
            params = n.get("parameters", {}) or {}
            ch = (params.get("channelId") or {})
            if isinstance(ch, dict) and ch.get("cachedResultName") == "team-tasks":
                ch["cachedResultName"] = "team-operations"
                changed = True
            if "team-tasks" in (n.get("name") or ""):
                n["name"] = n["name"].replace("team-tasks", "team-operations")
                changed = True
        # Fix downstream connections that reference the renamed node
        new_conns = json.dumps(wf["connections"]).replace("Post to #team-tasks", "Post to #team-operations")
        wf["connections"] = json.loads(new_conns)
        if changed:
            c, _ = safe_put(wf, deactivate_first=True)
            log.append(f"  • {wid} ({wf['name']}): cosmetic team-tasks→team-operations rename → {c}")
        else:
            log.append(f"  - {wid}: nothing to rename")

    # 2. UTF-8 mojibake fix in workflow names
    for wid, new_name in NAME_RENAMES.items():
        if new_name is None or len(wid) < 10:
            continue
        code, wf = http("GET", f"/workflows/{wid}")
        if code != 200:
            log.append(f"  ! {wid}: GET failed {code}"); continue
        if wf["name"] == new_name:
            continue
        old = wf["name"]
        wf["name"] = new_name
        c, _ = safe_put(wf, deactivate_first=wf.get("active"))
        log.append(f"  • {wid}: rename {old!r} → {new_name!r} → {c}")

    # 3. Lifecycle tags
    tag_ids = {}
    for tag_name in LIFECYCLE_GROUPS:
        tid = ensure_tag(tag_name)
        if tid:
            tag_ids[tag_name] = tid
            log.append(f"  · tag '{tag_name}' → id {tid}")

    for tag_name, wf_ids in LIFECYCLE_GROUPS.items():
        tid = tag_ids.get(tag_name)
        if not tid:
            continue
        for wid in wf_ids:
            # PUT /workflows/{id}/tags expects [{id: tagId}, ...]; we add this tag.
            code, resp = http("GET", f"/workflows/{wid}/tags")
            if code != 200:
                log.append(f"  ! {wid}: GET tags failed {code}")
                continue
            existing = resp if isinstance(resp, list) else (resp.get("data", []) if isinstance(resp, dict) else [])
            existing_ids = {t.get("id") for t in existing}
            if tid in existing_ids:
                continue
            new_tags = [{"id": t.get("id")} for t in existing] + [{"id": tid}]
            code, _ = http("PUT", f"/workflows/{wid}/tags", new_tags)
            log.append(f"    · {wid}: add tag '{tag_name}' → {code}")

    print("\n".join(log))


if __name__ == "__main__":
    main()
