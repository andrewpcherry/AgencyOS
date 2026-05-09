# AgencyOS — SmartSuite Structure Spec

**Date:** 2026-04-17 (updated from 2026-04-12 draft)
**Status:** VERIFIED — API-audited April 17, 2026. All 8 core apps confirmed.
**Principle:** A VA loads SmartSuite and knows exactly what to do. Everything else is automated.

---

## System Overview

The VA's job is to **build campaigns** and **monitor**. Everything else — onboarding progression, metric tracking, optimization decisions — is automated by n8n + Windsor AI.

SmartSuite serves three purposes:
1. **Where the VA works** — Tasks (queue) and Campaigns (what they build)
2. **Where n8n writes** — Onboarding status, metrics, optimization flags
3. **Where Andrew monitors** — Dashboard views across everything

---

## App Architecture (8 Apps)

| # | App | Purpose | Primary User | Populated By |
|---|-----|---------|-------------|-------------|
| 1 | Pipeline | Sales deals before they become clients | Andrew | Andrew / Close CRM sync |
| 2 | Conversation Tracker | Active conversation tracking | Andrew | Andrew |
| 3 | Clients | Client info — who they are, their details | Andrew / VA | Onboarding form + n8n |
| 4 | Onboarding | The gate — every step before campaigns can be built | n8n (auto) | n8n auto-updates each step |
| 5 | Campaigns | Building + running campaigns | VA builds, n8n tracks metrics | VA + Windsor AI via n8n |
| 6 | Tasks | VA work queue | VA | n8n creates tasks, VA works them |
| 7 | Optimization | Review cycles + rule-based decisions | n8n flags, Andrew reviews | Windsor AI metrics via n8n |
| 8 | Finance | Money in, money out | Andrew | Andrew / n8n |

**APPS TO DELETE:**
- Scripts → content lives in Google Drive, link field on Campaign
- Creative Assets → content lives in Google Drive, link field on Campaign

---

## App 1: Pipeline

**Purpose:** Track sales deals from first conversation to close.
**Primary user:** Andrew
**No changes needed** — current structure is clean.

### Pipeline Stages (from Close CRM — "Real Estate Investor" pipeline)
| Stage | Type | Notes |
|-------|------|-------|
| Conversation - Positive | Active | Initial positive interest |
| Follow Up / Reschedule | Active | Needs follow-up or rebook |
| Booked | Active | Call scheduled |
| No Show | Active | Didn't show up |
| Cancelled | Active | Cancelled call |
| Proposal - Decision - Pending | Active | Proposal sent, waiting on decision |
| Ghosted | Active | Gone silent |
| Signed - Invoice Sent | Active | Deal signed, invoice out |
| Won | Won | Closed deal → triggers client creation |
| Lost | Lost | Dead deal |

### Fields (24)
| Field | Type | Notes |
|-------|------|-------|
| Deal Name | Text | Primary field |
| Company Name | Text | |
| Contact Name | Text | |
| Contact Email | Email | |
| Contact Phone | Phone | |
| Contact LinkedIn | Text | |
| Stage | Dropdown | Matches pipeline above |
| Deal Value | Currency | |
| Expected Close Date | Date | |
| Health Status | Dropdown | On Track / At Risk / Stalled |
| Probability % | Percent | |
| Next Action | Text | |
| Next Action Date | Date | |
| Owner | Text | |
| Stage Changed Date | Date | |
| Close Reason | Text | |
| Notes | Rich Text | |
| ICP Score | Number | |
| Close Deal ID | Text | Sync key from Close CRM |

### Views
- **Active Deals** — Grid filtered to non-closed stages, sorted by Next Action Date
- **Won/Lost** — Grid filtered to Won or Lost, for reference

---

## App 2: Conversation Tracker

**Purpose:** Track active conversations with prospects.
**Primary user:** Andrew
**No changes needed** — current structure is clean.

### Fields (12)
| Field | Type | Notes |
|-------|------|-------|
| Title | Text | Primary field |
| Company | Text | |
| Decision Maker | Text | |
| Date | Date | |
| Outcome | Dropdown | Interested / Maybe / Not Interested |
| Notes | Text | |
| Close Activity ID | Text | Sync key |
| Call Booked | Yes/No | |

### Views
- **Active** — Grid filtered to recent conversations

---

## App 3: Clients

