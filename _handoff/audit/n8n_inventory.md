# n8n Workflow Inventory — Live Truth (2026-05-09)

**Source:** `_handoff/audit/raw/n8n_workflows.json` (full /api/v1/workflows dump) and `_handoff/audit/raw/n8n_sync_agent.json` (full Sync Agent workflow). Pulled by Andrew on 2026-05-09; sanitized of secrets.

**Headline numbers:**
- **Total workflows: 55** (active + inactive in workspace)
- **Active: 21** ✅ matches `AgencyOS_Architecture_AtoZ_Apr26.md` claim
- **Inactive: 34** ⚠️ — architecture map only acknowledges 6 deactivated workflows. Reality: 28 *more* than docs admit.
- `AgencyOS_Current_State.md` (Apr 20) workflow count of 24 is stale.

---

## Active workflows (21)

### Event-driven (instant)

| Workflow | ID | Trigger | Notes |
|---|---|---|---|
| M3 — Calendly invitee.created → SmartSuite | `1LMmEYIxSQHsPZd1` | webhook | ✅ Live, matches arch map |
| M4 — SS No-Show → Calendly Bridge | `1g5RRCFJKwWSl5ru` | webhook | ✅ Live |
| M5 — Deal Won → Full Client Setup | `A31jYsKR3aETSusC` | webhook | ✅ Live |
| Slack Task Router — /done | `ynGKEAco9U6Q0ShI` | webhook + manual | ✅ Live |
| SmartSuite Sync Agent — /update Parser | `8tdPtQWO4qDKEjgq` | slackTrigger | ✅ Live — see parser extraction below |
| Global Error Handler → DM Andrew | `ePyAmNK7lpzoXPgo` | errorTrigger | ✅ Live, fan-in for all errors |

### Schedule-driven (15)

Note: **all 15 are `scheduleTrigger`-based**. Memory rule about zombie scheduleTriggers (Apr 19 incident) means each one's `staticData` should be considered before any disable/edit operation.

| Workflow | ID | Notes |
|---|---|---|
| M2b — Close Polling → ConvTracker | `15VLgXsxSNGbJIdp` | Every 30m M-F 8a-3p ET. Bridge for broken Close webhook. |
| Daily Ops Briefing — 8am | `ey0cuADK27ntvgMe` | 8am ET → #team-operations |
| Daily Sales Metrics Brief | `pa7I1FKd50TQRFrV` | 8:05am ET M-F. Architecture map names this "Daily Sales Brief" — minor name drift. |
| Onboarding Health Monitor | `CqesBe55FnP6oaxA` | 8:30am ET. ⚠️ References `#team-tasks` — see stale-ref scan. |
| Slack Ops Supervisor | `5cdMtOByeZVRFS6H` | 8am + 8pm ET. ⚠️ References `#team-tasks` (8 matches). |
| Stale Record Detector | `lUl2nkA0Bo1k8nbv` | Daily |
| Onboarding Progression — Checkbox Done → Next Task | `NFU4jyVpaRSKv4Mj` | Daily 8am — name in JSON has UTF-8 corruption (`â` instead of `→`) |
| Prerequisites Met → Auto-Create Campaign Build Task | `uDdwyIl7VDFEWJ8N` | Daily. ⚠️ Still creates "CSV Import Build" tasks (6 matches) — needs M10 patch. Name in JSON has UTF-8 corruption (`â`). |
| SmartSuite → Form Submitted Watcher | `Zv2PYFdMiBDCLcZV` | Daily |
| SmartSuite → Video Watcher | `o6A12htwZffpOkbu` | Daily |
| Client Nudge — Form & Video Reminders | `fdUdIRGsBq0HB4jA` | Daily |
| SmartSuite Clients → Drive Folder → Slack | `BegEckXSgXmVffX2` | Daily 8am (was hourly per arch map) |
| Task Assigned → Slack + Task Complete → Confirm | `D4AvztGc4RCYyE5g` | scheduleTrigger (NOT webhook) — arch map line 359 implies this fires on SS event; live shows it's a poller |
| Task Blocked → DM Andrew | `ra2F0R9zrKMmGEvE` | scheduleTrigger (poller, not event) |
| Campaign QA Ready → Slack Checklist | `IHEmXUHvz1T034lF` | scheduleTrigger. ⚠️ Architecture map §I lists this as DEACTIVATED until first campaign launches. Live shows it ACTIVE. Resolve. |

