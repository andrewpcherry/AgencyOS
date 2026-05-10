# AgencyOS — Audit Verdict & Operator's Manual
**Audit date:** 2026-04-20 (04:56 UTC — ADDENDUM APPLIED 13:45 UTC)
**Auditor:** Signal
**Scope:** Full end-to-end — SmartSuite, n8n, Slack, Drive, Close, Windsor, Calendly/M3.

---

## ⚠ ADDENDUM — Written 9 hours after audit body below ⚠

Two findings in the audit body have been resolved since this doc was written. Treat the body as historical reference; trust this addendum for current state:

1. **Blocker 1 (four broken watchers) — CLEARED.** Video Watcher, Form Watcher, Client Nudge, Campaign Launch all executed `success` at the 04:00 UTC cron today (execs 2752/2758/2761/2753). The audit body was written before that cron fired. Zero-item results were correct behavior (nobody matched criteria); no error traffic.
2. **Issue 3a (Campaign Intelligence Agent JSON escape) — FIXED.** The `specifyBody: "json"` + `jsonBody` pattern landed. Exec 2763 at 04:00 UTC ran all 9 nodes clean end-to-end.
3. **M3 Calendly — SHIPPED.** No longer parked. Workflow `1LMmEYIxSQHsPZd1` reactivated. Calendly webhook subscription `a4a103d6-2404-4db8-9e41-a806870faf15` active for `invitee.created` + `invitee.canceled`. Synthetic payload verified: Pipeline record created with `deal_stage: Booked`. Real-booking verification pending first live booking.

**True current blocker to VA handover:** only the empty VA queue (Blocker 2 below). Seed one real Campaign Build task and system is ready.

---

---

## 1. CATEGORICAL VERDICT — Is AgencyOS ready for a VA today?

**No. Not yet. Two blockers. ~2 hours of work to clear.**

The system core is solid — data is clean, channels and folders are in place, Pipeline and Sync Agent work, M2 push is live, Global Error Handler catches failures. But four VA-facing watchers are firing 100% errors on every scheduled run, and the VA queue is currently empty. If you hand the system to a VA in its current state, they will see a dashboard with no tasks while you get 24+ error DMs per day.

**Bottom line:** do not onboard a VA to AgencyOS until the two blockers below are fixed. After that, system is VA-ready for the campaign-build workflow.

---

## 2. BLOCKERS — Must fix before VA handover

### BLOCKER 1 — Four active workflows are 100% broken
Four workflows query the **Clients** app (69ce5f18cb8a07430bfee02d) using field slugs that only exist on the **Onboarding** app (69db909cd9114601cccb2b57). Every scheduled run returns 400 Bad Request. Confirmed via live execution inspection — 40/40 recent runs = error.

| Workflow ID | Name | What it's supposed to do | Confirmed fail |
|---|---|---|---|
| `fdUdIRGsBq0HB4jA` | Client Nudge — Form & Video Reminders | DM reminders when onboarding form/videos overdue | 10/10 err |
| `Zv2PYFdMiBDCLcZV` | Form Submitted Watcher | Detects form completion, advances onboarding step | 9/10 err |
| `o6A12htwZffpOkbu` | Video Watcher | Detects videos uploaded to Drive, advances step | 10/10 err |
| `9jGs4HGdijkyYB4f` | Campaign Launch → Notify Client in Slack | Posts launch notice to #client-X channel | 10/10 err |

**Root cause:** each workflow has a SmartSuite `records/list_with_params` POST node hitting the Clients app ID but filtering on Onboarding slugs (`ob_form_submitted`, `ob_videos_received`, `step_campaign_launched`, `step_launch_notification_sent`). Those slugs don't exist on Clients → 400.

**Fix (per workflow):** change the appId in the failing node from `69ce5f18cb8a07430bfee02d` to `69db909cd9114601cccb2b57`. Then re-map any downstream `.client` field access to use the linked-client slug from the Onboarding record.

**Why this is a blocker:** three of the four are the engine of client onboarding and campaign delivery notifications. VA sees no onboarding progression, client sees no launch confirmation, Andrew gets no nudge-chain firing.

### BLOCKER 2 — VA queue is empty
Current data state:
- Campaigns app: 1 test record only, no live VA-pickupable builds
- Tasks app: 1 task, status Done
- Optimization app: 0 records

**Why this is a blocker:** even if every workflow worked perfectly, a VA opening SmartSuite right now sees nothing to do. You need at least one real Campaign Build task seeded before handover, otherwise the first VA question will be "what do I work on?"

