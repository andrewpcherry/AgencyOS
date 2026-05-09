# AgencyOS — Complete Architecture, A to Z

**Version:** 2026-04-26
**Owner:** Andrew Cherry (RequityAI)
**Purpose:** Single canonical description of what the agency does, the architecture that runs it, where the VA's hands are physical, and what the automations carry. Written so a brand-new operator (human or agent) can read this once and understand the whole stack end-to-end.

---

## A. WHAT THE AGENCY ACTUALLY DOES

**RequityAI is a Facebook ads agency.** The current niche is real-estate (REI / off-market deals), with the platform built so additional niches (Notes, Health, Construction, Other) can be plugged in by adding a row to a lookup table — not by rebuilding workflows.

The product the agency delivers per client is a 3-stage Facebook funnel running on the client's own Meta Business Portfolio:

| Stage | Campaign Type | Objective | CTA | Audience |
|---|---|---|---|---|
| TOF | Video Views | Video Views | "Comment OPTIONS" in copy | Broad — Special Housing category, no zip codes |
| MOF | Retarget | Engagement | "Comment OPTIONS" (different video) | Custom audience from TOF viewers (50/75/95%) |
| BOF | Lead Ad | Leads | FB Lead Form | Custom audience from MOF engagement |

Retargeting audiences are built **after launch**, not during onboarding — the Campaign Intelligence Agent watches video-view accumulation and creates a VA task to build them when thresholds are hit. No pixel needed.

The creative is **client-recorded talking-head video** following niche-specific scripts (REI today: 12 situation codes × 5 scripts = 60 scripts, code pattern `[SITUATION]-B[#]-[SCRIPT##]`). The client records → drops to Drive Raw Videos → VA edits → moves to Ad Creatives → builds in Ads Manager.

Optimization runs on a 72hr-then-7day loop driven by an LLM agent reading live campaign data and writing a decision back into SmartSuite, which a router then executes (Cut / Keep / Retarget / Swap Creative / Needs Review). No human in the loop unless decision = Needs Review.

**The whole point of AgencyOS:** Andrew is not the bottleneck. The VA executes the deterministic work, the agents do the cognition, and the automation layer carries every state change so nothing falls through.

---

## B. THE STACK — ONE LINE PER LAYER

| Layer | Tool | Role |
|---|---|---|
| Source of truth | **SmartSuite** (8 apps) | All deals, clients, onboarding state, campaigns, tasks, optimization records, finance |
| Automation runtime | **n8n Cloud** (`requityai.app.n8n.cloud`) | Every workflow, every webhook, every cron |
| Sales dialer | **Close CRM** | Calling only — NOT the SoT for deal stage |
| Scheduling | **Calendly** | Booking → fires `invitee.created` webhook into n8n |
| VA + client comms | **Slack** | Per-client channel pair + ops rollup + DMs to Andrew |
| Content storage | **Google Drive** | Videos, creative, scripts, onboarding docs (SmartSuite stores links only) |
| Ad metrics | **Windsor.ai** | FB Ads data → n8n → SmartSuite Campaigns |
| Intelligence | **Claude (Haiku 4.5)** | Campaign Intelligence Agent, Slack Ops Supervisor, Sync Agent |
| Builder/operator | **Cowork (this agent)** | Builds, debugs, ships against the stack via API |

**Architectural rule (locked):** content (videos, scripts, creative) lives in Drive. SmartSuite stores Drive URLs, not files. Killing the old Scripts/Creative apps was deliberate.

---

## C. THE 8 SMARTSUITE APPS (the data layer)

Source of truth for everything. Field slugs and IDs are documented in `AgencyOS_SmartSuite_Structure_Spec.md` — never guess them, the wrong slug silently writes nothing or wipes data.

