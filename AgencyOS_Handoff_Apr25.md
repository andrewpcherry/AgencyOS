# AgencyOS — Handoff: Phase 1+2 Complete, Phase 3+4 Pending

**Date:** 2026-04-25
**Thread scope completed:** Phase 1 (onboarding path) + Phase 2 (Form Watcher fix). Phase 3 (audit declared-live) and Phase 4 (campaign monitoring readiness) deferred to next thread.

---

## What Was Fixed

### Phase 1.1 — Drive Folder Creator (BegEckXSgXmVffX2)

Audited 30+ executions back through Apr 18. Workflow itself is functional (verified end-to-end via execution 2634 on Apr 18 — created folders for "Ed Rooney" client). All 6 current clients now have parent + Raw Videos + Ad Creatives folders in Drive (Bayrock + Next Journey were manually fixed prior to this thread; remediation already in place).

**Architectural weakness noted but not patched:** The "Needs Drive Folder?" filter checks `drive_folder_url.length === 0`. Once that field is set, the workflow ignores the client forever. If subfolder creation fails partway through, partial state is unrecoverable. This is fine in steady state because M5 does NOT write `drive_folder_url`, so new clients always pass the filter. But any future workflow that pre-writes `drive_folder_url` will silently break this chain. If hardening is wanted, change the detection to verify Drive structure (parent + 2 subfolders exist) rather than URL presence.

**Secondary issue noted, not patched:** BegEckXSgXmVffX2's SS list filter uses wrong inner key (`filters` not `fields` per memory rule) — silently passthroughs and returns all clients. Currently doesn't matter (workflow wants all clients) but worth cleaning up.

### Phase 1.2 — M5 (A31jYsKR3aETSusC)

**Root cause of recent failures:** The Code node SS list filter shape was wrong. Used `{fields:[{slug,query,operator}]}` which returns 400 "Input should be a valid string". This had been failing every 5 min since 09:50 UTC on Apr 25. Workflow had been deactivated/edited and redeployed broken between 22:45 Apr 24 and 09:50 Apr 25.

**Fix:** Replaced filter with verified-correct shape: `{filter:{operator:'and',fields:[{field,comparison,value}]}}`. Live-probed against SS Pipeline app — returns 8 Won deals correctly.

**Additional patch:** Webhook node `httpMethod` was unset (defaulted to GET). Patched to POST so the SS Automation can fire JSON body. Both poll mode (exec 3750) and webhook mode (exec 3751) verified success at 10:45–10:46 UTC.

**Outstanding (manual action for Andrew):**
- Create the SS Automation in SmartSuite UI to fire webhook when deal_stage moves to Won. Until that exists, the 5-min poller is the trigger (still works, just up to 5 min latency vs instant).
- SS Automation setup: `Pipeline → Automations → New → Trigger 'Record Updated' → Condition deal_stage='Won' → Action HTTP POST to https://requityai.app.n8n.cloud/webhook/m5-deal-won with body {"record_id":"{{record.id}}"}`

### Phase 1.3 — Niche-Aware Onboarding Doc Delivery

**Discovery:** M5's welcome message already posts 3 hardcoded Drive doc links. All 3 doc IDs verified in Drive:
- Facebook Setup Guide (no Business Portfolio yet): `1erR8MZx_SiuEpqj5wyGPJE6d9I1Q53aB` — niche-agnostic
- Facebook Access Guide (already has Business Portfolio): `18UTBCKYjrMC3ZJGS96xBgXaJm2Samusz` — niche-agnostic
- Video Script Library (Real Estate): `1G0J71V73QDFxRtqqF17vWH7KEjSforXE` — REI-specific

**Niche field already exists** on SS Clients (slug `priority`, label "Niche") with 5 options:
- REI (value="2")
- Notes (value="3")
- Health (value="4")
- Construction (value="5")
- Other (value="6")

**Backfilled:** Bayrock + Next Journey set to REI (both were empty).