**Fix:** manually create one Campaign Build task for the first real client through the normal flow (Client → Onboarding complete → Prerequisites Met fires → Campaign created → Task Assigned DMs VA). Or seed one directly in the Campaigns app with status "QA Ready" so the VA has a real first piece of work.

---

## 3. NON-BLOCKING ISSUES — Fix in next 48h

### 3a. Campaign Intelligence Agent — 100% error rate
14/14 recent runs fail with `unexpected control character in string` at JSON-parse time. Root cause: Claude API HTTP node builds the request body by string-interpolating SmartSuite campaign content (which may contain newlines, quotes, control chars) without JSON-escaping.

**Impact:** Decision Router never gets the AI recommendation → cut/retarget/keep decisions are manual. Not VA-blocking; this is an Andrew-facing feature.

**Fix:** wrap all interpolated strings with a Function/Code node that runs `JSON.stringify()` on each field before assembly.

### 3b. Slack Ops Supervisor — 47% error rate
Same JSON-escape failure mode as Campaign Intelligence Agent — same fix.

**Impact:** supervisor DMs to Andrew sometimes fire, sometimes fail silently. Not VA-blocking.

### 3c. Deal Won → Client + Onboarding creation is manual
The old `HZ18Xb98Szin8OTQ` workflow that did this was killed during the zombie incident (Apr 19). Current state: when a deal moves to Won in Pipeline, **you** have to hand-create Client + Onboarding records. `BegEckXSgXmVffX2` then auto-creates Drive folder + Slack channels.

**Impact:** minor manual step on each close. Logged as Wave 2 candidate (clean rebuild).

### 3d. Zombie trigger audit — one still pending
The Apr 19 audit flagged 3 candidates; 2 were cleared (1 benign, 1 zombie deactivated). The third — `5cdMtOByeZVRFS6H` Slack Ops Supervisor — was marked benign but is currently 47% erroring. Re-check its scheduler config while fixing 3b.

### 3e. M3 Calendly parked
Workflow `1LMmEYIxSQHsPZd1` is built and verified but deactivated pending a Calendly Standard plan upgrade. Not blocking — today, meetings flow from Calendly email → manual addition to SS Pipeline. Unblock Apr 20+ with 3 steps (already documented).

---

## 4. WHAT IS WORKING — Confirmed clean

| System | Status | Evidence |
|---|---|---|
| SmartSuite apps (8) | All app IDs valid, schema correct | Live probe Apr 19 — filter key `fields` confirmed |
| Pipeline data | 17 records across 7 stages | Sunlit corruption from filter inversion already fixed |
| Clients data | 4 clients, all bi-linked to Onboarding | Real-Vantage, First Integrity, Quick Home Buyers, Ritsel Notes |
| Drive folders | All 4 client folders exist under RequityAI parent | Verified folder IDs match SS URLs |
| Slack architecture | 4 `#team-X` (private) + 4 `#client-X` (public) + `#new-clients` + `#team-tasks` | Search confirmed pair pattern intact |
| M2 webhook (Close→SS push) | Active, subscription `whsub_3wzlFrsrVJP0Gh9HeSQ0jX` | Last exec success Apr 19 13:06 |
| Sync Agent (/update parser) | v1.3 active | Last exec success Apr 19 12:30 |
| Global Error Handler | Active, firing correctly | 8 catches over 24h — proves other workflows' errors are being surfaced |
| Clients→Drive→Slack (v3) | 15 clean runs | `BegEckXSgXmVffX2` is the only path for onboarding creation |
| Close CRM retirement | Complete | 2 pollers deactivated; M2 Opp+Meeting branches disconnected; SS is SoT |
| Close dropdown choices | 10 clean values persisted via API bypass | Verified Apr 19 |

---

## 5. OPERATOR'S MANUAL — How AgencyOS actually runs

### 5.1 System architecture at a glance

