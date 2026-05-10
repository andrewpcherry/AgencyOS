#!/usr/bin/env python3
"""
Phase 4 — functional verification of every active workflow.

Method: pull execution history (last 25 + most recent with full data) for each
active workflow. Determine GREEN / YELLOW / RED:

- GREEN: cadence-appropriate recent fires, all status=success, no node errors
- YELLOW: works but has caveats — graceful failure modes, latent bugs, etc.
- RED: status=error in recent runs, or hasn't fired when it should have

For event-driven workflows with no recent fires (e.g., M5 hasn't seen a Won
deal recently), GREEN if last execution succeeded; YELLOW if no executions
ever (untested in production).
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

N8N_KEY = os.environ["N8N_KEY"]
BASE = "https://requityai.app.n8n.cloud/api/v1"
NOW = datetime.now(timezone.utc)

# Active workflow inventory with expected cadence + verification notes
ACTIVE = [
    # (id, name, cadence, expected_window_hours, verification_notes)
    ("15VLgXsxSNGbJIdp", "M2b — Close Polling → ConvTracker",            "30min M-F 8am-3:30p ET", 4,    "polls Close API; depends on day/time"),
    ("1LMmEYIxSQHsPZd1", "M3 — Calendly invitee.created → Pipeline",      "event (Calendly webhook)", None, "fires only on real bookings"),
    ("1g5RRCFJKwWSl5ru", "M4 — SS No-Show → Calendly Bridge",             "event (deal_stage flip)",   None, "fires only on real no-shows"),
    ("5cdMtOByeZVRFS6H", "Slack Ops Supervisor",                          "12h cron (8am+8pm ET)",     16,   "monitors Slack ops health"),
    ("8tdPtQWO4qDKEjgq", "SmartSuite Sync Agent — Slack /update Parser",  "event (Slack /update)",     None, "filter.fields typo fixed 2026-05-10"),
    ("A31jYsKR3aETSusC", "M5 — Deal Won → Full Client Setup",             "event (Won) + 5min poller", None, "atomic onboarding chain"),
    ("BegEckXSgXmVffX2", "Drive Folder Creator",                          "daily 8am ET",              30,   "creates Drive folders for new clients"),
    ("CqesBe55FnP6oaxA", "Onboarding Health Monitor",                     "daily 8:30am ET",           30,   "DM Andrew on >5 day blockers"),
    ("D4AvztGc4RCYyE5g", "Task Assigned → Slack",                         "event (SS Task created)",   None, "DMs assignee on task creation"),
    ("IHEmXUHvz1T034lF", "Campaign QA Ready → Slack Checklist",           "event (campaign QA Ready)", None, "fires only when first campaign hits QA Ready"),
    ("NFU4jyVpaRSKv4Mj", "Onboarding Progression",                        "daily 8am ET",              30,   "advances onboarding_stage based on step_* fields"),
    ("Zv2PYFdMiBDCLcZV", "SmartSuite → Form Submitted Watcher",           "daily",                     30,   "fixed Apr 25"),
    ("ePyAmNK7lpzoXPgo", "Global Error Handler → DM Andrew",              "errorTrigger",              None, "wired to all other workflows"),
    ("ey0cuADK27ntvgMe", "Daily Ops Briefing",                            "daily 8am ET",              30,   "snapshot to #team-operations"),
    ("fdUdIRGsBq0HB4jA", "Client Nudge — Form & Video Reminders",         "daily",                     30,   "reminders on overdue forms/videos"),
    ("lUl2nkA0Bo1k8nbv", "Stale Record Detector",                         "daily",                     30,   "flags pipeline/client stalls"),
    ("o6A12htwZffpOkbu", "SmartSuite → Video Watcher",                    "daily",                     30,   "Drive triggers on new video"),
    ("pa7I1FKd50TQRFrV", "Daily Sales Metrics Brief",                     "8:05am ET M-F",             30,   "Calls/Booked/C→B ratios"),
    ("ra2F0R9zrKMmGEvE", "Task Blocked → DM Andrew",                      "event (SS Task → Blocked)", None, "DMs Andrew on blockers"),
    ("uDdwyIl7VDFEWJ8N", "Prerequisites Met → Auto-Create Campaign Build Task", "daily 8am ET",       30,   "M10 fix landed 2026-05-10"),
    ("ynGKEAco9U6Q0ShI", "Slack Task Router — /done [action]",            "event (Slack /done)",       None, "marks task complete"),
]


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


def parse_iso(s):
    if not s: return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def verify_workflow(wid, name, cadence, window, notes):
    code, resp = http("GET", f"/executions?workflowId={wid}&limit=25")
    if code != 200:
        return ("RED", f"executions API failed: {code}", None, None, None)
    exes = resp.get("data", []) if isinstance(resp, dict) else []
    if not exes:
        return ("YELLOW", f"no executions ever — untested in production", 0, None, None)

    # Aggregate
    statuses = [e.get("status", "?") for e in exes]
    success_count = sum(1 for s in statuses if s == "success")
    error_count = sum(1 for s in statuses if s == "error")
    last = exes[0]
    last_at = parse_iso(last.get("startedAt"))
    age_h = (NOW - last_at).total_seconds() / 3600 if last_at else None

    # Determine status
    if error_count > 0:
        return ("RED", f"{error_count}/{len(exes)} recent runs errored", success_count, last_at, age_h)
    if success_count == len(exes):
        if window is None:
            return ("GREEN", f"event-driven; last fire {age_h:.1f}h ago, all {success_count} runs green" if age_h else "GREEN", success_count, last_at, age_h)
        if age_h is not None and age_h < window:
            return ("GREEN", f"all {success_count}/{len(exes)} runs green; last fire {age_h:.1f}h ago (within {window}h window)", success_count, last_at, age_h)
        return ("YELLOW", f"all runs green but last fire {age_h:.1f}h ago exceeds {window}h cadence window", success_count, last_at, age_h)
    return ("YELLOW", f"mixed: {success_count} success / {error_count} error / {len(exes) - success_count - error_count} other", success_count, last_at, age_h)


def deep_verify(wid):
    """Pull most recent execution data and check for hidden errors in node outputs."""
    code, resp = http("GET", f"/executions?workflowId={wid}&limit=1&includeData=true")
    if code != 200:
        return None
    exes = resp.get("data", []) if isinstance(resp, dict) else []
    if not exes:
        return None
    e = exes[0]
    runs = (e.get("data", {}) or {}).get("resultData", {}).get("runData", {}) or {}
    issues = []
    for nname, arr in runs.items():
        if not arr: continue
        last = arr[-1] if isinstance(arr, list) else arr
        err = (last or {}).get("error")
        if err:
            issues.append(f"  ⚠ node '{nname}' errored: {(err.get('message') or str(err))[:120]}")
        else:
            d_out = (last or {}).get("data", {}).get("main", [])
            if d_out and d_out[0]:
                first_out = d_out[0][0] if d_out[0] else None
                if isinstance(first_out, dict):
                    j = first_out.get("json", {}) or {}
                    if j.get("error") or (j.get("ok") is False):
                        issues.append(f"  ⚠ node '{nname}' returned error payload: {json.dumps(j)[:150]}")
    return issues


def main():
    rows = []
    for wid, name, cadence, window, notes in ACTIVE:
        status, summary, success_count, last_at, age_h = verify_workflow(wid, name, cadence, window, notes)
        deep_issues = deep_verify(wid) or []
        rows.append({
            "id": wid, "name": name, "cadence": cadence, "status": status,
            "summary": summary, "last_at": str(last_at) if last_at else None,
            "age_h": age_h, "deep_issues": deep_issues, "notes": notes,
        })
        print(f"{status:7} {wid}  {name}")
        print(f"        summary: {summary}")
        if deep_issues:
            for di in deep_issues[:5]:
                print(di)
        print()

    # Save JSON for downstream report
    with open("_handoff/audit/raw/phase4_verification.json", "w") as f:
        json.dump(rows, f, indent=2, default=str)
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"\nTotals: {counts}")


if __name__ == "__main__":
    main()
