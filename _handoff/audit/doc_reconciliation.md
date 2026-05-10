# Doc Reconciliation Audit — RequityAI AgencyOS

**Author:** Cowork audit subagent
**Date:** 2026-05-09
**Scope:** 14 docs (6 V2 drafts in `_handoff/`, 8 markdown SOPs, master state doc, Apr-26 architecture map)
**Purpose:** Single canonical source for the SOP patching pass that follows.

---

## Section 1 — Doc inventory

| # | Doc | Last updated | Coverage |
|---|---|---|---|
| 1 | `_handoff/RequityAI_Operator_Guide_V2.txt` | (no date in body — drafted May 2 2026) | New-hire onboarding guide. 9 sections: what RequityAI does, AgencyOS sync model, the tools (Slack/SmartSuite/Drive/Meta), automations + 3 agents, VA responsibilities, communication standards, daily rhythm, escalation rules, core operating principle. |
| 2 | `_handoff/SOP_03_Clients_V2.txt` | May 2, 2026 | Clients app: status meanings, M5 auto-create flow, VA read-only rules, key fields, troubleshooting. |
| 3 | `_handoff/SOP_04_Onboarding_V2.txt` | May 2, 2026 | Onboarding app: 4 phases, "19-step checklist" claim, board/checklist views, blocker handling, daily routine. |
| 4 | `_handoff/SOP_05_Campaigns_V2.txt` | May 2, 2026 | Campaigns app: 3 funnel stages, naming convention, 7-step build, 9-point QA, metrics auto-pull. |
| 5 | `_handoff/SOP_06_Tasks_V2.txt` | May 2, 2026 | Tasks app: My Queue daily loop, "15 task types" list, blocked-task rules, priorities, statuses. |
| 6 | `_handoff/SOP_09_Slack_Communication_V2.txt` | May 2, 2026 | Slack architecture: 4-channel-type map, /update structured-message format per app, the 3 agents, common mistakes. |
| 7 | `SOPs/SOP_01_Pipeline.md` | (no date) | Pipeline app: 10 stages, Won flow, deal lifecycle, key fields. |
| 8 | `SOPs/SOP_02_Conversation_Tracker.md` | (no date) | Conversation Tracker: how to log, fields, n8n Close→SS sync. |
| 9 | `SOPs/SOP_03_Clients.md` | (no date) | Clients app v1 — same shape as V2 draft, fewer details. |
| 10 | `SOPs/SOP_04_Onboarding.md` | (no date) | Onboarding v1 — has Phase 4 audience build struck through, "19 steps" claim. |
| 11 | `SOPs/SOP_05_Campaigns.md` | (no date) | Campaigns v1 — same shape as V2 draft. Notes "Windsor pulls daily" (V2 says 12h). |
| 12 | `SOPs/SOP_06_Tasks.md` | (no date) | Tasks v1 — "15 types" list, includes "Create Retargeting Audiences". |
| 13 | `SOPs/SOP_07_Optimization.md` | (no date) | Optimization app: 72hr trigger, decision rules per campaign type, Andrew-only. |
| 14 | `SOPs/SOP_08_Finance.md` | (no date) | Finance app: record types, payment status, monthly revenue check, Andrew-only. |
| 15 | `AgencyOS_Current_State.md` | 2026-04-20 | Stale master state doc: claims 24 workflows, 4 clients, `#team-tasks`. |
| 16 | `AgencyOS_Architecture_AtoZ_Apr26.md` | 2026-04-26 | Most current architecture map: 21 workflows, 6 clients, niche-aware M5, `#team-operations`. Doc itself states it supersedes Current_State. |

---

## Section 2 — Confirmed misalignments (M1–M11)

### M1 — `#team-tasks` vs `#team-operations` (channel rename)

**Issue:** Channel was renamed Apr 22; some docs still reference old name.

**Affected:**
- `SOP_01_Pipeline.md:108` — "Check Slack #team-tasks for an error notification."
- `SOP_02_Conversation_Tracker.md:97` — "Check #team-tasks on Slack for error notifications."
- `SOP_03_Clients.md:113` — "Check #team-tasks in Slack for an error."
- `SOP_07_Optimization.md:141` — "Check #team-tasks Slack channel."
- `AgencyOS_Current_State.md:14` — "(#team-tasks = C0AKWU4835E)"
- `AgencyOS_Current_State.md:84,87` — "Task Assigned → DMs VA in #team-tasks", "#team-tasks — unified VA feed".

**Source of truth:** Authoritative fact #1, `feedback_notification_quiet_hours` adjacent — `#team-tasks` renamed to `#team-operations` Apr 22; ID `C0AKWU4835E` unchanged. Confirmed in `SOP_09_V2:107` ("renamed on April 22, 2026").

**Decision:** All references → `#team-operations`. Keep `C0AKWU4835E` ID where it appears.

**Patch:** Replace `#team-tasks` → `#team-operations` in 4 markdown SOPs and master state doc. 6 callsites total.

---

### M2 — Dead channel `C0AKWU4H8C8` referenced anywhere

**Issue:** Per memory note, `C0AKWU4H8C8` is dead and should appear nowhere.

**Affected:** Grepped — not present in any of the 14 docs read. Already clean. No patch needed in this doc set.