```
CLOSE CRM (dialer only)                    SMARTSUITE (source of truth)
  ├─ Calls + call outcomes ──[M2 webhook]──> Conversation Tracker
  └─ Deal state ──(NOT synced anymore — SS is SoT)

CALENDLY (manual for now, M3 parked)
  └─ Bookings ──[email]──> hand-added to Pipeline

WINDSOR AI (FB Ads metrics)
  └─ ──[12h poll]──> Campaigns.metrics fields

SMARTSUITE (8 apps)
  ├─ Pipeline (deals) ─── sales funnel, Won triggers client creation
  ├─ Clients ─────────── core customer record
  ├─ Onboarding ──────── step-by-step kickoff tracker
  ├─ Campaigns ───────── VA build queue + live campaign tracker
  ├─ Tasks ───────────── unified task list (15 task types)
  ├─ Optimization ────── weekly review / decision records
  ├─ Finance ─────────── invoicing + payment tracking
  └─ Conversation Tracker — call + meeting log

n8n (24 active workflows) = glue layer
  └─ Watches SmartSuite + Close + Windsor → posts Slack, advances records

SLACK (VA coordination)
  ├─ #team-tasks            — unified VA task feed + /done, /update
  ├─ #team-<client>         — internal VA discussion (private)
  ├─ #client-<client>       — external client-facing (public)
  ├─ #new-clients           — onboarding handoffs
  └─ DMs to Andrew          — errors, alerts, supervisor nudges

GOOGLE DRIVE (content store)
  └─ RequityAI/<Client>/    — raw videos, edited ads, scripts
```

### 5.2 The daily flow — what happens in what order

**Stage 1 — Sale closes (Andrew manual)**
1. Move deal to Won in SS Pipeline.
2. Create Client record in Clients app (manual — see Blocker 3c).
3. Create Onboarding record linked to Client (slug: `client`).
4. `BegEckXSgXmVffX2` picks up new Client on next hourly run → creates Drive folder + 2 Slack channels (`#client-X`, `#team-X`) + posts to `#new-clients`.

**Stage 2 — Onboarding (VA + client)**
1. Client fills intake form → Onboarding.step_form_submitted marked complete *(currently manual — Form Submitted Watcher is broken)*.
2. Client uploads videos to Drive → step_videos_received marked complete *(currently manual — Video Watcher is broken)*.
3. Prerequisites Met workflow (`uDdwyIl7VDFEWJ8N`) detects all onboarding steps complete → auto-creates Campaign Build task in Tasks app → Task Assigned workflow DMs the VA via `#team-tasks`.

**Stage 3 — Campaign build (VA primary work)**
1. VA sees Task Assigned notification in `#team-tasks` with Campaign ID + client link.
2. VA opens Campaigns app record → follows Campaign Build SOP (Google Doc linked from `sop_link` field).
3. Default path: **CSV Import** method (see `project_csv_import_build.md`). Manual build is fallback only.
4. VA builds TOF Video Views + MOF Retarget + BOF Lead Ad stack, using talking-head videos from Drive.
5. VA flips Campaign status to "QA Ready" → `IHEmXUHvz1T034lF` (Campaign QA Ready → Slack Checklist) posts the QA checklist.
6. VA runs self-cert checklist, then flips to "Live" → `9jGs4HGdijkyYB4f` is *supposed to* post launch notice to `#client-X` *(currently broken — see Blocker 1)*.
7. VA closes the Task via `/done [Task-ID]` in `#team-tasks` → `ynGKEAco9U6Q0ShI` (Slack Task Router) marks Task Done.

**Stage 4 — Live campaign management (VA ongoing)**
1. Windsor AI syncs FB Ads metrics → Campaigns.metrics every 12h (`ZwXd0unFysJjWl1M`).
2. CPL Threshold Alert (`gRzeR9zO9xbHMvXG`) DMs Andrew if CPL > ceiling.
3. Creative Fatigue Alert (`OmtNWq7oETDUAjni`) fires at 28-day mark.
4. 72hr Review Trigger (`VTiPgz0Zem8jiOYx`) creates Optimization record after launch+72h.
5. Decision Router (`iM5CNWHLS2UIIJ34`) + Campaign Intelligence Agent (`6TuDo3mqBZSBF667`) *should* produce cut/retarget/keep decision *(Intel Agent currently broken — see 3a)*.

**Stage 5 — VA status updates**
- Any time VA has context to share: type `/update <Task-ID> <notes>` in `#team-tasks` → Sync Agent (`8tdPtQWO4qDKEjgq`) parses + writes to Task.last_update and Task.notes.
- If VA blocked: type `/blocked <Task-ID> <reason>` → Task Blocked (`ra2F0R9zrKMmGEvE`) DMs Andrew.

### 5.3 VA's daily workflow (the one page they need)

