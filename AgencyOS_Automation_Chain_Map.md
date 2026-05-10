# AgencyOS — Complete Automation Chain Map

**Date:** 2026-04-17
**Status:** Audit findings — includes bugs found and fixes applied

---

## The Full Client Journey (Trigger → Live Campaign)

### STEP 1: Deal Won in Close CRM
**What happens:** Andrew closes a deal. Opportunity status changes to "Won" in Close CRM.

**Workflow:** Close CRM Won Deal → Create SmartSuite Client `[HZ18Xb98Szin8OTQ]` — **ON**
- Schedule Trigger (periodic check)
- Find New Won Deals — queries Close CRM for recently won opportunities
- Create SmartSuite Client — creates a record in the Clients app
- Notify #operations — posts to Slack

**Output:** New Client record in SmartSuite Clients app.

---

### STEP 2: Drive Folder + Slack Channels Created
**What happens:** n8n detects the new client, creates their Google Drive folder structure and Slack channels.

**Workflow:** SmartSuite Clients → Drive Folder → Slack (v3 FIXED) `[BegEckXSgXmVffX2]` — **ON**
- Schedule Trigger
- Get All Clients → checks for missing Drive folders
- Creates Client Folder + Raw Videos subfolder + Ad Creatives subfolder
- Writes Drive URL back to SmartSuite Client record
- Slack notification

**Workflow:** Client Onboarding — Slack Trigger `[W2GRDMN8xwlQhlqg]` — **ON (Manual Trigger)**
- Gets SmartSuite Clients
- Creates public Slack channel (client-facing) + private channel (internal)
- Invites Andrew, posts welcome message
- Updates SmartSuite Client record with Slack channel IDs

**Output:** Client has Drive folder, public + private Slack channels, SmartSuite record updated with links.

---

### ⚠️ GAP: Where Does the Onboarding Record Get Created?

The Clients app has a `link_to_onboarding` field. The Onboarding app exists. But **no active workflow creates the Onboarding record**. The spec says n8n handles onboarding, but the chain from Client → Onboarding record creation is missing. Either:
- It was manual (created by hand in SmartSuite)
- A SmartSuite automation rule creates it (not visible in n8n)
- An inactive workflow handles it (M1_ClientOnboarding_Orchestrator is OFF)

**This is a gap that needs resolving.** Without a reliable Onboarding record creation step, the rest of the chain breaks.

---

### STEP 3: Client Completes Onboarding Steps
**What should happen:** Client submits form, grants access, sends videos. n8n watches for these events and updates Onboarding step fields.

**Workflow:** SmartSuite → Form Submitted Watcher `[Zv2PYFdMiBDCLcZV]` — **OFF (broken)**
- 🐛 BUG: References `ob_form_submitted` on Clients app — field doesn't exist
- **Andrew's point:** Form submission IS what creates the client record. This watcher is redundant.

**Workflow:** SmartSuite → Video Watcher `[o6A12htwZffpOkbu]` — **OFF (broken)**
- 🐛 BUG: References `ob_videos_received` on Clients app — field doesn't exist
- **Fix needed:** Should check `step_videos_received` on the Onboarding app (value "3" = Complete)

**Workflow:** Client Nudge — Form & Video Reminders `[fdUdIRGsBq0HB4jA]` — **OFF (broken)**
- 🐛 BUG: References both `ob_form_submitted` and `ob_videos_received` — neither exists
- **Fix needed:** Remap to Onboarding app. Check `step_videos_received` for video nudge. For form nudge, check if onboarding record exists and `onboarding_stage` = "1" (Access Setup).

---

### STEP 4: Onboarding Progression
**What happens:** n8n periodically checks all onboarding records, detects completed steps, advances the stage.

**Workflow:** Onboarding Progression — Checkbox Done → Next Task `[NFU4jyVpaRSKv4Mj]` — **ON**
- Schedule Trigger
- Check Onboarding Progress — 101-line code node, reads all 17 step_ fields
- Has Updates? — If yes, notify #operations

**Note:** This workflow references 17 step_ fields (correct slugs). No `ob_` bug. It reads AND writes to the Onboarding app.

---

### STEP 5: Prerequisites Met → Campaign Build Task Created
**What happens:** When all prerequisites are complete (access, videos, audiences), n8n creates a campaign build task for the VA.

**Workflow:** Prerequisites Met → Auto-Create Campaign Build Task `[uDdwyIl7VDFEWJ8N]` — **ON**
- Schedule Trigger
- Check Prerequisites — queries Onboarding app
- Has Ready Clients? → Notify #operations

---

### STEP 6: VA Builds Campaign (Manual — Follows SOP_05)
**What happens:** VA gets the task, follows the Campaign Build SOP step by step.

**No automation here.** VA works in Ads Manager + SmartSuite manually:
1. Opens campaign record (Status = Draft)
2. Confirms setup info (client, market, campaign type, budget, scripts)
3. Builds campaign in Ads Manager following naming conventions
4. Fills in campaign record fields
5. Completes QA checklist (9 checks including Special Ad Category = Housing)
6. Changes status to QA Ready