| # | App | App ID | Role |
|---|---|---|---|
| 1 | Pipeline | `6908636826cfbf4238a34f31` | Every prospect deal, 7 stages (Booked → Engaged → Qualified → Proposal → Won / Lost / No Show). 24 fields. |
| 2 | Conversation Tracker | `69d92c38b801d747e74629d1` | Every Close call outcome, written by M2b polling. 12 fields. |
| 3 | Clients | `69ce5f18cb8a07430bfee02d` | Master record per client, status (Prospect → Active → Churned), niche, drive URL, slack channel ID. 31 fields. |
| 4 | Onboarding | `69db909cd9114601cccb2b57` | One record per client, 19 step_ dropdowns (3-state: Pending/In Progress/Complete), grouped into 4 phases. 34 fields. |
| 5 | Campaigns | `69ce678977bf866e34b46f68` | One record per live campaign, drives the optimization loop. 53 fields. |
| 6 | Tasks | `69ce67b3fec5b91842ebaf03` | Every VA work order. **VAs do not create tasks** — automations create them. 21 fields, 15 task types. |
| 7 | Optimization | `69ce67e01cc0855f89fee02e` | One record per campaign review cycle. Stores the agent's decision + execution state. 30 fields. |
| 8 | Finance | `69cee1623a5dd7f2078e4d93` | Setup fees + retainers, view "Unpaid". Andrew only — VAs don't touch. 18 fields. |

**Hard rules that have caused production bugs (non-negotiable):**

1. SmartSuite list filter inner key is `fields`, not `filters`. Wrong key silently returns ALL records. Has corrupted data twice.
2. Onboarding step_ dropdowns use **numeric index strings** ("1"/"2"/"3" = Pending/In Progress/Complete). Tasks/Campaigns status fields use string labels.
3. Link field format is plain URL string array `[url]`. Object format `{url, link_text}` returns 200 OK and silently wipes the field.
4. Email fields return arrays — extract with `Array.isArray(r.contact_email) ? (r.contact_email[0] || '') : (r.contact_email || '')`.
5. PUT endpoint is `change_field/` (trailing slash required).
6. Onboarding → Clients link slug is `client`, not `link_to_client`. Reverse direction is `link_to_onboarding`.

---

## D. THE n8n RUNTIME

- Instance: `https://requityai.app.n8n.cloud`
- API base: `https://requityai.app.n8n.cloud/api/v1/`
- Auth header: `X-N8N-API-KEY: <token>`
- Total active workflows: **21** (down from 28 after Apr 26 audit — 7 campaign-gated workflows deactivated until first campaign launches)
- Global error handler: `ePyAmNK7lpzoXPgo` — wired to every other workflow, DMs Andrew on any failure.

**Rules that have bitten before:**
- Never edit trigger nodes on an active workflow. **Deactivate → edit → save → reactivate.** Zombies hide in `staticData`.
- Never use `httpRequestWithAuthentication` in a Code node. Use HTTP Request node with credential, or `this.helpers.httpRequest` in Code.
- Quiet hours for client-facing notifications: 8am–6pm ET only.

---

## E. THE FULL CLIENT JOURNEY — END TO END

This is the spine of the whole agency. Read top to bottom.

