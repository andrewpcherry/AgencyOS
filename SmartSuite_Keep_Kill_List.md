# SmartSuite Keep / Kill List

**Date:** 2026-04-17
**Purpose:** Every custom field in every app, with a verdict: KEEP (used by n8n workflow or essential for VA/Andrew), KILL (not referenced by any workflow, no clear purpose), or DECIDE (Andrew's call).
**Source:** Field-to-workflow map built from all 21 active n8n workflows + spec review.

**Rule:** If a field isn't read or written by any n8n workflow AND isn't essential for manual VA/Andrew use, it dies.

---

## App 1: PIPELINE (24 fields in spec)

Pipeline is synced from Close CRM. Andrew is the only user.

| # | Field | Type | Used By Workflow? | Verdict | Reason |
|---|-------|------|-------------------|---------|--------|
| 1 | Deal Name | Text | Close CRM Sync | **KEEP** | Primary field, sync key display |
| 2 | Company Name | Text | Close CRM Sync | **KEEP** | Flows into Client record on Won |
| 3 | Contact Name | Text | Close CRM Sync | **KEEP** | Flows into Client record on Won |
| 4 | Contact Email | Email | Close CRM Sync | **KEEP** | Flows into Client record on Won |
| 5 | Contact Phone | Phone | Close CRM Sync | **KEEP** | Flows into Client record on Won |
| 6 | Contact LinkedIn | Text | No | **KILL** | Not synced, not used anywhere |
| 7 | Stage | Dropdown | Close CRM Sync | **KEEP** | Core pipeline tracking |
| 8 | Deal Value | Currency | Close CRM Sync | **KEEP** | Revenue tracking |
| 9 | Expected Close Date | Date | No | **KILL** | Not used by any workflow. Close CRM has its own close date tracking |
| 10 | Health Status | Dropdown | No | **KILL** | Andrew never asked for this. No workflow reads/writes it |
| 11 | Probability % | Percent | No | **KILL** | Andrew never asked for this. No workflow reads/writes it |
| 12 | Next Action | Text | No | **KILL** | Not used by any workflow. Andrew tracks next actions in Close CRM |
| 13 | Next Action Date | Date | No | **KILL** | Same — Close CRM is the action tracker, not SmartSuite |
| 14 | Owner | Text | No | **KILL** | Andrew is the only salesperson. No workflow uses this |
| 15 | Stage Changed Date | Date | No | **KILL** | No workflow reads this. Close CRM tracks stage history natively |
| 16 | Close Reason | Text | No | **KILL** | Not used by any workflow |
| 17 | Notes | Rich Text | No | **KEEP** | Andrew's manual notes — lightweight, useful |
| 18 | ICP Score | Number | No | **KILL** | Andrew never asked for this. No workflow reads/writes it |
| 19 | Close Deal ID | Text | Close CRM Sync | **KEEP** | Sync key — critical |

**Pipeline summary:** KEEP 9, KILL 10

### Pipeline VIEWS

| View | Verdict | Reason |
|------|---------|--------|
| Active Deals | **KEEP** | Core view — non-closed stages |
| Won/Lost | **KEEP** | Reference view |
| View 3? | **DECIDE** | Andrew saw 4 views — need to identify and kill extras |
| View 4? | **DECIDE** | Same — any view not matching Active Deals or Won/Lost = KILL |

---

## App 2: CONVERSATION TRACKER (8 fields in spec)

No n8n workflow reads or writes Conversation Tracker. It's Andrew's manual tracking tool synced from Close CRM activities.

| # | Field | Type | Used By Workflow? | Verdict | Reason |
|---|-------|------|-------------------|---------|--------|
| 1 | Title | Text | Close CRM Sync | **KEEP** | Primary field |
| 2 | Company | Text | Close CRM Sync | **KEEP** | Context |
| 3 | Decision Maker | Text | Close CRM Sync | **KEEP** | Who Andrew spoke to |
| 4 | Date | Date | Close CRM Sync | **KEEP** | When |
| 5 | Outcome | Dropdown | Close CRM Sync | **KEEP** | Result of conversation |
| 6 | Notes | Text | Close CRM Sync | **KEEP** | Details |
| 7 | Close Activity ID | Text | Close CRM Sync | **KEEP** | Sync key |
| 8 | Call Booked | Yes/No | Close CRM Sync | **KEEP** | Outcome flag |

**Conversation Tracker summary:** KEEP 8, KILL 0. This app is clean.

---

## App 3: CLIENTS (~31 fields after earlier cleanup, spec says target ~25)

Clients is heavily referenced by workflows — it's the central record that Onboarding, Campaigns, Tasks all link back to.

### Fields workflows actively USE:
- client_status (read by multiple workflows for active/paused filtering)
- slack_channel (Slack notification workflows)
- drive_folder (referenced in onboarding/campaign builds)
- ad_account / client_ad_account_id (campaign builds, Windsor sync)
- business_portfolio (onboarding checks)
- facebook_page (onboarding checks, campaign builds)
- instagram (onboarding checks)
- contact_name, contact_email, contact_phone (client comms, Deal Won creation)
- company_name / business_name (primary field, used everywhere)
- link_to_onboarding (onboarding workflows)
- link_to_campaigns (campaign workflows)
- link_to_tasks (task workflows)
- month (finance/reporting)
- niche (content targeting)
- market_region (campaign targeting)
- monthly_ad_budget (campaign setup)
- assigned_va (task routing)
- owner_name (client comms)
- notes (manual reference)

### Fields with OPEN QUESTIONS from spec (the "CONFIRM WITH ANDREW" items):

| # | Field | Type | Used By Workflow? | Verdict | Reason |
|---|-------|------|-------------------|---------|--------|
| 1 | Seller Contact Number | Text | No | **KILL** | No workflow uses it. Unclear purpose — if needed, it's in the client's CRM |
| 2 | Client Direct Phone | Text | No | **KILL** | Duplicate of Contact Phone |
| 3 | Email (duplicate) | Email | No | **KILL** | Duplicate of Contact Email |
| 4 | Overdue Actions | Rollup | No | **KILL** | No workflow writes/reads. Dashboard noise |
| 5 | Next Action | Rollup | No | **KILL** | No workflow writes/reads. Dashboard noise |
| 6 | Winners | Rollup | No | **KILL** | No workflow writes/reads |
| 7 | Slack Channels Created | Date | No | **KILL** | One-time event, no workflow checks this |
| 8 | Last Nudge Sent | Date | No | **KILL** | Client Nudge workflow is deactivated. Kill until reactivated |
| 9 | Audience Tasks Created | Yes/No | No | **KILL** | Audience phase removed Apr 13 |
| 10 | Creative Upload Tasks Created | Yes/No | No | **KILL** | No active workflow references this |
| 11 | Campaign Build Tasks Created | Yes/No | No | **KILL** | No active workflow references this |
| 12 | Welcome Sent | Yes/No | No | **KILL** | No active workflow references this |
| 13 | Anything Else We Should Know | Rich Text | No | **DECIDE** | From onboarding form — may want to keep for context. Not used by any workflow |
| 14 | Business Portfolio ID | Text | Yes — Onboarding checks | **KEEP** | Used by onboarding progression |
| 15 | Drive Folder URL | Text | Yes | **KEEP** | Referenced in campaign/onboarding workflows |
| 16 | Slack Channel ID | Text | Yes — all Slack notifications | **KEEP** | Critical for all client Slack comms |
| 17 | Ad Acct ID | Text | Yes — Windsor sync, campaign builds | **KEEP** | Critical |

**Clients summary:** ~12 fields to KILL, 1 DECIDE, rest KEEP.

---

## App 4: ONBOARDING (App ID: 69db909cd9114601cccb2b57)

Every step field is actively used by the Onboarding Progression workflow and Onboarding Health Monitor.

| # | Field | Used By Workflow? | Verdict | Reason |
|---|-------|-------------------|---------|--------|
| 1 | Client Name (Title) | Yes | **KEEP** | Primary field |
| 2 | Client (linked) | Yes | **KEEP** | Links to Clients app |
| 3 | Onboarding Stage | Yes — Health Monitor, Progression | **KEEP** | Core status |
| 4 | Onboarding Notes | No | **KEEP** | Manual context — lightweight |
| 5 | Blocker Notes | Yes — Health Monitor | **KEEP** | Surfaced in health alerts |
| 6-24 | All 19 step_* fields | Yes — Progression + Health Monitor | **KEEP** | Core automation |
| 25 | step_audience_* fields (7) | STALE — referenced by old Progression code | **KILL** | Audience phase removed Apr 13. Workflow code referencing these needs cleanup |

**SmartSuite default fields auto-created:**
| Field | Verdict | Reason |
|-------|---------|--------|
| Description | **HIDE** | Duplicate of Onboarding Notes |
| Assigned To | **HIDE** | n8n manages this, not manual assignment |
| Status | **HIDE** | Duplicate of Onboarding Stage |
| Due Date | **HIDE** | No workflow uses a due date for onboarding |
| Priority | **HIDE** | No workflow uses priority for onboarding |

**Onboarding summary:** KEEP all 24 core fields, KILL 7 stale audience fields, HIDE 5 default fields.

---

## App 5: CAMPAIGNS (App ID: 69ce678977bf866e34b46f68)

Heavily used by Campaign Intelligence Agent, Windsor AI sync, QA workflows, and VA build process.

### Fields workflows actively USE:
campaign_type, funnel_stage, status, launch_date, spend, thruplays, cost_per_thruplay, saves, comments, dms, leads, market, all 9 qa_* fields, platform_campaign_id, last_pull_date, campaign_record_name, client (linked), daily_budget, campaign_name, ad_set_name, ad_name, script_link, asset_link, week, owner, link_to_tasks, link_to_reviews, build_sop_reference, client_launch_notified

### Fields to KILL:

| # | Field | Type | Used By Workflow? | Verdict | Reason |
|---|-------|------|-------------------|---------|--------|
| 1 | Script Key | Lookup | No — from deleted Scripts app | **KILL** | Scripts app deleted. Lookup is broken |
| 2 | Bucket | Lookup | No — from deleted Scripts app | **KILL** | Same |
| 3 | Topic / Scenario | Lookup | No — from deleted Scripts app | **KILL** | Same |
| 4 | Version Number | Lookup | No — from deleted Scripts app | **KILL** | Same |
| 5 | Owner (Legacy) | User field | No | **KILL** | Replaced by Owner dropdown |
| 6 | 50% Views | Number | No | **DECIDE** | Windsor could populate, but no workflow currently does. Keep if Windsor sync is planned |
| 7 | 75% Views | Number | No | **DECIDE** | Same |
| 8 | 95% Views | Number | No | **DECIDE** | Same |
| 9 | Shares | Number | No | **DECIDE** | Same |
| 10 | Cost / Lead | Currency | No | **DECIDE** | Same |
| 11 | Winner Reviews (Helper) | Count | No | **KILL** | No workflow uses this |
| 12 | Next Action Date | Due Date | No | **KILL** | Tasks app handles action dates, not Campaigns |

**Campaigns summary:** KILL 7 outright, 5 DECIDE (all Windsor metrics — keep if Windsor sync will populate them, kill if not).

---

## App 6: TASKS (24 fields, spec says "already clean")

| # | Field | Used By Workflow? | Verdict | Reason |
|---|-------|-------------------|---------|--------|
| 1 | Task | Text | Yes | **KEEP** | Primary field |
| 2 | Client | Linked Record | Yes | **KEEP** | Links to client |
| 3 | Campaign | Linked Record | Yes | **KEEP** | Links to campaign |
| 4 | Type | Dropdown | Yes | **KEEP** | 15 task types used by task creation workflows |
| 5 | Status | Dropdown | Yes | **KEEP** | Core — read by multiple workflows |
| 6 | Priority | Dropdown | Yes | **KEEP** | Task routing |
| 7 | Assigned To | User | Yes | **KEEP** | VA assignment |
| 8 | Due Date | Date | Yes | **KEEP** | Task scheduling |
| 9 | Blocker Reason | Dropdown | Yes | **KEEP** | Used by blocked-task workflows |
| 10 | Notes | Rich Text | No | **KEEP** | VA working notes |
| 11 | Funnel Stage | Dropdown | Yes | **KEEP** | Referenced by task workflows |

**Tasks summary:** All fields KEEP. This app is clean.

### Tasks VIEWS — NEED AUDIT

| View | Verdict | Reason |
|------|---------|--------|
| My Queue | **KEEP** | VA's home screen |
| Blocked | **KEEP** | Blocked task visibility |
| Done This Week | **KEEP** | VA progress tracking |
| Any extras? | **DECIDE** | Andrew flagged views that "don't look obvious" — need to check |

---

## App 7: OPTIMIZATION (30 fields, spec says "NEEDS FULL AUDIT")

Workflows reference: next_review, review_date, status, funnel_stage

| # | Field | Used By Workflow? | Verdict | Reason |
|---|-------|-------------------|---------|--------|
| 1 | Review title/name | Text | Yes | **KEEP** | Primary field |
| 2 | Status | Dropdown | Yes | **KEEP** | Core |
| 3 | Funnel Stage | Dropdown | Yes | **KEEP** | TOF/MOF/BOF context |
| 4 | Review Date | Date | Yes — but mislabeled "Launch Date" | **KEEP + FIX LABEL** | Rename to "Review Date" |
| 5 | Next Review Date | Date | Yes — but mislabeled "72hr Review Date" | **KEEP + FIX LABEL** | Rename to "Next Review Date" |
| 6 | Campaign (linked) | Yes | **KEEP** | Links to campaign being reviewed |
| 7 | Client (linked) | Yes | **KEEP** | Links to client |
| 8-30 | Remaining ~23 fields | Unknown | **AUDIT NEEDED** | Optimization has 30 fields but spec doesn't list them all. Need API pull to identify and verdict each one |

**Optimization summary:** Core 7 fields KEEP (2 need label fixes), remaining ~23 need live API audit before verdict.

### Optimization VIEWS — NEED AUDIT

| View | Verdict | Reason |
|------|---------|--------|
| Pending Reviews | **KEEP** | Core view |
| Decision Log | **KEEP** | History |
| Any extras? | **DECIDE** | Andrew flagged these views too |

---

## App 8: FINANCE (17 fields)

No n8n workflow currently reads/writes Finance. It's Andrew's manual tracking.

**Verdict: KEEP ALL.** Every field is standard accounting (title, record type, amount, month, invoice date, payment status, etc.). Nothing redundant, nothing broken. Spec says "No changes needed."

---

## SOP LINKS — NOT YET ADDED

Andrew confirmed SOP links should live in SmartSuite. They're currently missing from every app. After the keep/kill cleanup, add:

| App | Field to Add | Content |
|-----|-------------|---------|
| Campaigns | Build SOP Reference (exists) | Populate with link to Campaign Build SOP |
| Onboarding | SOP Link (new field or use Notes) | Link to Onboarding SOP |
| Tasks | SOP Link (new field or use Notes) | Link to VA Task SOP |

---

## EXECUTION STATUS — COMPLETED 2026-04-17

All changes executed and verified via API audit.

### Fields
- **Pipeline:** 10 fields hidden via API ✅
- **Clients:** 12 kill targets already removed, 3 additional hidden ✅
- **Onboarding:** 5 default fields hidden, stale audience fields already gone ✅
- **Campaigns:** 5 fields already deleted, 1 hidden (due_date), Script lookups already gone ✅
- **Optimization:** All 30 fields verified purposeful, labels already fixed ✅
- **Tasks:** All fields kept, clean ✅
- **Conversation Tracker:** All 8 fields kept, clean ✅
- **Finance:** All 17 fields kept, clean ✅

### Views Deleted
- Pipeline: Pipeline Board, Needs Attention
- Campaigns: Performance, By Funnel Stage
- Tasks: Task Board, By Category
- Optimization: By Decision
- Clients: Client Board
- Onboarding: Onboarding Board

### Final View Counts
- **Pipeline:** Active Deals, Won/Lost (2)
- **Clients:** Dashboard, Active Clients, Client Onboarding Form (3)
- **Onboarding:** Checklist (1)
- **Campaigns:** Build Queue, QA Ready, Live, All Campaigns (4)
- **Tasks:** My Queue, Blocked, Done This Week (3)
- **Optimization:** Pending Reviews, Decision Log (2)
- **Conversation Tracker:** Active, Calls Booked, By Outcome (3)
- **Finance:** All Records, Monthly Costs, P&L by Month, Unpaid, Revenue (5)

### Apps Deleted (7 of 10 extras)
Deleted via API: Content Calendar, Creative Assets, Scripts, SOPs, Reporting, Ad Sets, Audiences

### Andrew's 6 Decisions — ALL KEEP
1. Clients → "Anything Else We Should Know" → **KEEP**
2. Campaigns → 50% Views → **KEEP**
3. Campaigns → 75% Views → **KEEP**
4. Campaigns → 95% Views → **KEEP**
5. Campaigns → Shares → **KEEP**
6. Campaigns → Cost / Lead → **KEEP**

### API Verification (field counts from live audit)
| App | Visible | Hidden | Total |
|-----|---------|--------|-------|
| Pipeline | 14 | 10 | 24 |
| Clients | 29 | 3 | 32 |
| Onboarding | 28 | 6 | 34 |
| Campaigns | 50 | 3 | 53 |
| Tasks | 20 | 1 | 21 |
| Optimization | 30 | 0 | 30 |
| Conversation Tracker | 12 | 0 | 12 |
| Finance | 17 | 1 | 18 |

### Still Manual (Andrew)
- Delete RequityAI Finance solution (Financial Metrics Dashboard is last app — API can't delete)
- Teams and Members are system apps — hide from nav if possible
- Delete 4 false "campaigns are live" Slack messages

### Still TODO
- Add SOP links to SmartSuite (Campaigns, Onboarding, Tasks)
- n8n cleanup: Remove stale step_audience_* references from Onboarding Progression workflow