**SOP:** SOP_05_Campaigns.md — exists in Agency OS/SOPs folder. **Not yet posted to Slack.**

---

### STEP 7: QA Check
**What happens:** n8n detects QA Ready status and posts the QA checklist to Slack.

**Workflow:** Campaign QA Ready → Slack Checklist `[IHEmXUHvz1T034lF]` — **ON**
- Schedule Trigger
- Find QA Ready campaigns
- Post QA checklist to Slack

---

### STEP 8: Campaign Launched → Client Notified
**What happens:** After QA passes, campaign goes live. n8n detects the launch and notifies the client.

**Workflow:** Campaign Launch → Notify Client in Slack `[9jGs4HGdijkyYB4f]` — **OFF (fixed, needs reactivation)**
- Schedule Trigger (midnight)
- Find Newly Launched Clients — queries Onboarding app where `step_campaign_launched` = "3" AND `step_launch_notification_sent` ≠ "3"
- Message Client Channel — sends "Your campaigns are now live!" to client's Slack channel
- Mark Notification Sent — updates `step_launch_notification_sent` to "3"

**Bugs found and fixed:**
- `ob_campaign_launched` → `step_campaign_launched` ✅
- `ob_launch_notification_sent` → `step_launch_notification_sent` ✅
- `value:true` → `value:"3"` ✅

---

## Supporting Workflows (Always Running)

| Workflow | ID | Status | What It Does |
|---|---|---|---|
| Daily Ops Briefing — 8am | ey0cuADK27ntvgMe | ON | Morning summary to Andrew |
| Stale Record Detector | lUl2nkA0Bo1k8nbv | ON | Flags records that haven't been updated |
| Task Assigned → Slack + Complete → Confirm | D4AvztGc4RCYyE5g | ON | Notifies VA of new tasks, confirms completion |
| Task Blocked → DM Andrew | ra2F0R9zrKMmGEvE | ON | Alerts Andrew when VA marks a task as blocked |
| Creative Fatigue Alert (28-Day Check) | OmtNWq7oETDUAjni | ON | Flags ads running 28+ days without creative swap |
| Windsor AI → SmartSuite Metrics (12h) | ZwXd0unFysJjWl1M | ON | Pulls ad performance metrics every 12 hours |
| CPL Threshold Alert → DM Andrew | gRzeR9zO9xbHMvXG | ON | Alerts when cost per lead exceeds threshold |
| Decision Router — Cut/Retarget/Lead Ad/Keep | iM5CNWHLS2UIIJ34 | ON | Auto-flags optimization decisions |
| 72hr Review Trigger | VTiPgz0Zem8jiOYx | ON | Creates review task 72hrs after campaign launch |
| Close CRM → SmartSuite Conversation Tracker | Gly17Kkp8oUTEyGp | ON | Syncs conversations from Close |
| Close CRM → SmartSuite Pipeline Sync | R4mXe... | ON | Syncs pipeline deals from Close |

---

## Bug Summary

| # | Workflow | Bug | Status |
|---|---|---|---|
| 1 | Campaign Launch | `ob_` prefix + boolean `true` instead of `"3"` | ✅ Fixed, saved, deactivated |
| 2 | Client Nudge | `ob_form_submitted` + `ob_videos_received` don't exist | ❌ Deactivated, needs remap |
| 3 | Video Watcher | `ob_videos_received` doesn't exist | ❌ Deactivated, needs remap |
| 4 | Form Submitted Watcher | `ob_form_submitted` doesn't exist | ❌ Deactivated — likely redundant |
| 5 | Ritsel Notes record | All 18 steps set to "3" (Complete) | ✅ Reset to "1" (Not Started) |
| 6 | Onboarding record creation | No workflow creates the record | ❓ Gap — needs resolution |

---

## SOPs Status

8 SOP markdown files exist in Agency OS/SOPs/:

| SOP | File | Status |
|---|---|---|
| SOP 01 — Pipeline | SOP_01_Pipeline.md | ✅ Written, in folder |
| SOP 02 — Conversation Tracker | SOP_02_Conversation_Tracker.md | ✅ Written, in folder |
| SOP 03 — Clients | SOP_03_Clients.md | ✅ Written, in folder |
| SOP 04 — Onboarding | SOP_04_Onboarding.md | ✅ Written, in folder |
| SOP 05 — Campaigns | SOP_05_Campaigns.md | ✅ Written, in folder |
| SOP 06 — Tasks | SOP_06_Tasks.md | ✅ Written, in folder |
| SOP 07 — Optimization | SOP_07_Optimization.md | ✅ Written, in folder |
| SOP 08 — Finance | SOP_08_Finance.md | ✅ Written, in folder |

**Not yet posted to Slack.** The Campaign Build SOP (SOP_05) is the most critical for VAs and needs to be in #team-tasks as a pinned Canvas so VAs can follow it step-by-step during campaign builds.

Additional SOP files (legacy DOCX format): Client_Facebook_Campaign_SOP_FINAL.docx, VA_Operating_Guide.docx, VA_Optimization_SOP.docx, Agency_OS_Automation_Guide.docx, Facebook setup guides (PDF + DOCX).