**Discrepancies vs Apr-26 architecture map (active set):**
- Architecture map §I (line 379) lists **Campaign Intelligence Agent** `6TuDo3mqBZSBF667` as ACTIVE every 12h. Live: **INACTIVE**.
- Architecture map §I (line 380) lists **Decision Router** `iM5CNWHLS2UIIJ34` as ACTIVE every 12h. Live: **INACTIVE**.
- Architecture map §I (line 378) lists **Windsor AI → SS Metrics** `ZwXd0unFysJjWl1M` as ACTIVE every 12h. Live: **INACTIVE**.
- Architecture map §I (line 387) lists **Campaign QA Ready → Checklist** `IHEmXUHvz1T034lF` as DEACTIVATED. Live: **ACTIVE**.
- Architecture map §E line 217 says Task Assigned and §E line 280 says Task Blocked are SS-event-driven. Live shows both are scheduleTrigger pollers.

The architecture map's Apr-26 audit numbers were correct at the time but a second cleanup pass since then has not been documented — likely the campaign-gated workflows that the doc says are reactivated when first campaign launches are still off, plus Campaign Intelligence Agent + Decision Router were deactivated more recently. **Confirm with Andrew (Phase 2 #N1).**

---

## Inactive workflows (34)

Categorized by pattern. Many of these are zombie carryover from earlier builds, broken predecessors that were superseded, or campaign-gated workflows.

### Campaign-gated (await first campaign launch) — 5

These are the legitimate "reactivate when first campaign launches" workflows the architecture map describes:
- `9jGs4HGdijkyYB4f` Campaign Launch → Notify Client in Slack
- `VTiPgz0Zem8jiOYx` 72hr Review Trigger
- `gRzeR9zO9xbHMvXG` CPL Threshold Alert → DM Andrew
- `OmtNWq7oETDUAjni` Creative Fatigue Alert (28-Day Check)
- `ZwXd0unFysJjWl1M` Windsor AI → SmartSuite Metrics (12h) + DM Andrew

Note: arch map said `IHEmXUHvz1T034lF` Campaign QA Ready was in this set. Live shows it's active.

### Recently deactivated (campaign intelligence path)

- `6TuDo3mqBZSBF667` Campaign Intelligence Agent — arch map says active. Now off.
- `iM5CNWHLS2UIIJ34` Decision Router — arch map says active. Now off.
- `bhu2yom6iUt1SfSa` 72hr Optimization Review Creator
- `qYFXgdFG6N9StUkO` Campaign Review Task Auto-Creator (every 7 days from launch)
- `YK0z988p7cqxFqKX` Campaign Goes Live - Set Next Review Date
- `whNlFn46NRMswO6D` Campaign Goes Live → Set Next Action Date (Thursday)

### Replaced predecessors (live duplicate exists with newer ID)

- `dInuMwYxjwcftjSp` **M2 — Close CRM Webhook → SmartSuite (push)** — replaced Apr 22 by `15VLgXsxSNGbJIdp` M2b polling. Self-references are the only mentions. Safe to delete after 7-day soak per Phase 3 §3.0 GREEN→YELLOW guidance.
- `Ikil2vx4jQNR7yxa` M4 — SS No-Show → Calendly Bridge — same name as the active `1g5RRCFJKwWSl5ru`. Inactive predecessor.
- `Gly17Kkp8oUTEyGp` Close CRM → SmartSuite Conversation Tracker — superseded by M2b
- `R4mXec6XM032MMyB` Close CRM → SmartSuite Pipeline Sync — Close-CRM-as-source pattern; retired Apr 19 per memory.
- `HZ18Xb98Szin8OTQ` Deal Won → Create Client + Onboarding (Manual) — superseded by M5
- `9pAsoQqBhRT4HHS6` Client Onboarding — Create Slack Channels — superseded by M5
- `W2GRDMN8xwlQhlqg` Client Onboarding — Slack Trigger — superseded by M5
- `I599mjvYW4ZdkNRf` Won Deal — Auto-Create Onboarding Task Chain — superseded by M5
- `QX0VicX53AzQmHPY` M1_ClientOnboarding_Orchestrator — predecessor to M5
- `7gKYzCvV0zibOWq9` Task Blocked - DM Andrew v2 (With Category + Funnel) — replaced by `ra2F0R9zrKMmGEvE`
- `SDIWZGNRgXFwg81W` Task Notifications v2 - With Category Type Funnel
- `DH5Yx9S2RS6OO6qG` Task Completed → Auto-Set Completed Date
- `KEcx3yQ7kephk0cM` Daily Data Hygiene Check → Stale Records Alert — replaced by Stale Record Detector
- `apbdh284pFlCy2hZ` QA Ready → Create QA Task for Andrew
- `XGVbY2c8ijPoz54w` Recurring Maintenance Tasks
- `PpfpYaSQRcGrJqLe` Weekly Skeleton Tasks — Every Monday 6am
- `G0ITjfkhRZqKIWX4` Windsor Metrics Sync v2 - Daily — superseded by ZwXd0unFysJjWl1M

