# AgencyOS — Current System State

**Last Updated:** 2026-04-20 (M3 Calendly shipped)
**Purpose:** Single source of truth. Read this FIRST before any work on RequityAI.

---

## System Architecture

- **Command Center:** SmartSuite (8 apps)
- **Automation:** n8n Cloud — **24 active workflows** (not 37 — old number was pre-cleanup)
- **Metrics:** Windsor AI → n8n → SmartSuite
- **VA Coordination:** Slack (#team-tasks = C0AKWU4835E)
- **Content Storage:** Google Drive
- **Dialer:** Close CRM (calling only — SmartSuite Pipeline is SoT for deal state)
- **Scheduling:** Calendly → n8n webhook → SmartSuite Pipeline (LIVE as of Apr 20)
- **Builder:** Signal (Manus retired Apr 17)

---

## The 8 SmartSuite Apps

| # | App | App ID | Status |
|---|-----|--------|--------|
| 1 | Pipeline | `6908636826cfbf4238a34f31` | 17 records, 7 stages, clean |
| 2 | Conversation Tracker | (live) | Clean — M2 webhook writing |
| 3 | Clients | `69ce5f18cb8a07430bfee02d` | 4 clients, all bi-linked to Onboarding |
| 4 | Onboarding | `69db909cd9114601cccb2b57` | 19 step fields, 3-state dropdowns |
| 5 | Campaigns | `69ce678977bf866e34b46f68` | 1 test record (awaits first real build) |
| 6 | Tasks | (live) | 15 task types, 1 record (Done) |
| 7 | Optimization | (live) | 0 records, ready for 72hr reviews |
| 8 | Finance | (live) | Andrew only |

---

## n8n — 24 Active Workflows (verified Apr 20 13:40 UTC)

**Core automation (schedule-driven):**
- `BegEckXSgXmVffX2` — Clients → Drive Folder → Slack (v3 FIXED)
- `ZwXd0unFysJjWl1M` — Windsor AI → SmartSuite Metrics (12h)
- `ey0cuADK27ntvgMe` — Daily Ops Briefing — 8am
- `CqesBe55FnP6oaxA` — Onboarding Health Monitor (daily + SLA escalation)
- `Zv2PYFdMiBDCLcZV` — Form Submitted Watcher
- `o6A12htwZffpOkbu` — Video Watcher
- `fdUdIRGsBq0HB4jA` — Client Nudge (Form & Video reminders)
- `9jGs4HGdijkyYB4f` — Campaign Launch → Notify Client in Slack
- `uDdwyIl7VDFEWJ8N` — Prerequisites Met → Auto-Create Campaign Build Task
- `NFU4jyVpaRSKv4Mj` — Onboarding Progression
- `IHEmXUHvz1T034lF` — Campaign QA Ready → Slack Checklist
- `VTiPgz0Zem8jiOYx` — 72hr Review Trigger
- `OmtNWq7oETDUAjni` — Creative Fatigue Alert (28-day)
- `gRzeR9zO9xbHMvXG` — CPL Threshold Alert → DM Andrew
- `6TuDo3mqBZSBF667` — Campaign Intelligence Agent (JSON-escape FIXED Apr 20)
- `iM5CNWHLS2UIIJ34` — Decision Router
- `lUl2nkA0Bo1k8nbv` — Stale Record Detector
- `5cdMtOByeZVRFS6H` — Slack Ops Supervisor (JSON-escape FIXED Apr 20)

**Event/webhook-driven:**
- `dInuMwYxjwcftjSp` — M2 Close CRM Webhook → SmartSuite (push)
- `1LMmEYIxSQHsPZd1` — **M3 Calendly invitee.created → SmartSuite (LIVE Apr 20)**
- `8tdPtQWO4qDKEjgq` — SmartSuite Sync Agent — Slack /update Parser
- `ynGKEAco9U6Q0ShI` — Slack Task Router — /done
- `ra2F0R9zrKMmGEvE` — Task Blocked → DM Andrew
- `D4AvztGc4RCYyE5g` — Task Assigned → Slack + Task Complete → Confirm
- `ePyAmNK7lpzoXPgo` — Global Error Handler (errorTrigger — all 23 others wired)

---

## What Ships Through What

```
CLOSE CRM (dialer only)
  └─ call outcomes ──[M2 webhook → ConvTracker]──> SmartSuite

CALENDLY (LIVE Apr 20)
  └─ invitee.created ──[M3 webhook]──> Pipeline (deal_stage = Booked)

WINDSOR AI
  └─ FB Ads metrics ──[12h cron]──> Campaigns.metrics

SMARTSUITE (SoT for deals, clients, campaigns, tasks)
  ├─ Prerequisites Met → auto-creates Campaign Build task when onboarding complete
  ├─ Task Assigned → DMs VA in #team-tasks
  └─ Campaign QA Ready → posts checklist + VA self-cert branch

SLACK
  ├─ #team-tasks — unified VA feed, /done, /update, /blocked
  ├─ #team-<client> (private x4) — internal VA + Andrew
  ├─ #client-<client> (public x4) — external client-facing
  ├─ #new-clients — onboarding handoffs
  └─ DMs to Andrew — errors, alerts, supervisor nudges

GOOGLE DRIVE — RequityAI/<Client>/ — content store
```

---

## Current Data State

- Clients: 4 (Real-Vantage, First Integrity, Quick Home Buyers, Ritsel Notes)
- Pipeline: 17 records across 7 stages
- Campaigns: 1 test record — **NOTE:** no live VA-pickupable builds yet
- Tasks: 1 record (Done)
- Optimization: 0 records
- Drive: 4 client folders under `RequityAI` parent (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`)

---

## Verdict — Blockers to VA Handover

1. ~~Four broken watchers~~ — **CLEARED Apr 20.** Video Watcher, Form Watcher, Client Nudge, Campaign Launch all ran green at 04:00 UTC cron today.
2. **Empty VA queue.** Campaigns app has no live builds. Before handing to a VA, seed one real Campaign Build by either: (a) walking a real client's onboarding to completion → Prerequisites Met auto-creates the task, or (b) manually seeding a Campaign record with status "QA Ready".

That's it. Core system is clean.

---

## Remaining Known Issues (non-blocking)

- **Manual Deal-Won step.** After zombie HZ18Xb98 killed Apr 19, moving a deal to Won no longer auto-creates Client + Onboarding. Manual 2-step until rebuilt clean (Wave 2).
- **Filter-key inversion vulnerability.** `fields` vs `filters` has bitten twice. Still no automated guard.
- **Real-booking verification for M3.** Synthetic verified Apr 20 — real Calendly booking not yet fired through. Will auto-prove on first org booking.

---

## Campaign Funnel

| Stage | Campaign Type | Objective | CTA | Audience |
|---|---|---|---|---|
| TOF | Video Views | Video Views | "Comment OPTIONS" in copy | Broad (Special Housing — no zip codes) |
| MOF | Retarget | Engagement | "Comment OPTIONS" (different video) | Custom audience from TOF viewers (50/75/95%) |
| BOF | Lead Ad | Leads | FB Lead Form attached | Custom audience from MOF engagement |

No pixel needed. Retargeting audiences created post-launch by Campaign Intelligence Agent, not during onboarding.

---

## Creative Workflow

1. Signal writes scripts (`[SITUATION]-B[#]-[SCRIPT##]` — 12 codes, 60 scripts)
2. VA reviews/edits for client voice
3. Client records talking-head videos → Drive Raw Video folder
4. VA processes → Drive Ad Creative folder
5. VA builds via CSV Import (primary) or Manual (fallback)

---

## Wave Progress

- **Wave 1 (Apr 19):** SHIPPED — Onboarding SLA, Global Error Handler, retry wrappers, QA self-cert
- **Wave 2 (Apr 19–20):** M2 Close webhook ✅, M3 Calendly webhook ✅, W1 poll-to-webhook migration ☐, B5 thruplay auto-trigger ☐
- **Wave 3:** Client touchpoints (B2), lead delivery verify (B3), Client Health Score (B4) — not started
- **Wave 4:** Data integrity (W6, W8) — not started
- **Wave 5:** Hygiene (W3, W4, W7, B6, M1) — not started

---

## Rules for Future Sessions

1. Read `AgencyOS_SmartSuite_Structure_Spec.md` before any SmartSuite work. No exceptions.
2. Read this file at start of any new session.
3. SmartSuite list filter key is `fields`, not `filters`. Inversion silently returns ALL records.
4. SmartSuite dropdown updates require numeric indices for Onboarding step fields ("1"/"2"/"3"); string labels for Tasks and Campaigns status fields.
5. Never use `httpRequestWithAuthentication` in n8n Code nodes — use HTTP Request node with credential.
6. Never edit trigger nodes on an active workflow. Deactivate → edit → save → reactivate. Zombies hide in staticData.
7. Content (scripts, videos, creative) lives in Google Drive. SmartSuite stores links only.
8. VAs don't create tasks, don't update onboarding steps, don't touch Finance or Optimization.
9. When a memory rule matters, probe live before trusting it.