```
PROSPECT BOOKS A CALL
  Andrew posts on LinkedIn / outbound / referral
  → Prospect lands on Calendly "Off Market Deal Flow Call"
  → invitee.created webhook fires
    → [M3 — automation] creates Pipeline record at deal_stage=Booked
       + writes close_lead_id by querying Close CRM by email
    → Calendly's own workflows fire: 24h reminder + 2h SMS reminder
    → If no-show: Andrew flips Pipeline to deal_stage=No Show
       → [M4 — automation] webhook fires Calendly /invitee_no_shows
         → Calendly auto-sends reschedule SMS + email

ANDREW RUNS THE CALL
  Andrew uses Close CRM to dial and run the call (Close = dialer ONLY)
  → Call outcome captured in Close
    → [M2b — automation] every 30 min M-F 8am–3:30pm ET, polls Close
       and writes the outcome into Conversation Tracker app

DEAL ADVANCES THROUGH PIPELINE
  Andrew updates Pipeline deal_stage in SmartSuite
  Stages: Booked → Engaged → Qualified → Proposal → Won / Lost / No Show

DEAL WON
  Andrew flips Pipeline.deal_stage = "Won"
  → SS Automation (manual setup outstanding) fires webhook to n8n
  → Fallback: 5-min poller catches it within 5 min
    → [M5 — automation] does ALL of the following atomically:
       - Creates SS Client record (with niche, defaulting to REI)
       - Creates SS Onboarding record linked to Client
       - Creates Slack #client-{slug} (public, client-facing)
       - Creates Slack #team-{slug} (private, internal)
       - Invites Andrew to both
       - Posts welcome message to #client-{slug} with 3 onboarding doc links:
           · FB Setup Guide (niche-agnostic)
           · FB Access / Partner Access Guide (niche-agnostic)
           · Video Script Library (niche-aware via SCRIPT_DOC_BY_NICHE map)
       - Posts VA action prompt to #team-{slug} with the client email
         and step-by-step single-channel-guest invite instructions
       - Posts summary to #team-operations
       - Writes Slack public channel ID to SS Client.slack_channel_id
       - Marks Pipeline.won_processed = true (idempotency flag)

  → [BegEckXSgXmVffX2 — automation] runs daily at 8am
       (was hourly until Apr 26 throttle):
       - Reads SS Clients with no drive_folder_url
       - Creates RequityAI/{Client Name}/ folder in Google Drive
       - Creates Raw Videos/ subfolder
       - Creates Ad Creatives/ subfolder
       - Writes Drive folder URL back to SS Client
       - Posts Drive folder link to #team-{slug}

VA INVITES CLIENT TO SLACK (manual — physical task)
  VA opens #client-{slug}, hits Members → Invite, enters client email,
  selects "Single-channel guest". Slack's external guest flow can't be
  automated on standard plans. The instruction post in #team-{slug}
  spells out the exact steps so the VA isn't guessing.

ONBOARDING — 4 PHASES, 19 STEPS, 3-STATE DROPDOWNS
  Tracked in SS Onboarding app. Dropdowns: 1=Pending, 2=In Progress, 3=Complete.
  VAs DO NOT manually flip these. n8n updates them. VA does the underlying work.

  PHASE 1 — ACCESS (5 steps)
    Business Portfolio Access (VA requests in Meta, client approves)
    Ad Account Visible (the account appears in VA's Business Manager)
    Facebook Page Confirmed (correct page identified, accessible)
    Instagram Connected (IG linked to FB page)
    Meta Ads App Installed (client installs on phone for lead notifications)

  PHASE 2 — LEADS (5 steps)
    Leads Access Confirmed (VA can see Lead Centre)
    Lead Notifications Set (client gets email/push on new leads)
    Lead Centre to CRM (leads flowing to client's CRM — GHL, sheet, etc.)
    Lead Destination Confirmed (client confirms where leads go)
    FB Lead Centre Connected (full Lead Centre setup confirmed)

  PHASE 3 — VIDEOS (4 steps)
    Video Brief Sent (Andrew or VA sends recording brief)
    Videos Received (client uploads to Drive Raw Videos)
    Videos Edited (VA edits, moves to Ad Creatives folder)
    Approved Videos Exist (review pass for ad use)

  PHASE 4 — CAMPAIGN LAUNCH (4 steps)
    Campaign Built (VA builds structure in Ads Manager per SOP_05)
    QA Passed (full QA checklist — including Special Ad Category = Housing)
    Campaign Launched (set to Active in Ads Manager)
    Launch Notification Sent (client notified in #client-{slug})

  Audience Phase REMOVED — retargeting audiences auto-build from Video Views
  campaign activity. Campaign Intelligence Agent monitors thresholds and
  creates a VA task when audiences should be built.

  WORKFLOWS THAT WATCH ONBOARDING:
    [Onboarding Progression NFU4jyVpaRSKv4Mj] — daily 8am, reads all step_ fields,
       advances onboarding_stage and posts to #team-operations on changes.
    [Onboarding Health Monitor CqesBe55FnP6oaxA] — daily 8:30am, blocked >5 days
       → DM Andrew + escalation task.
    [Form Watcher Zv2PYFdMiBDCLcZV] — daily, on form submission resolves
       team-{slug} channel at runtime, posts notification (was broken; fixed Apr 25).
    [Video Watcher o6A12htwZffpOkbu] — daily, new video upload → notify VA in team channel.
    [Client Nudge fdUdIRGsBq0HB4jA] — daily, overdue forms/videos → reminder in
       #client-{slug}.

PREREQUISITES MET
  When all access + videos complete:
    [Prerequisites Met → Auto-Create Campaign Build Task uDdwyIl7VDFEWJ8N]
       creates a "Build Campaign" task in SS Tasks for the VA.

CAMPAIGN BUILD (manual VA work — physical)
  VA follows SOP_05_Campaigns.md:
    1. Open campaign record (Status = Draft)
    2. Confirm setup (client, market, type, budget, scripts)
    3. Build in Ads Manager following naming convention
    4. Fill in campaign record fields
    5. Run 9-point QA checklist (incl. Special Ad Category = Housing)
    6. Flip campaign status to "QA Ready"

  → [Campaign QA Ready → Slack Checklist IHEmXUHvz1T034lF]
       posts the QA checklist to Slack for VA self-cert.
       VA confirms each line. Final OK → Andrew DM'd for go/no-go.

CAMPAIGN GOES LIVE
  VA flips campaign status to Live in Ads Manager and SS Campaigns.
  → [Campaign Launch → Notify Client 9jGs4HGdijkyYB4f]
       posts "Your campaign is live!" to #client-{slug},
       marks step_launch_notification_sent = "3".
  → Onboarding Progression sees launch_notification_sent complete
       → marks Onboarding record Complete + Client.status = Active.

OPTIMIZATION LOOP — runs forever until Cut
  +72 hours after launch:
    [72hr Review Trigger VTiPgz0Zem8jiOYx] creates Optimization record,
       status = Pending Review, linked to campaign.

  Every 12 hours:
    [Campaign Intelligence Agent 6TuDo3mqBZSBF667]
       - Pulls all Live campaigns from SS Campaigns
       - Builds prompt + lookup map (campaign → optimizationRecordId)
       - Calls Claude Haiku 4.5
       - Claude returns: CAMPAIGN_NAME | DECISION | REASONING
       - Valid decisions: Keep Running / Cut / Retarget / Swap Creative / Needs Review
       - Writes decision + reasoning to the matching Optimization record
       - DMs Andrew the summary

  Within minutes of decision being written:
    [Decision Router iM5CNWHLS2UIIJ34] sees decision populated +
       decision_notification_sent=false:
         Cut          → flip Campaign.status=Cut, create "Cut/Pause" task, Slack alert
         Keep Running → set next_review_date = +7 days, Slack alert
         Retarget     → create "Adjust Targeting" task, Slack alert
         Swap Creative → create "Swap Ad Creative" task, Slack alert
         Needs Review → create "Flag for Andrew Review" task, Slack alert
       Then sets decision_notification_sent=true to prevent double-fire.

  Continuous monitoring while live:
    [Windsor AI → SS Metrics ZwXd0unFysJjWl1M] — every 12h, FB Ads data
       hydrated into SS Campaigns metrics fields.
    [CPL Threshold Alert gRzeR9zO9xbHMvXG] — when CPL exceeds threshold, DM Andrew.
    [Creative Fatigue Alert OmtNWq7oETDUAjni] — at 28-day creative age, DM Andrew.

DAILY OPS LAYER (always running)
  [Daily Ops Briefing ey0cuADK27ntvgMe] — 8:00am ET → #team-operations
     open tasks, active clients, campaign anomalies.
  [Daily Sales Brief pa7I1FKd50TQRFrV] — 8:05am ET M-F → #team-operations
     Calls/Booked/C→B ratios Today/WTD/MTD + Pipeline snapshot.
  [Slack Ops Supervisor 5cdMtOByeZVRFS6H] — 8am + 8pm ET, monitors Slack ops health.
  [Stale Record Detector lUl2nkA0Bo1k8nbv] — flags records that haven't moved.
  [Global Error Handler ePyAmNK7lpzoXPgo] — DMs Andrew on any workflow failure.
```

