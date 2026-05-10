# n8n + SS Live Patch Log

Append-only record of every live infra change. Per CLAUDE.md §3.0 rails — green/yellow logged here, red never executed.

---

## 2026-05-10 — Runtime patches (Phase 3 prelude, pre-authorized by Andrew this session)

### M22 — SmartSuite Tasks `type` dropdown collapse (YELLOW, executed)

- **App:** Tasks (`69ce67b3fec5b91842ebaf03`), field `type` ("📌 Task Type")
- **What:** Replaced 15 corrupted choices (6 collided on `value='2'`; "Create Retargeting Audiences" still present despite May 5 retirement) with canonical 13-task vocabulary per `doc_reconciliation.md` §5
- **Why:** RUNTIME issue. Singleselect with duplicate values can't resolve records to unique labels — blocking VA-driven task work. 0 records existed at patch time → zero migration impact
- **API path:** `PUT /api/v1/applications/{app_id}/change_field/` with flat field body. Response 200
- **Pre-state hash:** 15 choices: 6 × `value='2'` (Set Up Ad Account Access, Set Up Lead Forms, Request Videos, Upload Creative, Write Script, Admin) + 9 unique (`iQMVn`, `n6EvX`, `WvoJS`, `3LeIB`, `pjZqe`, `Kr9Qn`, `LaFdW`, `gPtcw`, `M2IdT`)
- **Post-state hash:** 13 unique-valued choices:
  | # | Label | Value |
  |---|---|---|
  | 1 | Set Up Ad Account Access | `ad_account_access` |
  | 2 | Set Up Lead Forms | `lead_forms` |
  | 3 | Send Video Brief | `video_brief` |
  | 4 | Upload Creative | `upload_creative` |
  | 5 | Write Script | `write_script` |
  | 6 | Build Campaign | `iQMVn` (preserved, was CSV Import) |
  | 7 | QA Campaign | `WvoJS` (preserved) |
  | 8 | Launch Campaign | `3LeIB` (preserved) |
  | 9 | Cut / Pause Campaign | `Kr9Qn` (preserved) |
  | 10 | Swap Creative | `swap_creative` |
  | 11 | Adjust Targeting | `adjust_targeting` |
  | 12 | Update SmartSuite Records | `gPtcw` (preserved) |
  | 13 | Escalation Follow-Up | `M2IdT` (preserved) |
- **Dropped:** Admin (collapsed/9-to-13 reduction), Campaign Review (`pjZqe` — covered by SOP_07 review records), Build Campaign (Manual) (`n6EvX` — collapsed into Build Campaign), Create Retargeting Audiences (`LaFdW` — May 5 retirement)
- **Renamed:** "Request Videos" → "Send Video Brief" (more action-oriented, matches SOP_09 V2 vocabulary)
- **Added:** Swap Creative, Adjust Targeting (Decision Router output types per architecture map)
- **Reversibility:** Re-run `m22_tasks_dropdown_patch.py` with the original `pre_choices` payload (full pre-state preserved at top of `_handoff/audit/raw/ss_app_69ce67b3fec5b91842ebaf03.json`). The 15-choice corrupted state is fully reproducible.
- **Verification:** Post-state confirmed via re-probe immediately after patch. ✅
- **Script:** `_handoff/patched/m22_tasks_dropdown_patch.py`

### Sync Agent — `sf.filter.filters` → `sf.filter.fields` typo fix (YELLOW, executed)

- **Workflow:** `8tdPtQWO4qDKEjgq` (SmartSuite Sync Agent — Slack /update Parser)
- **Node:** "SmartSuite Lookup & Update" (Code node)
- **What:** Replaced 2 occurrences of `sf.filter.filters.push(...)` with `sf.filter.fields.push(...)`. The SS list-filter API uses `fields` as the array property; `filters` was undefined, so `.push()` would throw.
- **Why:** Latent runtime bug. Audit missed it. Would have thrown `Cannot read properties of undefined (reading 'push')` the first time `/update Tasks task: X` or `/update Campaigns campaign: X` arrived. Hasn't fired because there are 0 task records and 1 test campaign record — never been triggered in production.
- **Sequence per memory rule:** deactivate → PUT → activate. n8n public API rejected the original `settings` block (`binaryMode`, `callerPolicy`, `availableInMCP` are Cloud-only keys); retried with strict-allowlist settings (`executionOrder`, `errorWorkflow`, `timezone`, `saveData*`) → 200.
- **Reversibility:** Pre-state JSON saved at `_handoff/audit/raw/n8n_8tdPtQWO4qDKEjgq_pre_filter_fix.json`. To revert, replace `sf.filter.fields.push` with `sf.filter.filters.push` and re-PUT.
- **Verification:** Final probe shows `sf.filter.filters` count=0, `sf.filter.fields.push` count=2, active=True. ✅
- **Script:** `_handoff/patched/sync_agent_filter_fix.py`
- **Note:** Sync Agent still hardcodes `SS_TOKEN` in the JS code (literal string at top of node). Same security pattern as Anthropic key leak. Deferred to credential-rotation pass — not blocking runtime.