**Purpose:** Client directory. Who they are, their details, their status. NOT onboarding (that's a separate app).
**Primary user:** Andrew + VA (reference only)

### Fields (CLEANED — target ~25 fields, down from 82)

**Core Client Info:**
| Field | Type | Notes |
|-------|------|-------|
| Business Name | Text | Primary field |
| Status | Dropdown | Onboarding / Active / Paused / Churned |
| Niche | Dropdown | REI / Notes / Other |
| Market / Region | Text | Geographic market |
| Contact Name | Text | *DELETE duplicate "Primary Contact Name"* |
| Contact Email | Email | |
| Contact Phone | Phone | |
| Owner Name | Text | Business owner's name |
| Monthly Ad Budget | Currency | *DELETE duplicate "Monthly Budget"* |
| Business Portfolio ID | Text | Meta Business Portfolio |
| Facebook Page URL | Text | |
| Instagram Handle | Text | |
| Ad Acct ID | Text | Slug: `client_ad_account_id` — Meta ad account ID |
| Drive Folder URL | Text | Link to Google Drive folder for this client |
| Assigned VA | Dropdown | Andrew / Operator / VA |
| Slack Channel ID | Text | For n8n Slack notifications |
| Notes | Rich Text | |

**Linked Records:**
| Field | Type | Notes |
|-------|------|-------|
| Link to Onboarding | Linked Record | NEW — link to Onboarding app |
| Link to Campaigns | Linked Record | Existing |
| Link to Tasks | Linked Record | Existing |

**Rollup / Computed (Andrew dashboard):**
| Field | Type | Notes |
|-------|------|-------|
| Live Campaigns | Count | From linked Campaigns |
| Open Tasks | Count | From linked Tasks |
| Total Revenue | Rollup | From Finance |

**FIELDS TO DELETE FROM CLIENTS:**
- All 14 OB: fields (moved to Onboarding app)
- All 17 Setup: fields (moved to Onboarding app)
- Yes / No (orphan)
- Yes / No 1 (orphan)
- Text Area (unnamed orphan)
- Meta Ads App Installed (broken — has Client Status choices)
- Property Situations of Interest (broken — has Niche choices)
- Primary Contact Name (duplicate of Contact Name)
- Monthly Budget (duplicate of Monthly Ad Budget)
- Market (duplicate of Market / Region)
- Due Date (not relevant for a client record)
- Assigned VA (Legacy) (old user field, replaced by dropdown)
- Scripts (linked record — Scripts app being deleted)
- Seller Contact Number (unclear purpose — *CONFIRM WITH ANDREW*)
- Client Direct Phone (duplicate of Contact Phone — *CONFIRM WITH ANDREW*)
- Email (duplicate of Contact Email — *CONFIRM WITH ANDREW*)
- Overdue Actions (rollup — *KEEP or DELETE?*)
- Next Action (rollup — *KEEP or DELETE?*)
- Winners (rollup — *KEEP or DELETE?*)
- Slack Channels Created (date field — *KEEP or DELETE?*)
- Last Nudge Sent (date — *KEEP or DELETE?*)
- Audience Tasks Created (yes/no — *KEEP or DELETE?*)
- Creative Upload Tasks Created (yes/no — *KEEP or DELETE?*)
- Campaign Build Tasks Created (yes/no — *KEEP or DELETE?*)
- Welcome Sent (yes/no — *KEEP or DELETE?*)
- Anything Else We Should Know (rich text — from onboarding form, *KEEP or MOVE?*)

### Views
- **Dashboard** — Grid showing all clients with status, live campaigns, open tasks
- **Client Onboarding Form** — KEEP (form that collects client info, stays on Clients app, triggers n8n to create Onboarding record)

**VIEWS TO DELETE:**
- Onboarding Board (moves to Onboarding app)
- Onboarding (moves to Onboarding app)
- New Client Onboarding (duplicate/redundant with Client Onboarding Form)
- All Clients (redundant with Dashboard)

---

## App 4: Onboarding (NEW)

**Purpose:** The gate. Every step that must be completed before campaigns can be built. n8n auto-updates each step. VA doesn't manually update these.
**Primary user:** n8n (writes), Andrew (monitors)
**App ID:** 69db909cd9114601cccb2b57

### Fields

**Core:**
| Field | Type | Notes |
|-------|------|-------|
| Client Name | Text | Primary field — *needs rename from "Title" in UI* |
| Client | Linked Record | *Needs adding in UI* — link to Clients app |
| Onboarding Stage | Dropdown | Access Setup / Video Briefing / Awaiting Videos / Videos Received / Campaign Build / QA / Live |
| Onboarding Notes | Rich Text | |
| Blocker Notes | Rich Text | What's holding things up |

**Individual Steps (each is a 3-state dropdown: Not Started 🔴 / In Progress 🟠 / Complete 🟢):**

*Phase 1: Account Access*
| Field | Slug | What n8n checks |
|-------|------|-----------------|
| Business Portfolio Access | step_business_portfolio_access | VA has been granted access to client's Meta Business Portfolio |
| Ad Account Visible | step_ad_account_visible | Ad account appears in Business Manager |
| Facebook Page Confirmed | step_facebook_page_confirmed | Correct FB page identified and accessible |
| Instagram Connected | step_instagram_connected | IG account linked to FB page |
| Meta Ads App Installed | step_meta_ads_app_installed | Client has installed Meta Ads app on phone |

*Phase 2: Lead Setup*
| Field | Slug | What n8n checks |
|-------|------|-----------------|
| Leads Access Confirmed | step_leads_access_confirmed | Can access leads in the ad account |
| Lead Notifications Set | step_lead_notifications_set | Client receiving lead notifications |
| Lead Centre to CRM | step_lead_centre_to_crm | Leads flowing from Lead Centre to client's CRM |
| Lead Destination Confirmed | step_lead_destination_confirmed | Client confirmed where leads should go |
| FB Lead Centre Connected | step_fb_lead_centre_connected | Facebook Lead Centre is set up and connected |

*Phase 3: Videos*
| Field | Slug | What n8n checks |
|-------|------|-----------------|
| Video Brief Sent | step_video_brief_sent | Video requirements document sent to client |
| Videos Received | step_videos_received | Client has sent back their talking head videos |
| Videos Edited | step_videos_edited | Videos edited and ready for ads (added Apr 16) |
| Approved Videos Exist | step_approved_videos_exist | Videos reviewed and approved for ad use |

*~~Phase 4: Audience Build~~ — REMOVED Apr 13. Audiences are NOT created during onboarding. Campaign Intelligence Agent monitors TOF Video Views performance → creates "Create Retargeting Audiences" task for VA with specs (client, page, thresholds, lookback window) → VA executes in Ads Manager.*

*Phase 4: Campaign Launch*
| Field | Slug | What n8n checks |
|-------|------|-----------------|
| Campaign Built | step_campaign_built | Campaign created in Ads Manager |
| QA Passed | step_qa_passed | Campaign passed QA checklist |
| Campaign Launched | step_campaign_launched | Campaign set to live |
| Launch Notification Sent | step_launch_notification_sent | Client notified campaign is live |

*Master:*
| Field | Slug | What n8n checks |
|-------|------|-----------------|
| Onboarding Complete | step_onboarding_complete | All above steps = Complete |

### Views
- **Onboarding Board** — Kanban grouped by Onboarding Stage (Access Setup → Live)
- **Checklist** — Grid showing all clients with all step columns visible (wall of red/orange/green)

**DEFAULT SYSTEM FIELDS TO CLEAN UP:**
SmartSuite auto-created: Description, Assigned To, Status, Due Date, Priority. Consider hiding or removing these if they duplicate Onboarding Stage.

---

## App 5: Campaigns

**Purpose:** Everything about building and running campaigns. Scripts and creative assets referenced via Google Drive links.
**Primary user:** VA (builds), n8n + Windsor AI (writes metrics)
**App ID:** 69ce678977bf866e34b46f68

### Fields (CLEANED — current 53, target ~40-45)

**Core Campaign Info:**
| Field | Type | Notes |
|-------|------|-------|
| Campaign Record Name | Text | Primary field |
| Client | Linked Record | Link to Clients app |
| Market | Text | Geographic market |
| Campaign Type | Dropdown | Video Views / Retarget / Lead Ad (slug: `campaign_type`) |
| Funnel Stage | Dropdown | TOF / MOF / BOF (slug: `funnel_stage` — added Apr 17) |
| Market | Text | Geographic market (slug: `market` — added Apr 17) |
| Status | Dropdown | Draft / QA Ready / Live / Paused / Cut / Completed |
| Owner | Dropdown | VA / Operator |
| Week | Dropdown | W1–W13 |
| Daily Budget | Currency | |
| Launch Date | Date | |
| Campaign Name | Text | Naming convention for Ads Manager |
| Ad Set Name | Text | Naming convention |
| Ad Name | Text | Naming convention |

**Google Drive Links (NEW — replace Scripts/Creative Assets apps):**
| Field | Type | Notes |
|-------|------|-------|
| Script Link | URL | Link to script in Google Drive |
| Asset Link | URL | Link to video/creative in Google Drive |

**Metrics (populated by Windsor AI via n8n):**
| Field | Type | Notes |
|-------|------|-------|
| Platform Campaign ID | Text | Facebook campaign ID |
| Last Pull Date | Date | Last Windsor sync |
| Spend | Currency | |
| ThruPlays | Number | |
| Cost / ThruPlay | Currency | |
| 50% Views | Number | |
| 75% Views | Number | |
| 95% Views | Number | |
| Saves | Number | Key Hormozi metric — high saves = winning content |
| Shares | Number | |
| Comments | Number | |
| DMs | Number | |
| Leads | Number | |
| Cost / Lead | Currency | |

**QA Checklist (VA completes before launch):**
| Field | Type | Notes |
|-------|------|-------|
| QA: Correct Video Uploaded | Yes/No | |
| QA: Correct Page & IG Identity | Yes/No | |
| QA: Correct Geo/Market | Yes/No | |
| QA: Correct Budget Set | Yes/No | |
| QA: Naming Convention Matches | Yes/No | |
| QA: Special Ad Category = Housing | Yes/No | CRITICAL — legal requirement |
| QA: Placements Correct | Yes/No | |
| QA: CBO Off | Yes/No | |
| QA: CTA Correct | Yes/No | |

**Linked Records:**
| Field | Type | Notes |
|-------|------|-------|
| Link to Tasks | Linked Record | |
| Link to Reviews | Linked Record | Link to Optimization app |

**Lookups (from old Scripts/Creative Assets — REVIEW):**
| Field | Type | Notes |
|-------|------|-------|
| Script Key | Lookup | *May break when Scripts app deleted* |
| Bucket | Lookup | *May break when Scripts app deleted* |
| Topic / Scenario | Lookup | *May break when Scripts app deleted* |
| Version Number | Lookup | *May break when Scripts app deleted* |

**Other:**
| Field | Type | Notes |
|-------|------|-------|
| Build SOP Reference | Rich Text | |
| Client Launch Notified | Yes/No | |
| Winner Reviews (Helper) | Count | |
| Owner (Legacy) | User field | *DELETE — replaced by Owner dropdown* |
| Next Action Date | Due Date | |

### FIELDS TO DELETE:
- Owner (Legacy) — replaced by Owner dropdown
- Script Key, Bucket, Topic / Scenario, Version Number lookups — will break when Scripts app is deleted. Replace with text fields or remove if Google Drive links are sufficient.

### Views
- **All Campaigns** — Grid showing all campaigns with status, metrics
- **Build Queue** — Filtered to Draft status, what the VA needs to build
- **Live** — Filtered to Live status, with metrics columns visible
- **QA Ready** — Filtered to QA Ready, with QA checklist columns

---

## App 6: Tasks

**Purpose:** The VA's single work queue. n8n creates tasks, VA works them.
**Primary user:** VA

### Fields (24 — already clean after earlier fixes)
| Field | Type | Notes |
|-------|------|-------|
| Task | Text | Primary field |
| Client | Linked Record | |
| Campaign | Linked Record | |
| Type | Dropdown | 15 task types (already fixed) |
| Status | Dropdown | *Check current choices* |
| Priority | Dropdown | Urgent / High / Normal / Low (already fixed) |
| Assigned To | User | |
| Due Date | Date | |
| Blocker Reason | Dropdown | *Check current choices* |
| Notes | Rich Text | |
| + system fields | | |

### Views
- **My Queue** — Grid filtered to assigned VA, sorted by priority then due date. THIS IS THE VA's HOME SCREEN.
- **Blocked** — Filtered to blocked tasks
- **Done This Week** — Filtered to completed this week

---

## App 7: Optimization

**Purpose:** Review cycles for live campaigns. Windsor AI metrics in, rule-based decisions out.
**Primary user:** n8n (writes), Andrew (reviews)

### Current Fields (30) — NEEDS FULL AUDIT
*Known issues:*
- review_date labeled "Launch Date" — should be "Review Date"
- next_review_date labeled "72hr Review Date" — should be "Next Review Date"

**FUTURE:** This app will hold the rule-based optimization engine output:
- Kill rules: if spend > X with < Y views → flag for kill
- Scale rules: if CPL < Z → flag for budget increase
- Windsor AI brings in metrics, n8n applies rules, writes decisions here
- Andrew reviews and approves/overrides

### Views
- **Pending Reviews** — campaigns due for review
- **Decision Log** — history of optimization decisions and outcomes

---

## App 8: Finance

**Purpose:** Income and cost tracking.
**Primary user:** Andrew
**No changes needed** — current structure is clean.

### Fields (17)
| Field | Type | Notes |
|-------|------|-------|
| Title | Text | Primary field |
| Record Type | Dropdown | Setup Fee / Retainer / Bonus / VA Cost / Software Cost / Other Income / Other Cost |
| Amount | Currency | |
| Month | Dropdown | Jan 2026 – Dec 2026 |
| Invoice Date | Date | |
| Payment Status | Dropdown | Unpaid / Paid / Overdue / N/A |
| Payment Date | Date | |
| Payment Method | Dropdown | Wire / Stripe / PayPal / Cash / Other |
| Client | Linked Record | |
| Invoice Document | File | |
| Notes | Rich Text | |
| Description | Rich Text | |

### Views
- **All Records** — Grid, all finance records
- **Unpaid** — Filtered to Unpaid status

---

## CONFIRMED FUNNEL STRUCTURE (Apr 17, 2026)

| Stage | Campaign Type | Objective | CTA | Audience |
|-------|--------------|-----------|-----|----------|
| TOF | Video Views | Video Views | No button — ad copy says "comment OPTIONS" | Cold/broad (state or major metro) |
| MOF | Retarget | Engagement | No button — ad copy says "comment OPTIONS" (different video) | 25%/50% video viewers (auto-built from TOF) |
| BOF | Lead Ad | Leads | Facebook Lead Form (ONLY campaign that captures leads) | 75%/95% video viewers (auto-built from TOF) |

**No Facebook pixel required.** All lead capture is native Facebook Lead Forms. Retarget audiences auto-build from in-platform video view engagement.

**Audience creation:** NOT during onboarding. Campaign Intelligence Agent monitors TOF performance → creates "Create Retargeting Audiences" task with specs → VA executes in Ads Manager.

**Creative workflow:** Claude writes scripts → VA edits → Client sends raw videos to Raw Video folder → VA processes → moves to Ad Creative folder in Google Drive.

**CSV Import** is the primary campaign build method for duplicating across clients at scale.

---

## OPEN QUESTIONS FOR ANDREW

1. ~~**Campaign Type choices**~~ — **RESOLVED.** Video Views / Retarget / Lead Ad.

2. ~~**Funnel Stage on Campaigns**~~ — **RESOLVED.** TOF / MOF / BOF.

3. **Client fields to confirm deletion** — Seller Contact Number, Client Direct Phone, Email (duplicate?), Overdue Actions, Next Action, Winners (rollups), Slack Channels Created, Last Nudge Sent, various "Tasks Created" flags, Welcome Sent, "Anything Else We Should Know"

4. ~~**Optimization rules**~~ — **RESOLVED.** See companion document: `AgencyOS_Optimization_SOP.md`. Covers 72-hour review cycle, rule-based kill/scale thresholds calibrated for $50/day minimum spend.

5. **Nav bar order** — Should it be: Pipeline → Conversation Tracker → Clients → Onboarding → Campaigns → Tasks → Optimization → Finance? (Left-to-right = lifecycle order)

---

## IMPLEMENTATION STATUS (Updated Apr 17, 2026)

### Phase 1: SmartSuite Structure — COMPLETE
1. ✅ Onboarding app created with 19 step fields
2. ✅ Onboarding app configured — Client link added, Onboarding Stage dropdown, views created
3. ✅ Clients app cleaned — down to 31 fields, duplicates removed
4. ✅ Script Link + Asset Link added to Campaigns
5. ✅ Scripts app deleted
6. ✅ Creative Assets app deleted
7. ✅ Campaign Type choices set (Video Views / Retarget / Lead Ad)
8. ✅ Optimization app labels and decision choices configured
9. ✅ Funnel Stage (TOF/MOF/BOF) added to Campaigns (Apr 17)
10. ✅ Market field added to Campaigns (Apr 17)
11. ✅ Ad Acct ID field added to Clients (Apr 17)
12. ✅ step_videos_edited field added to Onboarding (Apr 16)
13. ✅ API audit verified all 8 core apps (Apr 17)

### Phase 2: n8n Rework — IN PROGRESS
- ✅ Deal Won → Create Client + Onboarding workflow rebuilt with correct 19 slugs
- ✅ Close CRM → Pipeline Sync active (12hr schedule)
- ✅ Campaign Intelligence Agent active
- ✅ Onboarding Progression active (needs step_videos_edited gate added)
- ✅ Prerequisites Met → Campaign Build Task active
- ⬜ Video Watcher — deactivated, needs slug remap
- ⬜ Client Nudge — deactivated, needs slug remap
- ⬜ Form Submitted Watcher — deactivated, needs slug remap
- ⬜ Campaign Launch → Notify Client — deactivated, needs testing
- ⬜ Windsor AI metric sync to Campaigns — not yet built
- ⬜ End-to-end test

### Phase 3: Client Deliverables (FUTURE)
- Send onboarding docs to new clients (Lead Center guide, Meta Ads app guide)
- Build optimization rule definitions with Andrew
