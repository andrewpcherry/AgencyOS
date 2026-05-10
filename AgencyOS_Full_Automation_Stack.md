# AgencyOS — Full Automation Stack
**RequityAI | Last updated: April 13, 2026**

---

## How to read this document

Every automation in RequityAI's stack is described here: what triggers it, what it does, what it writes to, and what fires next. This is the single source of truth for the entire system.

**Core principle: everything is event-driven.** No fixed calendar days. No Monday tasks, no Friday tasks. Every action fires because something happened — a field changed, a step was completed, a timer elapsed relative to a campaign launch date.

---

## THE FULL PIPELINE — END TO END

```
CLOSE CRM (lead/deal)
        ↓
  Deal closes → Andrew creates Client record in SmartSuite manually
        ↓
  ONBOARDING APP — VA works through 25-step checklist
        ↓
  WF1 monitors Onboarding → fires tasks at milestone completions
        ↓
  Campaign launched → Client marked Active
        ↓
  72hr elapses → Optimization record auto-created
        ↓
  Campaign Intelligence Agent (every 12h) → analyzes all live campaigns
        ↓
  Per-campaign decision written to Optimization record
        ↓
  Decision Router fires → executes decision (Cut / Keep / Retarget / etc.)
        ↓
  Daily Ops Briefing (8am) → team status in #team-tasks
```

---

## SMARTSUITE APPS (the data layer)

| App | ID | Purpose |
|-----|-----|---------|
| Clients | 69ce5f18cb8a07430bfee02d | Master client record. Tracks status (Prospect → Active → Churned) |
| Onboarding | 69db909cd9114601cccb2b57 | 25-step checklist. 3-state dropdowns (Pending / In Progress / Complete). One record per client |
| Tasks | 69ce67b3fec5b91842ebaf03 | All VA work orders. Created by automations, not manually |
| Campaigns | 69ce678977bf866e34b46f68 | Live campaign records. Status field drives the whole optimization loop |
| Optimization | 69ce67e01cc0855f89fee02e | One record per campaign review cycle. Stores decision + execution state |
| Finance | (solution: 69ce5f18cb8a07430bfee02b) | Revenue tracking. Setup fees + retainers. View: "Unpaid" |

**Content lives in Google Drive. SmartSuite holds links, not files.**
Scripts, video briefs, and creative assets are stored in Google Drive. SmartSuite fields hold the Drive URLs.

---

## N8N WORKFLOWS

---

### WF1 — Onboarding Progression
**ID:** NFU4jyVpaRSKv4Mj | **Status:** ACTIVE

**What it watches:** SmartSuite Onboarding app (polls on schedule)

**Trigger 1 — All Access Steps Complete:**
- Condition: ACCESS: FB Page Access, ACCESS: Ad Account Access, ACCESS: BM Access all = "Complete"
- Action: Creates task in Tasks app → "Build Audiences"
- Posts to Slack #team-tasks: `✅ Access confirmed — [Client Name]. Build Audiences task created.`

**Trigger 2 — Videos Approved:**
- Condition: VIDEOS: Video Review = "Complete"
- Action: Creates task in Tasks app → "Upload Creative"
- Posts to Slack #team-tasks: `🎬 Videos approved — [Client Name]. Upload Creative task created.`

**Trigger 3 — Launch Notification Sent:**
- Condition: LAUNCH: Launch Notification = "Complete"
- Action: Marks Onboarding record = Complete, sets Client Status = Active in Clients app
- Posts to Slack #team-tasks: `🚀 Onboarding complete — [Client Name] is now LIVE.`