---

## F. SLACK ARCHITECTURE — THE DISPATCH SURFACE

This is where the human (VA) and the automation talk to each other.

| Channel pattern | Purpose | Created by |
|---|---|---|
| `#client-{slug}` | External, client-facing — campaigns live, deliverables, onboarding docs | M5 on Won |
| `#team-{slug}` | Private, internal — VA + Andrew discussion for that client | M5 on Won |
| `#team-operations` (`C0AKWU4835E`) | Cross-client ops rollup — daily briefings, summaries, M5 notifications | Pre-existing |
| DM to Andrew | Errors, CPL alerts, fatigue alerts, blocked tasks, supervisor nudges | Various |

**Slack-driven automation:**
- `/done` slash command → `[ynGKEAco9U6Q0ShI]` marks the referenced task complete in SS Tasks.
- `/update` slash command → `[8tdPtQWO4qDKEjgq]` SmartSuite Sync Agent parses natural language updates and writes back.
- Task assignment in SS → `[D4AvztGc4RCYyE5g]` DMs the assignee in their team channel.
- Task marked Blocked in SS → `[ra2F0R9zrKMmGEvE]` DMs Andrew immediately.

**Decided NOT to build:** the `/book` Slack command. Andrew books prospects manually in Calendly, which fires the same downstream chain (M3 webhook → Pipeline). Zero capability lost, one less workflow to maintain.