### M10 — `uDdwyIl7VDFEWJ8N` "Prerequisites Met → Auto-Create Campaign Build Task" rewrite (YELLOW, executed)

- **Workflow:** `uDdwyIl7VDFEWJ8N` (active, daily 8am ET cron)
- **What:** Rewrote `Check Prerequisites` Code node. Two bugs fixed:
  1. **Dead audience check.** Old code required 8 fields (`step_audience_25_viewers` … `step_audience_form_submitted`) all = `'3'`. Those fields don't exist on the Onboarding app post-May 5 audience-phase retirement. All `undefined`, so `audiencesDone` was always false → workflow silently returned `{skip: true}` every day. **Confirmed via execution history**: every run since at least May 7 returned `{skip: true}`. New trigger condition: `step_approved_videos_exist === '3' && step_campaign_built === '1'` only.
  2. **Retired task type labels.** Old code wrote `type: 'Build Campaign (CSV Import)'` and `type: 'Build Campaign (Manual)'`. M22 dropdown collapse retired both labels. New code writes canonical `type: 'Build Campaign'` for all 3 task templates.
- **Why:** Workflow has been silently no-op'ing for 5+ days. Once `step_approved_videos_exist` flips to `'3'` for any onboarding record, the workflow now correctly creates the 3 Build Campaign tasks (TOF EDU VIDEO, MOF RETARGET, BOF LEADS).
- **Reversibility:** Pre-state saved at `_handoff/audit/raw/n8n_uDdwyIl7VDFEWJ8N_pre_m10_fix.json`. Restore by GET → replace `Check Prerequisites` jsCode with the saved version → PUT.
- **Verification:** Final probe shows 0 audience refs, 0 retired-label refs, 1 canonical `type: 'Build Campaign'`, active=True. ✅
- **Script:** `_handoff/patched/uDdwyIl7VDFEWJ8N_fix.py`
- **Note:** Same hardcoded `SS_TOKEN` security pattern. Deferred.

---

## Findings deferred to later phases (logged here so nothing is lost)

- **#team-tasks → #team-operations rename** in Slack node `cachedResultName` UI metadata (workflows `5cdMtOByeZVRFS6H` Slack Ops Supervisor, `CqesBe55FnP6oaxA` Onboarding Health Monitor). NOT runtime — channel ID `C0AKWU4835E` was correct, both workflows posting successfully (`ok: true` on 2026-05-09 runs). Phase 3c GREEN cosmetic rename.
- **`SS_TOKEN` hardcoded literal** in workflows `8tdPtQWO4qDKEjgq` (Sync Agent), `uDdwyIl7VDFEWJ8N` (Prereqs Met), and likely several others. Convert to n8n Credential. Same pattern as Anthropic key rotation runbook.
- **Slack bot `not_in_channel`** for `#client-real-vantage` (C0ARMBQ3PB9) per Slack Ops Supervisor 2026-05-09 08:00 ET execution: bot tried `conversations.history`, got `ok: false, error: not_in_channel`. Workflow handles gracefully but the bot needs guest-invited to all 6 client channels for full visibility. Andrew action.

---

## 2026-05-10 — Phase 3c n8n cleanup (GREEN, executed)

### Cosmetic team-tasks → team-operations rename in 2 active workflows

- `5cdMtOByeZVRFS6H` (Slack Ops Supervisor): replaced 4 `cachedResultName: "team-tasks"` UI labels + 1 node display name "Post to #team-tasks" → "Post to #team-operations" + connection refs. Channel ID `C0AKWU4835E` unchanged. Sequence: deactivate → PUT → reactivate. ✅
- `CqesBe55FnP6oaxA` (Onboarding Health Monitor): replaced 2 `cachedResultName` UI labels. ✅