**Decision:** No-op for these docs. Audit closes M2 clean. (Flag remains active for n8n workflow JSON outside this doc scope.)

---

### M3 — "Create Retargeting Audiences" listed as active task type

**Issue:** Retired May 5. Folded into SOP_05 Step 4 (audiences auto-build from Video Views; VA confirms existence). Still appears in two task lists and one example.

**Affected:**
- `SOP_06_Tasks.md:49` — full row in 15-types table: "**Create Retargeting Audiences** | Create custom audiences in Ads Manager. The Campaign Intelligence Agent creates this task with specific specs..."
- `SOP_06_Tasks_V2.txt:87` — same row in 15-types table.
- `SOP_09_V2:64` — listed in valid Task Types: "...Create Retargeting Audiences, Upload Ad Creatives..."
- `SOP_09_V2:163` — example uses it: `Task: Create Retargeting Audiences / Status: Blocked`.
- `SOP_04_Onboarding_V2.txt:73` — prose: "creates a 'Create Retargeting Audiences' task in Tasks when thresholds are hit."
- `SOP_04_Onboarding.md:59` — same prose: "creates a 'Create Retargeting Audiences' task for the VA with specific specs".
- `Operator_Guide_V2:73` — describes retargeting audience creation as a possible "operational task for you (e.g., swap creative, build retargeting)".

**Source of truth:** Authoritative fact #3 + memory `project_audience_creation_collapsed_may05`.

**Decision:** Remove the task type entirely. Replace mentions with: "VA confirms 25%/50%/75%/95% video-viewer audiences exist before building Retarget/Lead Ad campaigns (Campaigns SOP Step 4). Audiences auto-build."

**Patch:**
- `SOP_06_Tasks.md`: drop line 49; renumber "15 types" → "14 types" at line 33.
- `SOP_06_Tasks_V2.txt`: drop line 87; "15" → "14" at line 17–18.
- `SOP_09_V2`: drop from line 64 list; rewrite line 159–163 example to use a different blocked task (e.g., "Set Up Ad Account Access" — access pending).
- `SOP_04_Onboarding_V2.txt:72-73`: rewrite to "Retarget + Lead Ad audiences auto-build from Video Views activity. The VA confirms they exist when assigned the relevant Build Campaign task — see SOP 05 Step 4."
- `SOP_04_Onboarding.md:59`: same rewrite.
- `Operator_Guide_V2:73`: drop "build retargeting" from the example list.

---

### M4 — ConvTracker `last_call_outcome` 11 vs 15 values

**Issue:** Expanded 11 → 15 values on May 6. Affected docs reference no canonical list, but anything that does needs the new count.

**Affected:**
- `SOP_02_Conversation_Tracker.md:30-32` — only lists 3 outcome values: Interested / Maybe / Not Interested. This is a **separate field** (`Outcome`) not the Close-CRM-mirrored `last_call_outcome`. Both fields exist; the doc only documents one.

**Source of truth:** Authoritative fact #4 + memory `project_convtracker_outcome_expansion_may06`.

**Decision:** SOP_02 needs a new section / table for `last_call_outcome` (15 values, populated by M2b polling — VAs do not edit). Keep existing `Outcome` documentation as is.

**Patch:** Add to `SOP_02_Conversation_Tracker.md` after line 51 (between "Outcome vs Call Booked" and "n8n Sync") a new subsection documenting `last_call_outcome` field — populated by M2b poll, 15 values matching Close call outcomes (Andrew to supply the exact 15 if not already in Structure Spec; the M2b workflow has the map). VAs do not edit.

---

### M5 — Operator Guide implies prospects self-book

**Issue:** Operator Guide section 2 describes the booking flow as: "A prospect books a call → the sales pipeline record is created or updated automatically." Reads as if prospects book themselves via Calendly. They don't — Andrew books live on the call.

**Affected:**
- `Operator_Guide_V2:30` — "A prospect books a call → the sales pipeline record is created or updated automatically."
- `Operator_Guide_V2:212` — table row: "Prospect books a call | Creates or updates the sales pipeline record. Hydrates company name, phone, and Close lead reference automatically."

**Source of truth:** Authoritative fact #5 + memory `feedback_andrew_books_not_prospects` + `feedback_no_slack_book_command`.

**Decision:** Reword to make clear Andrew books in Calendly during the discovery conversation. M3 webhook still fires the same downstream chain; the trigger is Andrew's manual booking, not a self-service prospect link.

**Patch:**
- `Operator_Guide_V2:30`: change to "Andrew books a prospect on Calendly during the discovery conversation → the sales pipeline record is created automatically (M3 webhook)."
- `Operator_Guide_V2:212`: change first cell to "Andrew books a prospect in Calendly".

---

### M6 — Campaign Intelligence Agent presented as actively running

**Issue:** Operator Guide section 4 describes Campaign Intelligence Agent in present tense as if it's currently running. It's dormant — activates on first live campaign.

**Affected:**
- `Operator_Guide_V2:71-73` — "Three managed intelligence agents support the system... Reviews live campaign data — spend, leads, cost per lead, campaign age, status. Writes a recommended decision into SmartSuite."