### Demos / experiments

- `GQwRPVA9iaiZwCQ5` AI Maintenance Agent - Complete Workflow
- `PJaJYLuesPU2oxc7` RequityAI Enterprise Demo - Maintenance + Leasing + Slack
- `9fPbvP6pytQslBD1` Telnyx Listener Webhook
- `TX7laFirjpUrxDoa` Optimization Decision → Notify #operations
- `QGtGJydvWkR6vSCj` Client Communication — Onboarding Updates + Campaign Milestones
- `rtjwykL2X3VwKZxM` Client Report Auto-Generator — 7-Day Cycle from Launch

**Phase 3 cleanup target:** of these 34 inactive, ~20 are clear retirement candidates (replaced predecessors + demos + the M2/M4/M5 lineage of supersessions). Per Phase 3 §3.0 GREEN, those that meet (a) inactive logic, (b) no execution in 14 days, (c) no downstream dependency can be removed/renamed without escalation. **DELETE is YELLOW — deactivated workflows should be deactivated → soak 7d → delete.**

---

## Stale-infra reference scan (across all 55 workflows)

| Pattern | Hits in active | Hits in inactive |
|---|---|---|
| `C0AKWU4H8C8` (dead channel) | 0 | 0 |
| `#team-tasks` (renamed Apr 22 → `#team-operations`) | **2 active** | 2 inactive |
| `Create Retargeting Audiences` task creation | 0 | 0 |
| Old M2 webhook ID `dInuMwYxjwcftjSp` | 0 | 1 (self) |
| `CSV Import` build task | **1 active** (uDdwyIl7VDFEWJ8N, 6 matches) | 0 |
| `#new-clients` channel | 0 | 0 |
| "Manus" reference | 0 | 0 |

**Active workflows with `#team-tasks`:**
- `5cdMtOByeZVRFS6H` Slack Ops Supervisor — 8 matches in JSON. Posts daily ops health to a channel that no longer exists under that name.
- `CqesBe55FnP6oaxA` Onboarding Health Monitor — 2 matches. Same problem.

**Risk:** Slack API will return `channel_not_found` and the workflow's error path fires. Global Error Handler then DMs Andrew. The audit pattern is "alarm-when-broken" not "silent-stop", so there's no data loss — but it's noise that should have been caught when the channel was renamed Apr 22. Both workflows need `s/team-tasks/team-operations/g` in node parameters.

This is a P1 doc-and-code patch for Phase 3 (active workflows touching live data → YELLOW per §3.0). Both workflows should be: deactivated → patched → reactivated, per the zombie-staticData rule.

---

## Sync Agent parser — `8tdPtQWO4qDKEjgq` extraction

**Trigger:** Slack `slackTrigger` on `/update` slash command.

**Architecture:** 2 Code nodes —
1. *Parse /update Message* — splits raw text into `{appName, fields, clientName}` structured object. Strips trailing "Sent using Claude" suffix.
2. *SmartSuite Lookup & Update* — resolves client → record → applies field mapping → PATCHes via SS API.

**Hardcoded vocabulary (extracted verbatim):**