**Slack credentials:**
- Bot token (hardcoded in M5 Code node): `xoxb-9815813665076-...`
- OAuth2 credential (used by scheduled workflows): `<REDACTED_SLACK_OAUTH2_CREDENTIAL>`
- Andrew's user ID: `U09Q94U58EM`

---

## G. GOOGLE DRIVE — THE CONTENT STORE

- Parent folder: `RequityAI` (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`)
- Per-client structure (auto-created by BegEckXSgXmVffX2):
  - `RequityAI/{Client Name}/`
  - `RequityAI/{Client Name}/Raw Videos/` — client uploads here
  - `RequityAI/{Client Name}/Ad Creatives/` — VA edits land here
- Onboarding docs folder: **RequityAI Onboarding Doc folder** — contains:
  - FB Setup Guide (niche-agnostic): `1erR8MZx_SiuEpqj5wyGPJE6d9I1Q53aB`
  - FB Access / Partner Access Guide: `18UTBCKYjrMC3ZJGS96xBgXaJm2Samusz`
  - Video Script Library — REI: `1G0J71V73QDFxRtqqF17vWH7KEjSforXE`

**Niche-aware script delivery:** SS Clients has a `priority` field (label: "Niche") with options REI=2 / Notes=3 / Health=4 / Construction=5 / Other=6. M5 reads niche on Won, looks up the script doc in the `SCRIPT_DOC_BY_NICHE` map, posts the right link. Adding a new niche = add the dropdown option in SS UI + add one line to the lookup. No rework.

---

## H. WHERE THE VA'S HANDS ARE PHYSICAL — THE FULL LIST

This is the answer to your direct question. Everything else is automated. Be ruthless about keeping this list short — every item here is leverage Andrew has not yet captured.

**1. Slack guest invite (per Won deal — ~2 min)**
Open #client-{slug} → Members → Invite → enter client email → "Single-channel guest". Slack API can't do external guest invites on standard plans. The instruction is auto-posted to #team-{slug} so it's prescriptive, not improvised.

**2. Meta Business Portfolio access requests (per client — Phase 1)**
The VA has to physically click in Meta Business Manager to request access to the client's Business Portfolio, ad account, FB page, IG account. Meta has no API for partner access requests on RequityAI's tier. The client then has to physically approve in their own Meta. This is a 2-sided manual flow.

**3. Lead Centre / CRM wiring (per client — Phase 2)**
VA configures the client's Lead Centre destination — flowing leads into GoHighLevel, a Google Sheet, or whatever CRM the client uses. Client-specific, no automation possible.

**4. Video editing (per client — Phase 3)**
VA pulls raw video from `Raw Videos/`, edits, drops finished asset into `Ad Creatives/`. Editor work is human craft. (Drive triggers — Video Watcher — fire automatically when files appear, so the VA gets a notification, but the editing itself is hands.)

**5. Campaign build in Ads Manager (per launch — Phase 4)**
Following SOP_05: build the campaign structure in Meta Ads Manager — naming convention, audiences, budget, creative attachment, copy paste, Special Ad Category = Housing. Meta's API has automation paths but the cost/complexity of going API-built isn't worth it at current scale. VA builds in UI.

**6. 9-point QA checklist (per launch — Phase 4)**
VA self-certs the QA checklist that Slack posts when campaign hits "QA Ready". The checks are physical inspections in Ads Manager. The Slack workflow drives the process; the inspections are the VA's eyes.

**7. Manual campaign launch + status flip (per launch)**
VA hits "Publish" in Ads Manager and flips SS Campaigns.status to Live. Notification firing is automated; the publish click is manual on purpose (last sanity check before going live with budget).

**8. Decision execution for non-trivial decisions (per loop)**
When the Decision Router creates a "Swap Creative" or "Adjust Targeting" task, the VA does the actual creative swap or targeting change in Ads Manager. The decision and the work order are automated; the hands are the VA's.

**9. Andrew's manual touchpoints (kept manual on purpose):**
- Booking calls in Calendly (Andrew runs sales — flips through Pipeline stages)
- Running the call in Close CRM
- Flipping Pipeline.deal_stage to Won (the trigger event)
- Approving Drive cleanup (test artifacts)
- One-time SS Automation setup in the SmartSuite UI (outstanding — see section L)
- Decision sign-off when agent returns "Needs Review"

**Everything else is the automation layer.** If you find yourself doing something repeatedly that isn't in this list, that's a candidate for the next workflow.

---

## I. WHAT THE AUTOMATIONS DO — THE FULL 21 ACTIVE WORKFLOWS

### Event-driven (webhooks — instant)

| Workflow | ID | Trigger | What it does |
|---|---|---|---|
| **M3 — Calendly → Pipeline** | `1LMmEYIxSQHsPZd1` | Calendly `invitee.created` | Creates/updates Pipeline at deal_stage=Booked, writes close_lead_id |
| **M2b — Close → ConvTracker** | `15VLgXsxSNGbJIdp` | 30min poll M-F (Close webhook is broken — bridge until fixed) | Pulls call outcomes → ConvTracker records |
| **M5 — Won → Full Client Setup** | `A31jYsKR3aETSusC` | Webhook (SS Automation pending) + 5-min fallback poll | The big atomic onboarding event — see section E |
| **M4 — No-Show Bridge** | `1g5RRCFJKwWSl5ru` | Webhook (SS Automation pending) + fallback | Fires Calendly `/invitee_no_shows` → reschedule SMS+email |
| **Slack /done router** | `ynGKEAco9U6Q0ShI` | Slack slash command | Marks SS Task complete |
| **SmartSuite Sync Agent** | `8tdPtQWO4qDKEjgq` | Slack /update slash command | Claude parses VA natural-language update → writes to SS |
| **Task Assigned → Slack** | `D4AvztGc4RCYyE5g` | SS Task created with assignee | DMs the assignee + posts in team channel |
| **Task Blocked → DM Andrew** | `ra2F0R9zrKMmGEvE` | SS Task marked blocked | DMs Andrew immediately |
| **Global Error Handler** | `ePyAmNK7lpzoXPgo` | n8n errorTrigger from any other workflow | DMs Andrew with payload + workflow ID |

### Schedule-driven (legitimate time-based)

| Workflow | ID | Schedule | What it does |
|---|---|---|---|
| **Daily Ops Briefing** | `ey0cuADK27ntvgMe` | 8:00am ET daily | Posts daily ops snapshot to #team-operations |
| **Daily Sales Brief** | `pa7I1FKd50TQRFrV` | 8:05am ET M-F | Calls/Booked/C→B ratios + Pipeline snapshot |
| **Onboarding Health Monitor** | `CqesBe55FnP6oaxA` | Daily 8:30am | Blocked ≥5 days → DM Andrew + escalation task |
| **Slack Ops Supervisor** | `5cdMtOByeZVRFS6H` | 8am + 8pm ET | Monitors Slack ops health |
| **Stale Record Detector** | `lUl2nkA0Bo1k8nbv` | Daily | Flags pipeline/client records that haven't moved |
| **Onboarding Progression** | `NFU4jyVpaRSKv4Mj` | Daily 8am | Reads all step_ fields, advances onboarding_stage, posts changes |
| **Prerequisites Met** | `uDdwyIl7VDFEWJ8N` | Daily 8am | All access+videos done → creates Campaign Build task |
| **Form Watcher** | `Zv2PYFdMiBDCLcZV` | Daily | Resolves team-{slug} dynamically, posts on form submission |
| **Video Watcher** | `o6A12htwZffpOkbu` | Daily | New Drive video → notify VA in team channel |
| **Client Nudge** | `fdUdIRGsBq0HB4jA` | Daily | Overdue form/video → reminder to client |
| **BegEckXSgXmVffX2 — Drive Folder Creator** | `BegEckXSgXmVffX2` | Daily 8am (was hourly) | New Client → Drive parent + 2 subfolders + URL writeback + Slack post |
| **Windsor AI → Metrics** | `ZwXd0unFysJjWl1M` | Every 12h | FB Ads data → SS Campaigns metrics |
| **Campaign Intelligence Agent** | `6TuDo3mqBZSBF667` | Every 12h | Claude analyzes Live campaigns, writes decisions to Optimization records |
| **Decision Router** | `iM5CNWHLS2UIIJ34` | Every 12h | Reads Optimization decisions, executes (Cut/Keep/Retarget/Swap/Review) |

### Deactivated until needed (campaign-gated — zero events to fire on)

| Workflow | ID | Reactivate when... |
|---|---|---|
| Campaign Launch → Notify Client | `9jGs4HGdijkyYB4f` | First campaign goes live |
| Campaign QA Ready → Checklist | `IHEmXUHvz1T034lF` | First campaign hits QA Ready |
| 72hr Review Trigger | `VTiPgz0Zem8jiOYx` | First campaign launches |
| CPL Threshold Alert | `gRzeR9zO9xbHMvXG` | First campaign live |
| Creative Fatigue Alert | `OmtNWq7oETDUAjni` | First campaign live |
| Windsor AI metrics ingestion (campaign-gated portion) | (within Windsor wf) | First campaign live |

These were deactivated in the Apr 26 audit — they were polling against empty data and burning 9,000+ executions/month. Reactivation is a one-click flip when the first campaign launches.

---

## J. THE OPTIMIZATION LOOP — THE INTELLIGENCE LAYER

This is the agent loop that runs the agency's optimization brain.

```
Campaign launched (Status = Live, launch_date = today)
  ↓
+72 hours
  ↓
[72hr Review Trigger] creates Optimization record (status: Pending Review)
  linked to the campaign
  ↓
within ≤12 hours
  ↓
[Campaign Intelligence Agent] runs (every 12h cron)
  - Get Live Campaigns: SS Campaigns where status=Live (spend, leads, CPL,
    days running, type)
  - Format for Claude: structures into prompt block, builds lookup map
    {campaignName → {campaignId, optimizationRecordId}}
  - Claude Haiku 4.5: returns CAMPAIGN_NAME | DECISION | REASONING per line
  - Write Decisions: parses output, looks up optimizationRecordId,
    PATCHes decision + reasoning fields
  - DMs Andrew the summary
  ↓
within minutes
  ↓
[Decision Router] sees decision populated + decision_notification_sent=false:
  Cut          → flip Campaign.status=Cut, create "Cut/Pause" task, Slack alert
  Keep Running → next_review_date = +7d, Slack alert
  Retarget     → create "Adjust Targeting" task, Slack alert
  Swap Creative → create "Swap Ad Creative" task, Slack alert
  Needs Review → create "Flag for Andrew Review" task, Slack alert
  THEN sets decision_notification_sent=true
  ↓
If Keep Running, the +7d next_review fires the cycle again indefinitely
until the agent says Cut.
```

**No human in the loop unless decision = "Needs Review."** The whole point.

---

## K. CURRENT DATA STATE (verified Apr 25)

- 6 active clients: Bayrock Home Buyers, Next Journey, Real-Vantage, First Integrity, Quick Home Buyers, Ritsel Notes — all with complete Drive folder structure (Bayrock + Next Journey were manually backfilled in the Apr 25 fix session).
- Pipeline: 8 Won deals, all with `won_processed=true` (M5 will not reprocess).
- Onboarding: in progress for active clients, all on the REI niche.
- Campaigns: 0 live campaigns yet — agency is at the cusp of first launch.
- Drive: 4–6 client folders under RequityAI parent.
- Slack: per-client channel pairs exist for active clients. #team-operations is healthy.

---

## L. OUTSTANDING MANUAL ACTIONS FOR ANDREW

These are the only items where the system is waiting on a human. Knock these out and the system runs hands-off until the first campaign launches.

1. **Build the SS Automation in SmartSuite UI for M5:** Pipeline → Automations → New → Trigger "Record Updated" → Condition `deal_stage = "Won"` → Action HTTP POST to `https://requityai.app.n8n.cloud/webhook/m5-deal-won` with body `{"record_id":"{{record.id}}"}`. (Until then M5 still fires within 5 min via the fallback poller — the SS Automation makes it instant.)
2. **Build the SS Automation for M4** (No-Show): same pattern, condition `deal_stage = "No Show"`, POST to `/webhook/m4-no-show`.
3. **Trash the test Drive folder** `1VIiP7C8C8nIQccDQg9mcwqEa9UntlldP` (ZZ Test Client) in Drive UI.
4. **Audit Phase 3 workflows** (the 18 declared-live but never real-tested workflows listed in the Apr 25 handoff doc) before first campaign launch.

---

## M. HOW IT EVOLVES — RULES THAT GOVERN CHANGE

From `CLAUDE.md` (the canonical operator brief), three rules:

1. **Full autonomy on the stack.** Patch, fix, ship, report after the fact. Don't ask permission for routine work.
2. **Escalate only three things before acting:** destructive changes that could lose live data, cost-impacting changes, architectural shifts that move the system off its current foundations.
3. **Diagnose before patching.** Pull execution logs, read the actual payload, then act. One probe beats six speculations.

**Out of scope for AgencyOS:** sales, proposals, pricing, client comms, ad scripts, VA task content. Those are the Sales & Fulfillment project. AgencyOS is the infrastructure layer.

**The filter for every decision:** does this keep the stack running, make a VA more effective, or remove Andrew as a bottleneck? If not, it's noise.

---

## N. THE ONE-PARAGRAPH SUMMARY (if someone asks "what is AgencyOS?")

AgencyOS is the operational brain and infrastructure layer for RequityAI, a Facebook ads agency for real-estate operators. SmartSuite is the source of truth across 8 apps (Pipeline, Conversation Tracker, Clients, Onboarding, Campaigns, Tasks, Optimization, Finance). n8n Cloud runs 21 active workflows that carry every state change — from a Calendly booking firing M3 to write a Pipeline record, through Andrew flipping a deal to Won and M5 atomically creating a Client + Onboarding record + two Slack channels + welcome message with niche-aware onboarding docs + Drive folder structure, through the VA executing a deterministic 19-step onboarding checklist whose progress is read and updated by automation, through campaign build and QA self-cert in Slack, through a 72hr-then-7day optimization loop where Claude Haiku reads live campaign data and writes decisions to Optimization records that a Decision Router executes (Cut / Keep / Retarget / Swap Creative / Needs Review). The VA's hands are physical for ~9 specific things — Slack guest invite, Meta access requests, video editing, Ads Manager build, QA inspection, decision execution. Everything else is automated. Andrew is the sales engine and the escalation point; the VA is the precision operator; the agents do the cognition; and the automation layer is the connective tissue that means nothing falls through the cracks.

---

*This document supersedes `AgencyOS_Current_State.md` (which was last updated Apr 20 and is now stale on workflow count, M5 architecture, niche-aware doc delivery, and the Apr 26 audit results). When this doc and an older one disagree, this one wins until the next audit.*