**Source of truth:** Authoritative fact #6. SOP_09 V2 already says it correctly (line 139): "The Campaign Intelligence Agent is currently dormant — it activates the moment a real campaign goes live."

**Decision:** Add the "currently dormant — activates on first live campaign" qualifier to Operator Guide. Keep the description of what it does.

**Patch:** `Operator_Guide_V2:73` — append sentence: "Note: this agent is currently dormant. It activates the moment a real campaign goes live; until then, no recommendations will appear."

---

### M7 — Active client count: 4 vs 6

**Issue:** State doc + V1 SOPs assume 4 clients. Apr-26 architecture doc + Apr-25 Slack probe confirm 6.

**Affected:**
- `AgencyOS_Current_State.md:27` — "4 clients, all bi-linked to Onboarding"
- `AgencyOS_Current_State.md:100` — "Clients: 4 (Real-Vantage, First Integrity, Quick Home Buyers, Ritsel Notes)"
- `AgencyOS_Current_State.md:90` — "#team-<client> (private x4)" / "#client-<client> (public x4)"
- `AgencyOS_Current_State.md:105` — "Drive: 4 client folders"
- `SOP_09_V2:117-120` — Current Client Channels table lists only 4: Ritsel Notes, Quick Home Buyers, RealVantage, First Integrity.

**Source of truth:** Authoritative fact #7 + `AgencyOS_Architecture_AtoZ_Apr26.md:441` — "6 active clients: Bayrock Home Buyers, Next Journey, Real-Vantage, First Integrity, Quick Home Buyers, Ritsel Notes."

**Decision:** Update count to 6 everywhere. Add Next Journey Homes + Bayrock Home Buyers (both Apr 25, both with **private** client channels — see M12 below) to client channel table.

**Patch:**
- `AgencyOS_Current_State.md`: lines 27, 90, 100, 105 — update counts to 6, add the two new client names.
- `SOP_09_V2:117-120`: add 2 rows for Next Journey Homes + Bayrock Home Buyers, with a note that their `#client-` channel is private (vs the original 4 which are public).

---

### M8 — n8n active workflow count: 24 vs 21

**Issue:** State doc says 24. Apr 26 audit dropped to 21.

**Affected:**
- `AgencyOS_Current_State.md:11` — "24 active workflows (not 37 — old number was pre-cleanup)"
- `AgencyOS_Current_State.md:36` — "n8n — 24 Active Workflows (verified Apr 20 13:40 UTC)"
- `AgencyOS_Current_State.md:38-66` — full list of 24 workflows; missing M2b polling, M4 No-Show, M5 Deal Won, M3 Close hydration, Daily Sales Brief, Form Watcher fix; still lists `dInuMwYxjwcftjSp` M2 webhook as live (replaced Apr 22 — see M11).

**Source of truth:** Authoritative fact #8 + memory `project_execution_audit_apr26` + `AgencyOS_Architecture_AtoZ_Apr26.md:80,347`.

**Decision:** Update master state doc workflow count to 21, replace the workflow list with the corrected one in Apr-26 architecture map (sections D + I), or have state doc reference the architecture doc as canonical.

**Patch:** `AgencyOS_Current_State.md` — rewrite header (line 11) and workflow list (lines 38–66) to match Apr-26 architecture (21 workflows, divided event-driven / scheduled / deactivated). Best path: replace lines 36–66 with a one-liner pointing to `AgencyOS_Architecture_AtoZ_Apr26.md` as canonical, plus explicit "21 active" count.

---

### M9 — Calendly + M-series workflow status not reflected in V1 SOPs

**Issue:** V1 SOPs predate Calendly + M-series infra. SOP_01 says "n8n will automatically create a new record in the Clients app" without naming M5; SOP_03 same. Master state doc has M3 LIVE but not M4, M5, M3 Close hydration. Reality: M3 (Apr 20) + M4 (Apr 22) + M5 (Apr 24) + M5 niche-aware (Apr 25) + M3 Close hydration (Apr 26) all LIVE.

**Affected:**
- `SOP_01_Pipeline.md:57-58` — "n8n will automatically create a new record in the Clients app and start the onboarding flow." (Generic — should name M5 + niche delivery + dual channels.)
- `SOP_03_Clients.md:24` — "n8n automatically creates a new client record here and kicks off onboarding." (Same.)
- `AgencyOS_Current_State.md` — claims M3 LIVE Apr 20, no mention of M4/M5/M3-Close-hydration; section heading dated Apr 20.

**Source of truth:** Authoritative fact #9 + memory entries `project_m3_calendly_live_apr20`, `project_m4_noshow_bridge_live_apr22`, `project_m5_deal_won_live_apr24`, `project_m5_niche_aware_apr25`, `project_m3_close_hydration_apr26`.

**Decision:** V1 SOPs (Pipeline, Clients) get a one-line callout naming M5 + niche-aware doc delivery + Slack channel pair creation as part of the Won flow. State doc gets the Apr 22/24/25/26 milestones added or replaced wholesale by Apr-26 architecture map.