**Key IDs used:**
- Onboarding app: 69db909cd9114601cccb2b57
- Tasks app: 69ce67b3fec5b91842ebaf03
- Clients app: 69ce5f18cb8a07430bfee02d
- Slack credential: slackOAuth2Api ID ZfcZadVk2p3qVS3a (Slack account 2)
- Slack channel: C0AKWU4835E (#team-tasks)

---

### WF2 — Build Audiences → Campaign Launch
**Status:** ACTIVE

**What it watches:** Tasks app — polls for "Build Audiences" tasks marked Complete

**Trigger:** "Build Audiences" task status = Complete
**Action:**
- Creates next task in Tasks app → "Launch Campaign"
- Posts to Slack #team-tasks: notification that audiences are built and campaign is ready to launch

**This is the bridge between the build phase and go-live.**

---

### 72hr Review Trigger
**Status:** ACTIVE

**What it watches:** Campaigns app — calculates elapsed time since campaign launch date

**Trigger:** Campaign status = Live AND (today - launch_date) ≥ 3 days
**Action:**
- Creates a new record in the Optimization app linked to the campaign
- Sets optimization record status = Pending Review
- This record sits waiting for the Campaign Intelligence Agent to fill in the `decision` field

**This is the entry point for the entire optimization loop.**

---

### Campaign Intelligence Agent
**ID:** 6TuDo3mqBZSBF667 | **Status:** ACTIVE (write-back enabled)

**Schedule:** Every 12 hours

**Node 1 — Get Live Campaigns:**
- POST to SmartSuite Campaigns app (69ce678977bf866e34b46f68)
- Filter: status = "Live"
- Returns all active campaigns with spend, leads, CPL, days running, campaign type

**Node 2 — Format for Claude:**
- Code node that structures campaign data into a clean prompt block
- Also builds a lookup map: `{campaignName → {campaignId, optimizationRecordId}}`
- The lookup map travels alongside the Claude prompt (not inside it)

**Node 3 — Claude Campaign Analysis:**
- POST to https://api.anthropic.com/v1/messages
- Model: claude-haiku-4-5-20251001
- Prompt instructs Claude to return decisions in parseable format:
  `CAMPAIGN_NAME | DECISION | REASONING`
- Valid decisions: `Keep Running` / `Cut` / `Retarget` / `Swap Creative` / `Needs Review`

**Node 4 — Write Decisions to SmartSuite (NEW):**
- Code node that parses Claude's `CAMPAIGN_NAME | DECISION | REASONING` output line by line
- For each line: looks up the Optimization record ID from the lookup map
- PATCHes the `decision` field on that Optimization record
- Also writes `reasoning` to the Optimization record if the field exists
- This write is what triggers the Decision Router — no manual intervention needed

**Node 5 — DM Andrew (Slack):**
- Posts a summary of all decisions made to Andrew's DM (or #team-tasks)
- Confirmation that the agent ran, decisions written, Decision Router will execute

---

### Decision Router
**ID:** iM5CNWHLS2UIIJ34 | **Status:** ACTIVE

**What it watches:** Optimization app — polls for records where:
- `decision` field is populated (not empty)
- `decision_notification_sent` = false

**On match, routes by decision value:**

| Decision | Action |
|----------|--------|
| **Cut** | PATCH Campaign status = "Cut" → Create VA task "Cut / Pause Campaign" → Slack alert to #team-tasks |
| **Keep Running** | Set `next_review_date` = today + 7 days → Slack alert to #team-tasks |
| **Retarget** | Create VA task "Adjust Targeting" → Slack alert |
| **Swap Creative** | Create VA task "Swap Ad Creative" → Slack alert |
| **Needs Review** | Create VA task "Flag for Andrew Review" → Slack alert |

**After execution:** Sets `decision_notification_sent` = true on the Optimization record (prevents double-firing)

---

### Daily Ops Briefing
**Schedule:** 8:00 AM daily | **Status:** ACTIVE

**What it does:**
- Queries SmartSuite for: open Tasks (assigned, not complete), Active clients, any Campaigns with status anomalies
- Posts structured daily briefing to Slack #team-tasks
- Gives VA and Andrew a single morning snapshot of what needs action today

---

### Task Assigned → Slack
**Status:** ACTIVE

**Trigger:** New task created in Tasks app with an assignee
**Action:** Posts to Slack #team-tasks notifying the assignee a task is waiting

---

### DEACTIVATED — Do Not Reactivate

| Workflow | Why Killed |
|----------|------------|
| Weekly Skeleton Tasks | Hardcoded weekly task creation violated event-driven architecture |
| Campaign Goes Live → Set Next Action Date (Thursday) | Hardcoded "Thursday" — tasks must be relative to launch date, not calendar day |

---

## THE OPTIMIZATION LOOP (zoomed in)

This is the core intelligence cycle of the entire system:

```
Campaign launched
      ↓
  [+72 hours]
      ↓
  72hr Review Trigger creates Optimization record (status: Pending Review)
      ↓
  [up to 12 hours later]
      ↓
  Campaign Intelligence Agent runs (schedule: every 12h)
  → Pulls all Live campaigns from SmartSuite
  → Sends to Claude for analysis
  → Claude returns: CAMPAIGN_NAME | DECISION | REASONING
  → Write-back node PATCHes `decision` on Optimization record
      ↓
  [within minutes]
      ↓
  Decision Router detects decision_notification_sent = false
  → Executes decision
  → Marks decision_notification_sent = true
      ↓
  If decision = Keep Running → next_review_date = +7 days
  → 72hr Trigger equivalent fires again in 7 days
  → Loop continues indefinitely until Cut
```

**No human in the loop unless decision = "Needs Review."**

---

## ONBOARDING CHECKLIST (25 steps, phase-prefixed)

VA works through these in order. Each field is a 3-state dropdown: Pending → In Progress → Complete.

| Phase | Steps |
|-------|-------|
| **ACCESS** | FB Page Access, Ad Account Access, Business Manager Access |
| **LEADS** | Lead Form Setup, Lead Webhook Test, CRM Integration Confirmed |
| **VIDEOS** | Video Brief Sent, Videos Received, Video Review |
| **AUDIENCE** | Custom Audience Created, Lookalike Audience Created, Retargeting Audience Created |
| **LAUNCH** | Campaign Structure Built, Ad Copy Written, Creatives Uploaded, Campaign Review, Campaign Published, Launch Notification Sent, Client Briefed |

**WF1 fires at three milestone completions:** All ACCESS complete, VIDEOS: Video Review complete, LAUNCH: Launch Notification Sent complete.

---

## CREDENTIALS & IDs (quick reference)

| Item | Value |
|------|-------|
| SmartSuite API Token | Token 716c2356a4f2679445cca53e374fb173be57ba7d |
| SmartSuite Account ID | 52739 |
| Slack Credential (n8n) | slackOAuth2Api ID: ZfcZadVk2p3qVS3a ("Slack account 2") |
| Slack Channel — #team-tasks | C0AKWU4835E |
| Anthropic API | Used by Campaign Intelligence Agent (Claude Haiku) |

---

## ARCHITECTURE DECISIONS (locked)

- **Google Drive for content, SmartSuite for links.** Scripts and creative assets apps were killed. Drive links live in SmartSuite fields.
- **Organic posting is manual.** VA posts videos to client FB Page during campaign build. Same OPTIONS CTA every time. No API automation on this.
- **No fixed days.** All task timing is relative to campaign launch date or step completion time.
- **Ritsel Homes is notes/probate, not wholesaling.** Separate video scripts and ad content. Different niche, different messaging.
- **Andrew is not the builder.** Andrew's role: decisions, QA, and activating workflows. Not building nodes, not editing code.

---

*This document is the operating manual for AgencyOS. If a workflow fires unexpectedly or a step is missed, check this document first.*