**M5 Code patched:**
- `SCRIPT_DOC_BY_NICHE` lookup: `{ 'REI': '1G0J71V73QDFxRtqqF17vWH7KEjSforXE' }` — extensible by adding one line per new niche.
- `NICHE_LABEL_TO_VALUE` map: REI/Notes/Health/Construction/Other → "2"/"3"/"4"/"5"/"6"
- M5 now sets niche on Client create (defaulting to REI if not provided in webhook payload).
- Welcome message script line is template-driven; falls back gracefully to "your custom script library will be shared shortly" if niche has no doc mapping.

**To add a new niche later:** (a) add option to SS Clients `priority` field dropdown via UI; (b) add `'NewNiche': '<doc_id>'` to `SCRIPT_DOC_BY_NICHE` in M5 Code node; (c) extend `NICHE_LABEL_TO_VALUE` map.

### Phase 1.4 — End-to-End Test (verified live)

Created test Pipeline record `ZZ-TEST-DELETE-ME` (deal_stage=Won, won_processed=false). Fired M5 webhook. ALL artifacts confirmed in real systems:

- SS Client `69ec9d973785ec0b2a8bffc0` with niche=REI ✅
- SS Onboarding `69ec9d986ff7da892983cfa9` linked to Client ✅
- Slack public channel `client-zz-test-client` (C0B07JBSS49) ✅
- Slack private channel `team-zz-test-client` (C0AV5977FRT) ✅
- Andrew invited to both ✅
- Welcome message posted with all 3 doc links AND **REI script doc URL correctly resolved** ✅
- Team channel setup message posted ✅
- #team-operations summary posted ✅
- Pipeline `won_processed=true` ✅
- BegEckXSgXmVffX2 hourly cron at 11:00 UTC processed test client → created Drive parent + Raw Videos + Ad Creatives ✅
- `drive_folder_url` written back to Client ✅

**Cleanup:** SS records deleted, Slack channels archived. **Outstanding for Andrew:** trash Drive folder `1VIiP7C8C8nIQccDQg9mcwqEa9UntlldP` (ZZ Test Client) in Google Drive UI — children are deleted with parent.

### Phase 2 — Form Submitted Watcher (Zv2PYFdMiBDCLcZV)

**Bug:** Posted to dead channel C0AKWU4H8C8.

**Fix:** Check Form Completion Code now derives `slug` from client name and resolves `team-{slug}` channel ID via Slack `conversations.list` (private channels) per item. Falls back to #team-operations (C0AKWU4835E) if not found. Slack node `channelId` now expression-driven from `$json.team_channel_id`.

No real form completions had fired since the bug was introduced (Check Form Completion always returned 0 items in recent execution history) — bug was preventive, never surfaced a live alert. Patch is durable for the next real form completion. Test will only run when a client has both `client_ad_account_id` AND `facebook_page_url` populated AND step_ad_account_visible NOT yet "3".

---

## What Was NOT Done (Phase 3+4 — for next thread)

The brief listed 22 declared-live workflows that need real-data verification. These were intentionally deferred per scope decision at thread start.

### Phase 3 — Audit declared-live workflows (priority order)