**Patch:**
- `SOP_01_Pipeline.md:57`: rewrite to mirror SOP_03_V2 lines 50–58 (M5 atomically creates Client + Onboarding + Drive folder + 2 Slack channels + niche-aware welcome doc).
- `SOP_03_Clients.md:24`: same rewrite.
- `AgencyOS_Current_State.md`: replace whole doc with pointer to Apr-26 architecture map, OR backfill the Apr 22/24/25/26 events. Recommend: replace with pointer (Apr-26 doc itself states it supersedes the state doc).

---

### M10 — CSV Import as primary build method

**Issue:** Authoritative fact #10 — Andrew has decided to scrap CSV Import as primary. Manual fresh build per a sharp SOP_05.

**Affected:**
- `SOP_06_Tasks.md:43-44` — "Build Campaign (CSV Import) | Build campaigns using the CSV import method — the primary method for duplicating campaigns across clients at scale." + "Build Campaign (Manual) | Build a single campaign manually..."
- `SOP_06_Tasks_V2.txt:81-82` — same two rows.
- `SOP_09_V2:64` — Valid Task Types list: "Build Video Views Campaign, Build Retarget Campaign, Build Lead Ad Campaign, ... CSV Import Build, ...".
- `AgencyOS_Current_State.md:144` — "VA builds via CSV Import (primary) or Manual (fallback)"
- Memory `project_csv_import_build` — old decision, now superseded.

**Source of truth:** Authoritative fact #10 (Andrew's decision in this session).

**Decision:** Collapse "Build Campaign (CSV Import)" + "Build Campaign (Manual)" into single "Build Campaign" task type. CSV Import retired. Memory entry needs updating after this audit (out of scope here — flag for parent).

**Patch:**
- `SOP_06_Tasks.md`: replace the two rows at lines 43–44 with a single row: "**Build Campaign** | Build a single campaign manually in Ads Manager + SmartSuite. Follow SOP 05."
- `SOP_06_Tasks_V2.txt:81-82`: same replacement.
- `SOP_09_V2:64`: in Valid Task Types list, replace the trio "Build Video Views Campaign, Build Retarget Campaign, Build Lead Ad Campaign" + "CSV Import Build" with single "Build Campaign". (Note: SOP_09's task type list is internally inconsistent with SOP_06's — see Section 5 vocabulary canonicalization.)
- `AgencyOS_Current_State.md:144`: rewrite "VA builds manually following SOP_05".

---

### M11 — Onboarding step count: 19 vs 18 vs 17

**Issue:**
- SOP_04 V2 prose says "19-step checklist" (lines 8, 28, 52).
- SOP_04 V2 phase enumeration counts 18: Phase 1 = 5 steps + Phase 2 = 5 + Phase 3 = 4 + Phase 4 = 4. (Lines 56–78.)
- SOP_04 V1 markdown enumerates same 18 (lines 26–69) but claims "19 steps" (lines 86, 112).
- SOP_09 V2 enumerates 17 named steps + 1 master flag "Onboarding Complete" (lines 68–73): Access 5 + Lead 5 + Videos 3 + Launch 4 + Master 1. The Videos phase is missing "Videos Edited" (which is in SOP_04 lines 70).
- Apr-26 architecture map (lines 151–179) enumerates exactly 18 named steps: 5+5+4+4 (matches SOP_04 V2 phase tables, not the "19" prose).

**Source of truth:** Authoritative fact #11 — needs live SS probe to resolve. Doc evidence strongly suggests **18 steps + 1 master flag** = 19 fields total, which would explain the "19" claim if "Onboarding Complete" was being counted as a step.

**Decision:** Most likely correct: **18 named steps** in 4 phases, plus 1 master flag (`Onboarding Complete`). The "19" originates from counting the master flag as a step. Verification needed via SS app probe (App ID `69db909cd9114601cccb2b57`, count `step_*` fields). Recommend canonical wording: "18 onboarding steps across 4 phases, plus the master `Onboarding Complete` flag (19 dropdown fields total)."

**Patch (pending live verification):**
- `SOP_04_Onboarding_V2.txt`: lines 8, 28, 52 — rewrite "19-step" → "18-step" or use the canonical phrasing above.
- `SOP_04_Onboarding.md`: lines 86, 112 — same rewrite. Also drop the "Videos Edited" inconsistency vs SOP_09.
- `SOP_09_V2:68-73`: add "Videos Edited" to Videos phase if SS probe confirms it exists. Reads like a doc copy-paste error.
- `AgencyOS_Current_State.md:28` — already says "19 step fields" (literally fields, not steps) which is fine.
- `AgencyOS_Architecture_AtoZ_Apr26.md`: line 58 says "19 step_ dropdowns" + lines 151 say "19 STEPS" but enumerates 18. Match its own enumeration.

**Action item:** Probe SS Onboarding app for `step_*` field count BEFORE patching this. Memory `feedback_read_spec_first` applies.

---

## Section 3 — Net-new misalignments (M12+)

### M12 — New client channels are PRIVATE; existing 4 are PUBLIC

**Issue:** SOP_09 V2 line 111–115 says the channel-pair pattern is "client-{slug} (public, client-facing)" + "team-{slug} (private, internal)". Authoritative fact #7 says Next Journey Homes + Bayrock Home Buyers — both Apr 25 — have **private** client channels (not public). The architecture map says M5 creates `#client-{slug}` as public (line 271). So either (a) M5 was changed Apr 25 to default new client channels to private, (b) Andrew manually flipped privacy after creation, or (c) the original 4 are anomalous.

