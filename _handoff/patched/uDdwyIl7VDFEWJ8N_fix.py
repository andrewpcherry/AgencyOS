#!/usr/bin/env python3
"""
Workflow uDdwyIl7VDFEWJ8N — "Prerequisites Met → Auto-Create Campaign Build Task"

Two bugs:
1. Audience-step check requires 8 fields (step_audience_25_viewers …
   step_audience_form_submitted) all = '3'. Those fields don't exist on
   Onboarding records (removed in May 5 audience-phase retirement). All
   are undefined, so audiencesDone is always false, so workflow has been
   silently returning {skip:true} since May 5.
2. Task `type` writes use retired labels "Build Campaign (CSV Import)"
   and "Build Campaign (Manual)". M22 dropdown patch collapsed both into
   single canonical "Build Campaign". Writes would silently fail/error.

Fix:
- Drop audience check entirely. Trigger condition becomes:
  step_approved_videos_exist === '3' && step_campaign_built === '1'
- Replace 3 task templates with canonical "Build Campaign" type.
- Update Slack message to reflect canonical naming.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

N8N_KEY = os.environ["N8N_KEY"]
BASE = "https://requityai.app.n8n.cloud/api/v1"
WF_ID = "uDdwyIl7VDFEWJ8N"

NEW_CHECK_PREREQ_CODE = r"""const SS_TOKEN = "Token 716c2356a4f2679445cca53e374fb173be57ba7d";
const SS_ACCOUNT = "52739";
const CLIENTS_APP = "69ce5f18cb8a07430bfee02d";
const ONBOARDING_APP = "69db909cd9114601cccb2b57";
const TASKS_APP = "69ce67b3fec5b91842ebaf03";
const OPS_CHANNEL = "C0AKWU4835E";

const obRes = await this.helpers.httpRequest({
  method: 'POST',
  url: `https://app.smartsuite.com/api/v1/applications/${ONBOARDING_APP}/records/list/`,
  headers: {'Authorization': SS_TOKEN, 'ACCOUNT-ID': SS_ACCOUNT, 'Content-Type': 'application/json'},
  body: {pagination: {limit: 200, offset: 0}}
});

// Audience phase retired 2026-05-05 — retargeting audiences auto-build from
// Video Views activity. Trigger only on creative ready + campaign not yet built.
const readyRecords = (obRes.items || []).filter(r =>
  r.step_approved_videos_exist === '3' && r.step_campaign_built === '1'
);

if (readyRecords.length === 0) return [{json: {skip: true}}];

const results = [];
const today = new Date();
const dueDate = new Date(today);
dueDate.setDate(today.getDate() + 2);
const dueDateStr = dueDate.toISOString().slice(0, 10);

for (const ob of readyRecords) {
  const clientIds = Array.isArray(ob.client) ? ob.client : [];
  if (clientIds.length === 0) continue;
  const clientId = clientIds[0];
  const clientName = ob.title || 'Unknown Client';
  const obId = ob.id;

  // Canonical task vocabulary (post M22 dropdown collapse 2026-05-10):
  // single "Build Campaign" type. CSV Import / Manual variants retired.
  const buildTasks = [
    {title: `Build Campaign — TOF EDU VIDEO — ${clientName}`, funnel_stage: 'TOF', priority: 'High'},
    {title: `Build Campaign — MOF RETARGET — ${clientName}`, funnel_stage: 'MOF', priority: 'Normal'},
    {title: `Build Campaign — BOF LEADS — ${clientName}`,    funnel_stage: 'BOF', priority: 'Normal'}
  ];

  for (const bt of buildTasks) {
    await this.helpers.httpRequest({
      method: 'POST',
      url: `https://app.smartsuite.com/api/v1/applications/${TASKS_APP}/records/`,
      headers: {'Authorization': SS_TOKEN, 'ACCOUNT-ID': SS_ACCOUNT, 'Content-Type': 'application/json'},
      body: {
        title: bt.title, status: 'To Do', type: 'Build Campaign',
        task_category: 'Campaign Build', funnel_stage: bt.funnel_stage,
        priority: bt.priority, assigned_to_select: 'VA',
        client: [clientId], due_date: {from_date: {date: dueDateStr}}
      }
    });
  }

  await this.helpers.httpRequest({
    method: 'PATCH',
    url: `https://app.smartsuite.com/api/v1/applications/${ONBOARDING_APP}/records/${obId}/`,
    headers: {'Authorization': SS_TOKEN, 'ACCOUNT-ID': SS_ACCOUNT, 'Content-Type': 'application/json'},
    body: {step_campaign_built: '2'}
  });

  results.push({json: {
    channel: OPS_CHANNEL,
    message: `🏗️ *Campaign build tasks created for ${clientName}*\n\n• Build Campaign — TOF EDU VIDEO\n• Build Campaign — MOF RETARGET\n• Build Campaign — BOF LEADS\n\n_Prerequisites met: creative uploaded. Due ${dueDateStr}._`
  }});
}

return results.length > 0 ? results : [{json: {skip: true}}];
"""


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
    code, wf = http("GET", f"/workflows/{WF_ID}")
    if code != 200:
        print(f"GET failed: {code}\n{wf}")
        sys.exit(1)
    print(f"Workflow: {wf['name']} | active={wf.get('active')}")

    target = next((n for n in wf["nodes"] if n["name"] == "Check Prerequisites"), None)
    if not target:
        print("Check Prerequisites node not found")
        sys.exit(2)

    old_code = target["parameters"]["jsCode"]
    print(f"Old code: {len(old_code)} chars, has audience refs: {'step_audience_' in old_code}")
    target["parameters"]["jsCode"] = NEW_CHECK_PREREQ_CODE
    print(f"New code: {len(NEW_CHECK_PREREQ_CODE)} chars, has audience refs: {'step_audience_' in NEW_CHECK_PREREQ_CODE}")

    with open(f"_handoff/audit/raw/n8n_{WF_ID}_pre_m10_fix.json", "w") as f:
        json.dump(wf, f, indent=2)
    # Restore the original code in the in-memory wf for the backup we just wrote, then re-apply for PUT
    # Actually we already mutated target before saving — re-write backup with original code:
    target["parameters"]["jsCode"] = old_code
    with open(f"_handoff/audit/raw/n8n_{WF_ID}_pre_m10_fix.json", "w") as f:
        json.dump(wf, f, indent=2)
    target["parameters"]["jsCode"] = NEW_CHECK_PREREQ_CODE
    print("Backup saved.")

    print("\nDeactivating...")
    code, _ = http("POST", f"/workflows/{WF_ID}/deactivate")
    print(f"  → {code}")

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
        http("POST", f"/workflows/{WF_ID}/activate")
        sys.exit(3)

    time.sleep(1)
    print("Activating...")
    code, _ = http("POST", f"/workflows/{WF_ID}/activate")
    print(f"  → {code}")

    code, wf2 = http("GET", f"/workflows/{WF_ID}")
    final = next(n for n in wf2["nodes"] if n["name"] == "Check Prerequisites")["parameters"]["jsCode"]
    print(f"\nFinal verification:")
    print(f"  active={wf2.get('active')}")
    print(f"  step_audience_ count={final.count('step_audience_')} (target: 0)")
    print(f"  'Build Campaign (CSV Import)' count={final.count('Build Campaign (CSV Import)')} (target: 0)")
    print(f"  'Build Campaign (Manual)' count={final.count('Build Campaign (Manual)')} (target: 0)")
    needle = "type: 'Build Campaign'"
    print(f"  {needle!r} count={final.count(needle)} (target: 1)")


if __name__ == "__main__":
    main()