```
APP_MAP — 7 apps:
  tasks, campaigns, onboarding, pipeline, optimization, finance, clients

  ⚠ Missing from parser: Teams, Members, Financial Metrics Dashboard, SOPs.
  VAs cannot /update those four. Confirms VA scope = the 7 documented apps only.

STATUS_MAPS:
  tasks:                 To Do / In Progress / Blocked / Done           ← matches live
  campaigns:             Draft / QA Ready / Live / Paused / Cut / Completed  ← matches live
  clients:               Onboarding / Active / Paused / Churned        ← matches live `status` (the OLD one), NOT `client_status`
  finance_payment:       Paid / Unpaid / Overdue / N/A                  ← matches live
  pipeline:              10 stages exactly matching live deal_stage     ← matches live (resolves M15)
  optimization_decision: Keep Running / Cut / Retarget Test / Lead Ad Candidate / Swap Creative
                                                                        ← matches live (resolves M21)

OB_STEP_MAP — 19 entries:
  All 18 named steps + step_onboarding_complete master flag.
  Includes step_videos_edited (Apr 16 add).
  Matches live SS exactly (resolves M11).

OB_STATUS_MAP:
  not started → 1, in progress → 2, complete → 3
```

**Per-app field handlers:**
- `tasks`: writes `status` and appends to `description`. **Does NOT write `type`.** No canonical task-type list exists in the parser. SOP_06 V2 and SOP_09 V2 both reference "the parser's hardcoded valid task-type list" — that list does not exist. Fabricated.
- `campaigns`: maps `action` → `status` (Build Complete → Draft, QA Ready → QA Ready, Launched → Live, Paused → Paused). Appends to `build_sop_reference`.
- `onboarding`: writes a single `step_*` slug to 1/2/3 based on parsed step + status. Strict — anything not in OB_STEP_MAP is silently dropped.
- `pipeline`: writes `deal_stage` from STATUS_MAPS.pipeline. Appends to `notes`.
- `optimization`: writes `decision` if `action=Review Complete` AND decision is one of the 5 valid values.
- `finance`: maps `action` → `payment_status`. Parses `amount` numerically (strips currency symbols). Appends to `notes`.
- `clients`: only allows `action=Info Update` with explicit field/value pairs. Whitelist: status / niche (→`priority`) / market / contact_name / contact_email / contact_phone / facebook_page_url / instagram_handle / ad_account_id (→`client_ad_account_id`).

**Implications for VA Manual:**
1. `/update` works on 7 apps — VAs cannot use it for Teams, Members, Financial Metrics Dashboard, SOPs.
2. `/update` cannot change Task `type`. If VAs need to recategorize a task (rare), Andrew does it in SS UI.
3. The Onboarding `step:` field name in `/update` must match one of 19 case-insensitive strings (the OB_STEP_MAP keys). Anything else fails silently. Manual must list these 19 exactly.

---

## Cross-system referential integrity (schema-only)

Schema dumps don't include records, so record-level integrity (every Client.slack_channel_id resolves, every Onboarding has a Client link, every active Campaign has a Platform ID) is **probe-pending**.

What we *can* assert from schemas:
- Tasks → Client linked record field exists ✅
- Tasks → Campaign linked record field exists ✅
- Onboarding → Client linked record field exists ✅
- Campaigns → Client linked record field exists ✅
- Optimization → Campaign linked record field exists ✅
- Finance → Client linked record field exists ✅

Andrew can run a record-list dump per app for the Phase 3 verification pass — see Phase 4 validation §13.

---

## Security cross-check

Per `_handoff/audit/security_findings.md`, the P1 leaked-secret pattern is broader than just the Sync Agent. Scan results:

- All 21 active workflows contain `<REDACTED_*>` placeholder markers (2–10 per workflow). Every one originally had hardcoded secrets that the dump-time sanitizer caught.
- No raw secret patterns (sk-ant, xoxb-, JWT, 40-hex tokens) leaked through sanitization. The dump is safe to keep in git.
- For Phase 3 cleanup: every active workflow that has hardcoded secrets needs to be migrated to use n8n Credentials. Per the security note, the rotation order is: rotate at provider → mint n8n credential → swap node references → deactivate-edit-reactivate → verify green.

---

*End of n8n inventory.*
