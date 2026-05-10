#!/usr/bin/env python3
"""
M22 — Tasks `type` dropdown patch.

Live state (probed 2026-05-10):
- 6 labels collide on value='2' (schema-corrupt singleselect)
- "Create Retargeting Audiences" still in dropdown despite May 5 retirement
- 0 Task records → no migration impact

Target: canonical 13-task list per doc_reconciliation §5
- Preserve existing unique values where the label survives unchanged
- Repurpose `iQMVn` (was "Build Campaign (CSV Import)") to "Build Campaign"
- Drop n6EvX (Manual collapsed), pjZqe (Campaign Review out), LaFdW (Retargeting retired), all value='2' duplicates collapsed to fresh unique values

Approach: GET application → modify `type` field's `params.choices` →
POST /change_field/ with full updated field config (SS structure-mod endpoint).
"""
import json
import os
import sys
import urllib.request
import urllib.error

SS_TOKEN = os.environ["SS_TOKEN"]
SS_WS = os.environ["SS_WS"]
TASKS_APP_ID = "69ce67b3fec5b91842ebaf03"
BASE = "https://app.smartsuite.com/api/v1"

CANONICAL = [
    # (label, value, color)  preserve existing values where possible
    ("Set Up Ad Account Access",     "ad_account_access", "#883CD0"),
    ("Set Up Lead Forms",            "lead_forms",        "#883CD0"),
    ("Send Video Brief",             "video_brief",       "#883CD0"),
    ("Upload Creative",              "upload_creative",   "#883CD0"),
    ("Write Script",                 "write_script",      "#883CD0"),
    ("Build Campaign",               "iQMVn",             "#883CD0"),
    ("QA Campaign",                  "WvoJS",             "#17C4C4"),
    ("Launch Campaign",              "3LeIB",             "#13C2C2"),
    ("Cut / Pause Campaign",         "Kr9Qn",             "#EC506E"),
    ("Swap Creative",                "swap_creative",     "#EC506E"),
    ("Adjust Targeting",             "adjust_targeting",  "#EC506E"),
    ("Update SmartSuite Records",    "gPtcw",             "#0C41F3"),
    ("Escalation Follow-Up",         "M2IdT",             "#FFA940"),
]


def http(method, path, body=None):
    headers = {
        "Authorization": f"Token {SS_TOKEN}",
        "ACCOUNT-ID": SS_WS,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return r.status, json.loads(txt) if txt else None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def main():
    # 1. Pull current structure
    code, app = http("GET", f"/applications/{TASKS_APP_ID}/")
    if code != 200:
        print(f"GET app failed: {code}\n{app}")
        sys.exit(1)
    type_field = next((f for f in app["structure"] if f["slug"] == "type"), None)
    if not type_field:
        print("type field not found")
        sys.exit(1)

    # 2. Verify pre-state matches what we expect (corruption present)
    pre_choices = type_field["params"]["choices"]
    pre_values = [c["value"] for c in pre_choices]
    dup_two = pre_values.count("2")
    has_retargeting = any(c["label"] == "Create Retargeting Audiences" for c in pre_choices)
    print(f"Pre-state: {len(pre_choices)} choices, {dup_two} share value='2', "
          f"Create Retargeting Audiences present={has_retargeting}")
    if dup_two != 6 or not has_retargeting:
        print("Pre-state doesn't match expected corruption — aborting")
        sys.exit(2)

    # 3. Build new choices array
    new_choices = []
    for i, (label, value, color) in enumerate(CANONICAL):
        new_choices.append({
            "label": label,
            "value": value,
            "value_color": color,
            "value_help_text": "",
            "value_order": i,
            "value_icon": None,
            "icon_type": "icon",
            "records": None,
            "default_color": color,
            "weight": 1,
        })

    # 4. Build new field definition (preserve all top-level keys)
    new_field = json.loads(json.dumps(type_field))  # deep copy
    new_field["params"]["choices"] = new_choices

    # 5. PUT to change_field endpoint — try multiple payload shapes
    candidates = [
        ("flat-field", new_field),
        ("wrapped-field", {"field": new_field}),
        ("slug+field",  {"slug": "type", "field": new_field}),
        ("slug+params", {"slug": "type", "params": new_field["params"]}),
    ]
    success = False
    for name, payload in candidates:
        print(f"\n--- Trying PUT /change_field/ with payload shape '{name}' ---")
        code, resp = http("PUT", f"/applications/{TASKS_APP_ID}/change_field/", payload)
        print(f"Response: {code}")
        if isinstance(resp, dict):
            print(json.dumps(resp, indent=2)[:1200])
        else:
            print(str(resp)[:1200])
        if code in (200, 201, 204):
            success = True
            break
    if not success:
        print("\nAll PUT shapes failed. Will need to surface for UI work.")
        sys.exit(3)

    # 6. Re-probe to verify
    code2, app2 = http("GET", f"/applications/{TASKS_APP_ID}/")
    type2 = next((f for f in app2["structure"] if f["slug"] == "type"), None)
    post_choices = type2["params"]["choices"]
    print(f"\nPost-state: {len(post_choices)} choices")
    for c in post_choices:
        print(f"  value={c['value']!r:25} label={c['label']!r}")


if __name__ == "__main__":
    main()