**Affected:**
- `SOP_09_V2:111` — "client-<client> | Client-facing channel (if the client is in Slack). Professional tone only."
- `SOP_09_V2:115` — "Two channels per client — never mix them up... #client-<client> = EXTERNAL. Client may be reading."
- `AgencyOS_Architecture_AtoZ_Apr26.md:271` — "#client-{slug} | External, client-facing | M5 on Won"
- M5 source code (out of scope here) — defines channel privacy default.

**Decision needed:** Open question for Andrew (Section 4 #Q1). Does the new default for M5-created `#client-{slug}` channels need to flip to private? If yes, M5 needs a code change AND the SOP needs to say "private by default; Andrew flips to public when client is invited as guest."

---

### M13 — SOP_06 says SmartSuite/n8n syncs "daily"; SOP_05 V2 says 12h; both correct, both inconsistent

**Issue:** Windsor sync cadence inconsistent across docs.
- `SOP_05_Campaigns.md:152` — "Windsor AI pulls performance data from Facebook **daily**"
- `SOP_05_Campaigns_V2.txt:73` — "Windsor AI pulls performance data from Facebook **every 12 hours**"
- Apr-26 architecture map line 248, 378 — "Every 12h"

**Source of truth:** Apr-26 architecture map says every 12h.

**Decision:** Canonical is 12h. SOP_05 v1 markdown line 152 → patch.

**Patch:** `SOP_05_Campaigns.md:152` → "Windsor AI pulls performance data from Facebook every 12 hours".

---

### M14 — SOP_07 references "Launch Date" mislabel as known UI issue

**Issue:** `SOP_07_Optimization.md:100` documents a UI rename gap (column header says "Launch Date" but field is actually Review Date). It's a 30-second fix that's been sitting. Either fix in SS UI or remove the note from the SOP.

**Affected:** `SOP_07_Optimization.md:100,142`.

**Source of truth:** Andrew's call.

**Decision:** Open question (Section 4 #Q2). Fix the SS UI rename and drop the SOP comment OR keep the doc explanation.

---

### M15 — Pipeline stage list inconsistent across docs

**Issue:**
- `SOP_01_Pipeline.md:17-29` — 10 stages: Conversation - Positive / Follow Up / Reschedule / Booked / No Show / Cancelled / Proposal - Decision - Pending / Ghosted / Signed - Invoice Sent / Won / Lost.
- `SOP_09_V2:75` — 11 stages: Lead, Contacted, Discovery Call, NDM (No Decision Made), Proposal Sent, Negotiation, Verbal Commit, Onboarding, Active Client, Churned, Lost.
- `AgencyOS_Architecture_AtoZ_Apr26.md:55` — "7 stages (Booked → Engaged → Qualified → Proposal → Won / Lost / No Show)".
- `AgencyOS_Architecture_AtoZ_Apr26.md:114` — "Booked → Engaged → Qualified → Proposal → Won / Lost / No Show" (same 7).
- Memory `project_pipeline_stage_fix` says 10 choices matching Close CRM exactly, slug `deal_stage`.
- Memory `project_m2_replaced_by_polling_apr22` says "NDM choice added (11 total)".

**Source of truth:** Most current = memory `project_m2_replaced_by_polling_apr22` (Apr 22) → 11 stages, slug `deal_stage`. SOP_09 V2's 11-value list (which includes NDM) likely comes from this memory; it's also internally inconsistent with the architecture map.

**Decision:** Pull live `deal_stage` choices via SS API before canonicalizing. Until then, canonical is the 11 from SOP_09 V2 (most recent doc) — but verify. Note that SOP_09's 11 ("Lead, Contacted, Discovery Call...") and the architecture map's 7 ("Booked → Engaged...") use **different vocabulary entirely**, suggesting one of them is outdated language.

**Patch (pending probe):** Re-pull `deal_stage` from SS API. Single canonical 11-value list goes everywhere — SOP_01, SOP_09, architecture map. SOP_01's 10-value list is definitively stale.

**Action item for parent:** Probe SS Pipeline app `deal_stage` field options before patching.

---

### M16 — SOP_05 V2 build sequence puts Special Ad Category in QA list, not in build steps

**Issue:** SOP_05 V2 "Step 4 — Build in Ads Manager" omits "Set Special Ad Category = Housing" as an explicit build step. It only appears in the QA checklist (line 132) and as one of "Three things that will break the system" (line 124). SOP_05 V1 markdown line 110 has it explicitly as build step #8.

**Affected:** `SOP_05_Campaigns_V2.txt:34-53`.

**Source of truth:** SOP_05 V1 (operationally complete). Andrew's Apr decision: Special Ad Category = Housing is non-negotiable.

**Decision:** Add explicit "Set Special Ad Category = Housing" as a numbered build step in V2, between "Set the CTA" and "Do NOT use zip code targeting".

**Patch:** `SOP_05_Campaigns_V2.txt:53` (between "Lead Ad → Facebook Lead Form attached" and "Do NOT use zip code targeting") — insert: "Set **Special Ad Category = Housing**. ⚠️ Required by law. Skipping risks an account ban."

---

### M17 — Operator Guide mentions "video editor" as separate role; no other doc does

**Issue:** Operator Guide V2 line 55 + 99 references a separate "video editor" who processes raw videos. Other docs treat this as VA work (`project_creative_workflow`: "VA processes → Drive Ad Creative folder"; SOP_06 Task type "Upload Creative" line 78: "Move client raw videos from Raw Video → Ad Creative folder...once edited and ready" — passive voice on the editing).

**Affected:**
- `Operator_Guide_V2:55` — "The video editor processes them."
- `Operator_Guide_V2:99` — "The video editor produces approved ad creative."
- `SOP_06_Tasks_V2.txt:78` — "Move client raw videos from Raw Video → Ad Creative folder in Google Drive **once edited and ready**." (Implies external party.)
- `SOP_04_Onboarding_V2.txt:70` — "Videos have been edited and processed (moved from Raw Video folder to Ad Creative folder)." (Implies VA does it.)
- Apr-26 architecture map line 320–321 — "Video editing (per client — Phase 3) — VA pulls raw video..., edits, drops finished asset into Ad Creatives/. Editor work is human craft."

**Source of truth:** Architecture map says VA does it. No memory note about a separate video editor role.

**Decision:** Open question for Andrew (Section 4 #Q3). Is there a separate video editor on the team or is this a VA task? If VA, Operator Guide language needs to change; if separate role, SOP_04 + SOP_06 + architecture map need to acknowledge them.

---

### M18 — `Operator_Guide_V2` lists "swap creative" + "build retargeting" as VA-executable optimization tasks

**Issue:** `Operator_Guide_V2:73` — "The recommendation may translate into an operational task for you (e.g., swap creative, build retargeting)..." But "build retargeting" is retired (M3 above). Also, swap creative is real (Decision Router writes it as a task type — architecture map line 243).

**Decision:** Drop "build retargeting" from the example. Keep "swap creative." Already covered by M3 patch.

---

### M19 — Operator Guide describes "Sync Agent" as Slack-driven only; SOP_09 + architecture say Sync Agent parses `/update`

**Issue:** Both documents agree the agent parses Slack `/update`. No real misalignment — labelled M19 only to confirm cross-checked. **No patch.**

---

### M20 — `feedback_no_timed_api_keys` rule violated by `signal` key

**Issue:** Memory `reference_n8n_api_key` notes the old "signal" key expires May 14. Today is May 9. **5 days to expiry.** Not a doc issue — flagging because it intersects with the docs reference (`reference_n8n_api_key.md`).

**Action:** Revoke the old `signal` key manually in n8n UI before May 14 to avoid silent breakage. Out of scope for this doc-reconciliation file, but flag for parent.

---

## Section 4 — Open questions requiring Andrew's decision

### Q1 — New client channel privacy default

The 4 original `#client-{slug}` channels are public; the 2 new ones (Next Journey Homes, Bayrock Home Buyers — both Apr 25) are private. Decision: should M5 default new `#client-` channels to **private** going forward (matching the recent 2), or **public** (matching the original 4)? Current M5 code defaults to public per architecture map line 271. Until Andrew decides, SOP_09 should call out the ambiguity rather than picking one.

### Q2 — SOP_07 SmartSuite UI rename of "Launch Date" → "Review Date"

The mislabel on the Optimization app column header has been documented as a 30-second fix for weeks. Fix it in SS UI now and drop the SOP note, or leave both as is? Recommend: fix the UI, drop the SOP note. Owner: Andrew.

### Q3 — Video editor role

Is video editing a separate hired role (Operator Guide V2 implies yes), or is it the VA's job (SOP_04, SOP_06, architecture map all imply yes)? Reconcile to a single canonical answer before patching.

### Q4 — Pipeline stages canonical list

Probe `deal_stage` choices in SS Pipeline app to resolve the SOP_01-vs-SOP_09-vs-architecture-map disagreement (10 vs 11 vs 7 stages, with overlapping but non-identical labels). Likely answer is 11 per memory note. Andrew confirms.

### Q5 — `last_call_outcome` 15-value list

The 15 expanded values (Hung Up / LVM / Voice Agent / Invalid + 11 originals) are not enumerated in SOP_02. Either pull them from the live SS app or from the M2b workflow JSON. Andrew confirms canonical list before SOP_02 gets patched.

### Q6 — Master state doc — replace or backfill

`AgencyOS_Current_State.md` is stale on workflow count, M-series infra, client count, channel name, build method. Cleanest fix: delete the doc entirely and let `AgencyOS_Architecture_AtoZ_Apr26.md` be the single canonical state doc. The Apr-26 doc itself states it "supersedes" Current_State at line 481. Andrew confirms: delete Current_State.md, or keep + backfill?

---

## Section 5 — Vocabulary canonicalization: Task Types

### Source lists

**SOP_06 V2** (15 types — `_handoff/SOP_06_Tasks_V2.txt:75-89`):
1. Set Up Ad Account Access
2. Set Up Lead Forms
3. Request Videos
4. Upload Creative
5. Write Script
6. Admin
7. Build Campaign (CSV Import)
8. Build Campaign (Manual)
9. QA Campaign
10. Launch Campaign
11. Campaign Review
12. Cut / Pause Campaign
13. Create Retargeting Audiences
14. Update SmartSuite Records
15. Escalation Follow-Up

**SOP_09 V2** (15 types — `_handoff/SOP_09_Slack_Communication_V2.txt:64`):
1. Build Video Views Campaign
2. Build Retarget Campaign
3. Build Lead Ad Campaign
4. Create Retargeting Audiences
5. Upload Ad Creatives
6. Process Raw Video
7. QA Campaign
8. Launch Campaign
9. Set Up Ad Account Access
10. Configure Lead Notifications
11. Send Video Brief
12. Organic Page Post
13. CSV Import Build
14. Optimization Review
15. General Task

The two lists overlap on only ~5 names (QA Campaign, Launch Campaign, Set Up Ad Account Access, Create Retargeting Audiences, and the build-campaign concept). They are not the same list.

### Canonical 13-task list (proposed)

After applying Andrew's decisions (retire Create Retargeting Audiences May 5, collapse CSV Import + Manual into single Build Campaign), and choosing the more operationally-useful name where they conflict:

| # | Canonical Task Type | One-sentence definition |
|---|---|---|
| 1 | Set Up Ad Account Access | VA requests access to client's Meta Business Portfolio + ad account; confirms visibility in Business Manager. |
| 2 | Set Up Lead Forms | VA configures Facebook Lead Centre and connects it to the client's CRM/destination; confirms test lead delivery. |
| 3 | Send Video Brief | VA sends the niche-specific video recording brief to the client and follows up until videos are received. |
| 4 | Upload Creative | VA moves client-recorded videos from Raw Videos folder to Ad Creatives folder in Drive after editing. |
| 5 | Write Script | VA reviews and edits an AI-generated script for the client's voice before recording. |
| 6 | Build Campaign | VA builds a single Facebook ad campaign in Ads Manager + mirrors record in SmartSuite per SOP_05 (Special Ad Category = Housing required). |
| 7 | QA Campaign | VA runs the 9-point QA checklist in SmartSuite and Ads Manager before publish. |
| 8 | Launch Campaign | VA publishes the QA-passed campaign in Ads Manager and flips SmartSuite Status to Live. |
| 9 | Cut / Pause Campaign | VA pauses or cuts an underperforming campaign per Decision Router output. |
| 10 | Swap Creative | VA replaces an ad's creative with an approved alternate per Decision Router output. |
| 11 | Adjust Targeting | VA modifies audience targeting per Decision Router output. |
| 12 | Update SmartSuite Records | VA performs a one-off SS data update — Notes field describes which app/record/field. |
| 13 | Escalation Follow-Up | VA follows up on an escalated blocker per Notes. |

### Notes on the canonical list

- **Removed:** Create Retargeting Audiences (M3 — retired May 5).
- **Collapsed:** Build Campaign (CSV Import) + Build Campaign (Manual) → "Build Campaign" (M10).
- **Renamed for clarity:** "Request Videos" → "Send Video Brief" (SOP_09's name; more action-oriented).
- **Added from architecture map (Decision Router output types):** Swap Creative, Adjust Targeting (these match the actual Decision Router task types — architecture map lines 240–244 — and were missing from both source lists).
- **Dropped from SOP_09 list:** "Build Video Views Campaign" / "Build Retarget Campaign" / "Build Lead Ad Campaign" — collapsed into Build Campaign (the campaign type is in the campaign record, not the task type).
- **Dropped from SOP_09 list:** "Optimization Review" — covered by SOP_07 review records, not a Task.
- **Dropped from SOP_09 list:** "Organic Page Post" — per memory `project_organic_posting_decision`, this is VA work but no task type currently fires. Keep manual until automated.
- **Dropped from SOP_09 list:** "Process Raw Video" — covered by Upload Creative.
- **Dropped from SOP_09 list:** "Configure Lead Notifications" — covered by Set Up Lead Forms.
- **Dropped:** "Admin" / "General Task" — fold into Update SmartSuite Records or Escalation Follow-Up. If kept, it's a 14th catch-all bucket. Andrew picks.
- **Reality check needed:** the SS Tasks app dropdown needs to be updated to match this canonical list. Memory `project_audience_creation_collapsed_may05` already notes "SS dropdown + n8n still need cleanup."

### Open vocabulary question for Andrew

Keep "Admin" / "General Task" as a 14th bucket, or fold into existing types? Recommend: drop. If a task doesn't fit one of the 13, it's likely "Update SmartSuite Records" or "Escalation Follow-Up."

---

## Section 6 — Stale references to retired infra

### S1 — Close Pipeline as a writable system

Retired Apr 19 (memory `project_close_pipeline_retired_apr19`). Close = calling only.

**Affected:**
- `SOP_01_Pipeline.md:80` — "**Close Deal ID** | Auto-populated by the Close CRM sync. Don't touch this." → still accurate (read direction only); leave but verify field still populates from M3 Close hydration not from Pipeline-write-back.
- `SOP_01_Pipeline.md:109` — "Close CRM sync not working | Check n8n for a failed workflow. Andrew handles this." → vague but not wrong.
- `SOP_02_Conversation_Tracker.md:49,67-72` — references "Close CRM" as syncing inbound (correct: M2b polls). Does **not** describe writing back to Close. Clean.
- No SOP describes writing to Close. Clean on this dimension.

**Patch:** No-op for SOP content. Confirmation only.

### S2 — Original M2 webhook (replaced Apr 22 by polling)

Memory `project_m2_replaced_by_polling_apr22` — M2 webhook was silently broken (custom.prefix bug); polling workflow `15VLgXsxSNGbJIdp` LIVE since Apr 22.

**Affected:**
- `AgencyOS_Current_State.md:60` — "**Event/webhook-driven:** `dInuMwYxjwcftjSp` — M2 Close CRM Webhook → SmartSuite (push)" — STALE. Workflow is no longer the canonical path; M2b polling is. The Apr-26 architecture map (line 354) lists M2b polling at `15VLgXsxSNGbJIdp` as the authoritative ingress.
- `AgencyOS_Current_State.md:74` — "└─ call outcomes ──[M2 webhook → ConvTracker]──> SmartSuite" — STALE. Should say "M2b 30-min poll".

**Patch:** Replace `dInuMwYxjwcftjSp` → `15VLgXsxSNGbJIdp` and "M2 webhook" → "M2b 30min poll M-F 8am–3:30pm ET" in `AgencyOS_Current_State.md`. (Master state doc is being deprecated per Q6 anyway.)

### S3 — Dead channel `C0AKWU4H8C8`

Not present in any of the 14 docs scanned. Clean. (Still flagged in memory `reference_slack_channels` as DEAD — out of scope but parent should grep n8n workflows for it.)

### S4 — `#new-clients` channel

`AgencyOS_Current_State.md:91` — "#new-clients — onboarding handoffs" is referenced as live. Apr-26 architecture map omits it entirely. M5 posts to `#team-operations`, not `#new-clients`. Likely defunct.

**Patch:** Drop `#new-clients` from `AgencyOS_Current_State.md:91`. Verify in Slack workspace before deleting if Andrew wants to keep the doc.

### S5 — Manus references

Memory `project_architecture_decisions` — "Manus→Signal shift". State doc line 17 says "Builder: Signal (Manus retired Apr 17)". Apr-26 architecture map line 43 says "Builder/operator: Cowork (this agent)". Both are correct in their context (Signal writes scripts; Cowork operates the stack).

**Patch:** Master state doc line 17 — update or drop. Apr-26 doc is canonical: "Cowork = builder/operator; Signal = script generator (creative workflow)."

### S6 — Old workflow IDs referenced in stale state doc

`AgencyOS_Current_State.md:38–66` — workflow list missing M2b (15VLgXsxSNGbJIdp), M4 (1g5RRCFJKwWSl5ru), M5 (A31jYsKR3aETSusC), Daily Sales Brief (pa7I1FKd50TQRFrV). Covered by M8.

### S7 — "/book" Slack command — already correctly absent

Apr-26 architecture map line 282 — "Decided NOT to build: the /book Slack command." No SOP references it. Clean. Memory `feedback_no_slack_book_command` correctly enforced in docs.

### S8 — Audiences phase as a separate onboarding phase

`SOP_04_Onboarding.md:58-59` — "~~Phase 4: Audience Build~~ — REMOVED" with strikethrough. Then renames Campaign Launch as "Phase 4." Cosmetic — could be cleaner. Apr-26 architecture map line 181: "Audience Phase REMOVED — retargeting audiences auto-build from Video Views campaign activity."

**Patch:** `SOP_04_Onboarding.md:58-60`: drop the strikethrough block entirely. Replace with a one-line callout box: "Note: Retargeting audiences auto-build from Video Views campaign activity. The VA confirms they exist when assigned the Build Campaign task — see SOP 05 Step 4." Same fix as M3.

---

## Action items derived from this audit (for the patching pass)

1. **Live probes BEFORE patching** (these resolve open questions Q4, Q5, M11):
   - Probe SS Onboarding app (`69db909cd9114601cccb2b57`) — count `step_*` fields. Resolves M11.
   - Probe SS Pipeline app (`6908636826cfbf4238a34f31`) — pull `deal_stage` choices. Resolves M15/Q4.
   - Probe SS Conversation Tracker app (`69d92c38b801d747e74629d1`) — pull `last_call_outcome` 15 values. Resolves M4/Q5.
   - Probe Slack workspace channel privacy for the 6 client `#client-` channels. Confirms M12/Q1.
2. **Andrew decisions needed** (Q1–Q6 in Section 4) — surface BEFORE patching.
3. **Mechanical patches** (M1, M2, M3, M6, M7, M9, M10, M13, M14, M16, M18, S1–S8) can proceed once the above are resolved.
4. **n8n + SS hygiene cleanup** (memory note `project_audience_creation_collapsed_may05`: "SS dropdown + n8n still need cleanup") — Tasks app dropdown needs updating to canonical 13-type list (Section 5). Out of scope for this audit but on the path.
5. **Old `signal` n8n API key revocation** before May 14 (M20).

---

*End of doc reconciliation audit.*