```
START OF SHIFT
  1. Open Slack → #team-tasks channel → scroll back to last /done
  2. For each new "Task Assigned" notification: click SmartSuite link
  3. Open the Campaigns app record → read sop_link → work the SOP
  4. Upload assets to the client's Drive folder (linked in Campaigns record)
  5. Flip Campaign status when stage complete:
      Draft → QA Ready → Live → Completed
  6. /update <Task-ID> <what you did> after any major step
  7. /done <Task-ID> when task complete
  8. /blocked <Task-ID> <reason> if stuck

ESCALATION
  — Never touch Pipeline or Clients apps (Andrew-only)
  — Never create new Onboarding records (they're auto-created)
  — Never post directly in #client-X channels — only campaign outputs go there

END OF SHIFT
  — Post a summary in #team-tasks: "Today's done: [IDs], WIP: [IDs], blocked: [IDs]"
```

### 5.4 Andrew's daily workflow

```
MORNING (Daily Ops Briefing fires at 8am ET via ey0cuADK27ntvgMe)
  — Read the DM summary: which campaigns, which tasks, which alerts
  — Triage /blocked DMs from the night
  — Check Pipeline for new deals to move forward

THROUGHOUT DAY
  — Calls via Close (dialer only) — every call logs to ConvTracker via M2
  — Move deal stages in SS Pipeline (NOT Close anymore)
  — On Won: create Client + Onboarding records manually (Blocker 3c)

END OF DAY
  — Review Optimization app for pending decisions
  — Approve / reject Decision Router recommendations
```

### 5.5 Role boundaries (what each system owns)

| Concern | System of record | Do NOT edit in |
|---|---|---|
| Deal state / Opp stage | SmartSuite Pipeline | Close CRM |
| Call activity | Close → (via M2 webhook) ConvTracker | SmartSuite directly |
| Client record | SmartSuite Clients | anywhere else |
| Onboarding progress | SmartSuite Onboarding | Clients app |
| Campaign assets | Google Drive | SmartSuite attachments |
| Campaign metadata | SmartSuite Campaigns | Drive filenames |
| Task assignments | SmartSuite Tasks (via Slack `/done`, `/update`) | Slack messages |
| Ad performance | Windsor AI (read-only) → Campaigns | anywhere manual |
| Meetings | Calendly → manual SS Pipeline | Close |

### 5.6 Channel reference

| Channel | Type | Purpose | Automation touches it? |
|---|---|---|---|
| `#team-tasks` (C0AKWU4835E) | public | Unified task feed, /done, /update, /blocked | Yes — all task workflows |
| `#team-<client>` x4 | private | Internal VA + Andrew discussion per client | `BegEckXSgXmVffX2` creates |
| `#client-<client>` x4 | public | Client-facing updates, launch notices | `9jGs4HGdijkyYB4f` posts here (currently broken) |
| `#new-clients` | public | Onboarding handoff announcements | `BegEckXSgXmVffX2` posts here |
| DMs to Andrew | — | Errors, CPL alerts, blockers, supervisor | Global Error Handler + alerts |

---

## 6. WEAK SPOTS — Where the system is most likely to break

Ranked by blast radius × probability.

### 6.1 HIGH — SmartSuite filter key inversion (recurring)
The `fields` vs `filters` bug has been fixed twice and inverted once already (Apr 17 inversion was the root of the Sunlit corruption). Any new workflow author (or any re-deploy from a stale branch) can silently reintroduce it. Failure mode is catastrophic: 200 OK returning all records, upsert corrupts row 1.

**Mitigation:** check `feedback_n8n_smartsuite_bugs.md` is loaded before ANY n8n work. Add a weekly cron that greps all workflows for `"filters":` and Slack-DMs Andrew if any found.

### 6.2 HIGH — Zombie triggers survive in-place edits
Editing a trigger on an active workflow leaves staticData ghosts that n8n keeps scheduling. The HZ18Xb98 incident fired every 12h for 5+ days creating phantom folders.

**Mitigation:** never edit triggers on active workflow. Rule: deactivate → edit → save → reactivate. Weekly zombie audit (Python scan: staticData keys vs node names).

### 6.3 MEDIUM — App-ID mismatches in SmartSuite HTTP nodes
Blocker 1 is the example. The 4 workflows were likely copy-pasted from a Clients template and their queries never updated when Onboarding was split out. One line (the appId URL path segment) determines whether the query hits schema.

**Mitigation:** every SmartSuite HTTP node should have a comment line above it naming which app it's targeting. Pre-deploy check: grep for hard-coded app IDs in active workflow code vs the 8 known-good IDs.