Note: this was originally pitched as a P0 runtime fix, but live evidence (both workflows posting `ok: true` on 2026-05-09 runs) confirmed the channel rename never broke routing — it's purely a label-clarity change in the n8n UI.

### UTF-8 mojibake fix in 10 workflow names

`â\x86\x92` (mis-decoded `→`) and `â\x80\x94` (mis-decoded `—`) replaced with proper Unicode in workflow display names:

| ID | Old (mojibake) → New |
|---|---|
| `DH5Yx9S2RS6OO6qG` | "Task Completed â Auto-Set Completed Date" → "Task Completed → Auto-Set Completed Date" |
| `I599mjvYW4ZdkNRf` | "Won Deal â Auto-Create Onboarding Task Chain" → "Won Deal → Auto-Create Onboarding Task Chain" |
| `KEcx3yQ7kephk0cM` | "Daily Data Hygiene Check â Stale Records Alert" → "Daily Data Hygiene Check → Stale Records Alert" |
| `QGtGJydvWkR6vSCj` | "Client Communication â Onboarding Updates + Campaign Milestones" → "Client Communication → Onboarding Updates + Campaign Milestones" |
| `XGVbY2c8ijPoz54w` | "Recurring Maintenance Tasks â Event-Driven (replaces Weekly Skeleton Tasks)" → "Recurring Maintenance Tasks — Event-Driven (replaces Weekly Skeleton Tasks)" |
| `apbdh284pFlCy2hZ` | "QA Ready â Create QA Task for Andrew" → "QA Ready → Create QA Task for Andrew" |
| `qYFXgdFG6N9StUkO` | "Campaign Review Task Auto-Creator â Every 7 Days from Launch" → "Campaign Review Task Auto-Creator — Every 7 Days from Launch" |
| `rtjwykL2X3VwKZxM` | "Client Report Auto-Generator â 7-Day Cycle from Launch" → "Client Report Auto-Generator — 7-Day Cycle from Launch" |
| `uDdwyIl7VDFEWJ8N` | "Prerequisites Met â Auto-Create Campaign Build Task" → "Prerequisites Met → Auto-Create Campaign Build Task" |

`PJaJYLuesPU2oxc7` (Enterprise Demo) rename returned 400 on PUT — workflow's node graph likely has structure the public API rejects on round-trip. Cosmetic; deferred. Tag still applied.

### Lifecycle tagging — 5 tags applied to 53 workflows

Tags created in n8n via `POST /tags`:
- `active` → 21 in-cycle workflows currently driving the system
- `campaign-gated` → 13 inactive workflows that auto-reactivate when first real campaign publishes (Q-N1 resolved per Andrew). Includes: `6TuDo3mqBZSBF667` (Campaign Intelligence Agent), `iM5CNWHLS2UIIJ34` (Decision Router), `ZwXd0unFysJjWl1M` (Windsor AI → SS Metrics), plus optimization-cycle workflows that need live campaign telemetry to fire (CPL alert, 72hr review, fatigue check, etc.)
- `deprecated` → 14 workflows superseded by newer canonical workflows. 7-day soak then candidates for deletion. Includes: `dInuMwYxjwcftjSp` (M2 webhook → replaced by M2b polling Apr 22), `R4mXec6XM032MMyB` (Close→SS Pipeline Sync — Close Pipeline retired Apr 19), `Ikil2vx4jQNR7yxa` (DUPLICATE of active M4 No-Show Bridge `1g5RRCFJKwWSl5ru`), `HZ18Xb98Szin8OTQ` (Manual Deal Won — superseded by M5), `9pAsoQqBhRT4HHS6` (Manual Slack channel creator — superseded by M5), and others.
- `demo` → 1 workflow (`PJaJYLuesPU2oxc7` Enterprise Demo).
- `experimental` → 5 workflows (Telnyx, AI Maintenance Agent, Windsor v2, Client Communication, QA Ready).

All 53 tag applications returned 200. ✅

### Zombie scheduleTrigger probe (no findings)

Probed all 34 inactive workflows for execution timestamps post-2026-04-26. **Zero zombie fires detected.** The Apr 19 staticData-zombie incident pattern is fully resolved — no phantom cron firings remain in the system. No node removals required.

### Workflow count

- Before this session: 55 total (21 active, 34 inactive)
- After this session: 55 total (21 active, 34 inactive) — no deletions; deactivations remain in YELLOW per §3.0 rails. Tag-driven lifecycle gives Andrew a 7-day soak window before `deprecated` set is candidates for hard delete in a follow-up pass.