1. **Onboarding Progression** (`NFU4jyVpaRSKv4Mj`) — field slug verification under real conditions
2. **Prerequisites Met → Auto-Create Campaign Build Task** (`uDdwyIl7VDFEWJ8N`) — never triggered, no client has finished onboarding yet
3. **Onboarding Health Monitor** (`CqesBe55FnP6oaxA`) — daily SLA check, filter logic untested
4. **Windsor AI → SS Metrics** (`ZwXd0unFysJjWl1M`) — never run against live campaign
5. **Campaign Intelligence Agent** (`6TuDo3mqBZSBF667`) — JSON-escape fix Apr 20, real test never run
6. **M4 No-Show Bridge** (`1g5RRCFJKwWSl5ru`) — synthetic test used fake URI (404 expected), real invitee never tested
7. **Video Watcher** (`o6A12htwZffpOkbu`) — green at 4am cron Apr 20, untested with real upload
8. **Client Nudge** (`fdUdIRGsBq0HB4jA`) — green Apr 20, never triggered with real overdue client
9. **Campaign Launch → Notify Client** (`9jGs4HGdijkyYB4f`) — never triggered (no live campaign)
10. **Campaign QA Ready → Checklist** (`IHEmXUHvz1T034lF`) — never triggered with real QA fields
11. **Daily Ops Briefing** (`ey0cuADK27ntvgMe`) — fires daily but content accuracy under real load untested
12. **Slack Ops Supervisor** (`5cdMtOByeZVRFS6H`) — JSON-escape fix Apr 20, content untested
13. **SmartSuite Sync Agent** (`8tdPtQWO4qDKEjgq`) — v1.3 confirmed live Apr 19, untested in real VA use
14. **Decision Router** (`iM5CNWHLS2UIIJ34`) — untested
15. **Stale Record Detector** (`lUl2nkA0Bo1k8nbv`) — filter logic untested under real conditions
16. **Task Blocked → DM Andrew** (`ra2F0R9zrKMmGEvE`) — untested
17. **Task Assigned → Slack** (`D4AvztGc4RCYyE5g`) — untested with real task assignment
18. **Slack Task Router /done** (`ynGKEAco9U6Q0ShI`) — untested with real VA

### Phase 4 — Campaign monitoring readiness (before first launch)

Audit before any live campaign:
- Windsor AI → Campaigns metrics — confirm field slug mapping, hydration shape
- CPL Threshold Alert (`gRzeR9zO9xbHMvXG`) — never triggered, threshold logic unverified
- Creative Fatigue Alert (`OmtNWq7oETDUAjni`) — 28-day age check, never triggered
- 72hr Review Trigger (`VTiPgz0Zem8jiOYx`) — never triggered
- Campaign Intelligence Agent — referenced above

---

## Memory Rules Touched / Reinforced This Session

- **SS list filter shape** memory rule confirmed once again: `{filter:{operator:'and',fields:[{field,comparison,value}]}}`. Both M5 (was wrong, now fixed) and BegEckXSgXmVffX2 (still has wrong inner key `filters` but workflow wants all records anyway) are evidence the rule still bites.
- **Trigger hygiene** memory rule (deactivate → edit → save → reactivate) followed for both M5 and Form Watcher patches.
- **No `httpRequestWithAuthentication` in Code nodes** — both patched workflows use `this.helpers.httpRequest` correctly.
- **Slack channel architecture** (`client-X` external + `team-X` internal pair) preserved.

---

## Confirmed System State After Phase 1+2

- 28 active n8n workflows (vs 24 in old state doc — system has grown).
- 8 Won deals in Pipeline, all `won_processed=true`. M5 will not reprocess.
- 6 active clients, all with complete Drive folder structure.
- M5 trigger: dual-mode (5-min poller + POST webhook). Webhook needs SS Automation manually configured.
- M5 doc delivery: niche-aware. 3 docs auto-posted to client channel on Won. REI is the only niche with a script doc mapped today.
- Form Watcher: routes to per-client team channel by name lookup, falls back to #team-operations.

---

## Outstanding Manual Actions for Andrew

1. **Trash Drive folder** `1VIiP7C8C8nIQccDQg9mcwqEa9UntlldP` (ZZ Test Client) in Google Drive UI.
2. **Create SS Automation** on Pipeline app: Trigger "Record Updated", Condition deal_stage="Won", Action HTTP POST to `https://requityai.app.n8n.cloud/webhook/m5-deal-won` with body `{"record_id":"{{record.id}}"}`. (Without this, M5 still fires within 5 min via poller.)

---

## Open Questions for Future Sessions

- When a non-REI client (Notes, Health, Construction, Other) is Won, M5 will gracefully post a fallback message ("script library will be shared shortly"). When are non-REI script libraries planned to be created? Without them, the VA must manually share scripts for those niches.
- Bayrock and Next Journey's drive_folder_url got written somehow before BegEckXSgXmVffX2 could process them — the path that wrote it isn't fully recoverable from logs. Worth understanding if the system regularly creates "URL set but folders missing" partial states.