### 6.4 MEDIUM — JSON body assembly in AI API calls
Campaign Intelligence Agent + Slack Ops Supervisor fail 47–100% of runs when SmartSuite content happens to contain control chars. Clients have no reason to stop including line breaks in their campaign descriptions.

**Mitigation:** always route interpolated content through a Function node that runs `JSON.stringify()` before HTTP body assembly. Add a unit-test input with a known-bad string ("quotes\nnewlines\ttabs") to each new AI workflow.

### 6.5 MEDIUM — Manual Deal-Won step is easy to skip
Since `HZ18Xb98Szin8OTQ` was killed, creating Client + Onboarding on Won is a manual 2-step that happens rarely. Easy to forget → Drive folder + Slack channels don't auto-create → VA never sees the new client.

**Mitigation:** short-term, add a Pipeline → DM Andrew workflow that fires on any move-to-Won ("Create Client + Onboarding now"). Medium-term, rebuild the workflow clean (Wave 2 candidate).

### 6.6 LOW — Close webhook subscription can pause
If Close gets 2 consecutive non-2xx from the M2 webhook, subscription auto-pauses. Polling backstop exists (12h) but Pipeline will visibly lag.

**Mitigation:** M2 already uses `responseMode: onReceived` for fast 200. Monitor webhook subscription status weekly via Close API.

### 6.7 LOW — Drive folder parent drift
All 4 current client folders are correctly under RequityAI parent (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`). If someone moves a folder or deletes the parent, `BegEckXSgXmVffX2` will happily create new folders wherever its hard-coded parent points.

**Mitigation:** hard-code the parent ID as an environment variable in n8n, not in node config. Weekly assert: all client folders have this parent.

### 6.8 LOW — n8n API key rotation
Current key has no expiration (verified). Prior key was 30-day. Operational habit of picking "No expiration" is set in memory.

**Mitigation:** already in place (see `feedback_no_timed_api_keys.md`).

---

## 7. RECOMMENDED IMMEDIATE SEQUENCE (Mon Apr 20)

The smallest first step that closes the VA-ready gap:

**Step 1 — Fix Blocker 1 workflow #1 only (~20 min)**
Start with `Zv2PYFdMiBDCLcZV` (Form Submitted Watcher) because it unblocks the whole onboarding chain. Change appId from Clients to Onboarding, re-map downstream `.client` references, deploy, watch 2 executions. If clean, repeat for the other three.

**Step 2 — Seed one real Campaign Build (~15 min)**
Pick one of the 4 existing clients whose onboarding is closest to done. Walk them through last step manually, let Prerequisites Met fire the first real Campaign + Task. This gives the VA a real first task and validates the whole Stage 2 → Stage 3 chain end-to-end.

**Step 3 — Hand VA the SOP list + `/done` primer (~10 min)**
Write a single Slack message to the VA with: the `#team-tasks` channel pin, the 3-slash-command cheat sheet, and the link to the Campaign Build SOP. That's their onboarding.

**Total: ~45 min to VA-ready once the 4 watchers are fixed.**

Then 3a + 3b can wait 48h; they don't block VA work.

---

## 8. What I did NOT test (known gaps in this audit)

- **Windsor AI data freshness** — confirmed workflow active + last success, didn't verify values match FB Ads manager.
- **Onboarding form itself** — the public form link wasn't tested for submission; only the downstream Form Watcher (which is broken anyway).
- **Close webhook subscription status from Close side** — checked from n8n side (receives events). Didn't confirm subscription `whsub_3wzlFrsrVJP0Gh9HeSQ0jX` still shows `status: active` in Close admin.
- **Calendly M3** — parked, not tested.
- **VA self-serve onboarding guide** — not audited, doesn't exist yet in Drive that I could find.
- **Financial app integrity** — opened schema, didn't audit records.

---

## 9. Files referenced

- Master state: `AgencyOS_Current_State.md`
- Memory index: `.auto-memory/MEMORY.md`
- Zombie RCA: `.auto-memory/project_zombie_trigger_incident_apr19.md`
- Close retirement: `.auto-memory/project_close_pipeline_retired_apr19.md`
- M2 webhook live: `.auto-memory/project_m2_webhook_live.md`
- Apr 19 audit status: `.auto-memory/project_agencyos_status_apr17.md`
- n8n+SS bug checklist: `.auto-memory/feedback_n8n_smartsuite_bugs.md`

---

**End of audit. Next action: Blocker 1, workflow 1 (Form Submitted Watcher). 20 min. Then everything else cascades.**
