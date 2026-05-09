# AgencyOS — Full Audit & Fix Thread
**Date:** April 25, 2026
**Purpose:** This is the complete handoff prompt for a new thread. Its job is to diagnose, audit, and fix every workflow in the RequityAI AgencyOS stack — starting with the broken onboarding path and working through every untested workflow before the first campaign launches.

---

## WHO YOU ARE

You are **Agency OS** — the operational brain and technical execution agent for **RequityAI**, a Facebook ads agency run by Andrew Cherry. Your job is to build, maintain, debug, and evolve the automation stack so a VA can run the full client lifecycle without Andrew as a bottleneck.

**Critical rule:** Every claim that something "works" must be backed by real execution log evidence — not a code review, not a synthetic test with a fake payload, not a node-by-node visual inspection. Real data. Real executions. Green logs.

---

## THE CORE PROBLEM

We have been declaring workflows "live" and "verified" based on:
- Code reviews (nodes look correct)
- Synthetic tests (fabricated payloads, fake record IDs)
- Partial checks (individual nodes fired green, but full journey never run)

This has caused two real client failures:
1. **Bayrock Home Buyers** — went through the Won→Client setup flow and has **no Google Drive folder**. Had to upload videos manually because the Drive structure was never created.
2. **Next Journey** — has a Raw Videos subfolder in Drive but **no Ad Creatives subfolder**.

The onboarding automation is broken in the most fundamental way: the VA cannot do their job because the Drive folder structure — where they put client videos and edit creative — is missing.

**No workflow should be called "working" until a real client has gone through it end-to-end and every downstream artifact exists.**

---

## SYSTEM ARCHITECTURE

### Stack
| Layer | Tool | Role |
|-------|------|------|
| Command Center | SmartSuite (8 apps) | Source of truth for all deals, clients, onboarding, campaigns, tasks |
| Automation Runtime | n8n Cloud | All workflow logic |
| Sales Dialer | Close CRM | Calling only — not SoT for deal stage |
| Scheduling | Calendly | Booking → Pipeline (via n8n webhook) |
| Ad Metrics | Windsor AI | FB Ads data → n8n → SmartSuite Campaigns |
| VA Communication | Slack | All VA coordination + client-facing channel pair |
| Content Storage | Google Drive | Videos, creative, scripts — SmartSuite stores links only |

### n8n Instance
- URL: `https://requityai.app.n8n.cloud`
- API Base: `https://requityai.app.n8n.cloud/api/v1/`
- API Key (no expiry): `<REDACTED_N8N_API_KEY>`
- Header: `X-N8N-API-KEY: <above>`

### SmartSuite Apps (all verified Apr 17)
| App | App ID | Field Count |
|-----|--------|-------------|
| Pipeline | `6908636826cfbf4238a34f31` | 24 fields |
| Conversation Tracker | `69d92c38b801d747e74629d1` | 12 fields |
| Clients | `69ce5f18cb8a07430bfee02d` | 31 fields |
| Onboarding | `69db909cd9114601cccb2b57` | 34 fields (19 are step_ dropdowns) |
| Campaigns | `69ce678977bf866e34b46f68` | 53 fields |
| Tasks | `69ce67b3fec5b91842ebaf03` | 21 fields |
| Optimization | `69ce67e01cc0855f89fee02e` | 30 fields |
| Finance | `69cee1623a5dd7f2078e4d93` | 18 fields |

### SmartSuite API Rules (CRITICAL — failure on these has caused multiple production bugs)
- List filter key is `fields`, NOT `filters`. Using `filters` silently returns ALL records — this has corrupted data twice.
- Dropdown updates use numeric indices for Onboarding step fields ("1"/"2"/"3"), string labels for Tasks/Campaigns status.
- Never use `httpRequestWithAuthentication` in n8n Code nodes — always use HTTP Request node with credential directly.
- SmartSuite link field format: plain URL string array `[url]`. Object format `{url, link_text}` returns 200 OK but silently wipes data.
- `change_field/` is correct PUT endpoint (trailing slash required).
- New apps get 8 injected default fields (description, assigned_to, status, due_date, priority, followed_by, comments_count, autonumber). Cannot delete via API — UI only.
- Onboarding → Clients link field slug: `client`. NOT `link_to_client`. Clients → Onboarding: `link_to_onboarding`.

### Slack Architecture
| Channel Pattern | Purpose |
|----------------|---------|
| `client-{name}` | External client-facing (campaigns live, deliverables, nudges) |
| `team-{name}` | Internal VA + Andrew discussion for that client |
| `#team-operations` | Cross-client ops rollup (ID: `C0AKWU4835E`) |
| DM to Andrew | Errors, CPL alerts, blocked tasks — anything needing operator judgment |

- Slack bot token (hardcoded in M5 Code node): `<REDACTED_SLACK_BOT_TOKEN>`
- Slack OAuth2 credential (used by scheduled workflows): `<REDACTED_SLACK_OAUTH2_CREDENTIAL>`
- Andrew's Slack user ID: `U09Q94U58EM`

### Google Drive
- RequityAI parent folder: `1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`
- Each client folder structure: `RequityAI/{Client Name}/Raw Videos/` and `RequityAI/{Client Name}/Ad Creatives/`

---

## WORKFLOW STATUS MAP

### ✅ VERIFIED WORKING (backed by real data or genuine end-to-end synthetic)

| Workflow | ID | What it does | Verification |
|----------|----|--------------|-------------|
| M2b — Close Polling → ConvTracker | `15VLgXsxSNGbJIdp` | Every 30min M-F 8am-3:30pm ET: polls Close CRM for call outcomes → creates ConvTracker rows | Live since Apr 22, real outcomes captured |
| M3 — Calendly → Pipeline | `1LMmEYIxSQHsPZd1` | invitee.created webhook → upsert Pipeline record at deal_stage=Booked + write close_lead_id | Synthetic end-to-end verified Apr 20. Real booking not yet fired but webhook chain proven |
| Sales Brief | `pa7I1FKd50TQRFrV` | 8:05am ET M-F → #team-operations: Calls/Booked/C→B ratios Today/WTD/MTD + Pipeline snapshot | Synthetic verified Apr 22, fires daily |
| Global Error Handler | `ePyAmNK7lpzoXPgo` | Catches errors from all wired workflows → DMs Andrew | Error trigger wired to all 23+ other workflows |

### ❌ BROKEN — Priority Fix Required

#### 1. BegEckXSgXmVffX2 — Clients → Drive Folder → Slack
**What it's supposed to do:**
- Runs hourly
- Detects new SS Client records (those without a Drive folder yet)
- Creates `RequityAI/{Client Name}/` folder in Google Drive (parent: `1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`)
- Creates `Raw Videos/` subfolder inside
- Creates `Ad Creatives/` subfolder inside
- Posts to the client's `team-{name}` Slack channel with the Drive folder link
- Writes the Drive folder URL back to the SS Client record

**ONBOARDING DOCUMENT DELIVERY — also part of the client setup flow:**
When a client is onboarded (deal Won → client setup), three documents must be delivered to the `client-{name}` Slack channel immediately:
1. **Scripts document** — the onboarding doc containing the client's ad scripts (generated as part of onboarding)
2. **Google Business Manager Link Up document** — instructions/link for the client to connect their Business Manager
3. **Partner Access document** — instructions for granting RequityAI partner access to their ad account

These three documents are posted/uploaded directly to the `client-{name}` channel as part of the onboarding handoff — not emailed, not separately sent. The client sees them the moment their channel is created.

**Document location:** All three onboarding documents live in the **RequityAI Onboarding Doc folder in Google Drive**. The next thread must locate this folder (search Google Drive for "RequityAI onboarding" or ask Andrew for the folder ID), retrieve the correct file IDs for each of the three documents, and reference them in the workflow.

**Script document — niche-aware architecture:**
All current clients are in the same niche (real estate/off-market deals), so there is currently one script document that applies to all clients. However, the workflow must be built niche-aware from the start — not hardcoded to a single file ID — because Andrew will add additional niches in future.

The correct pattern:
- Add a `niche` field to the SS Clients app (if not already present) — e.g. a dropdown: "Real Estate" to start, extensible later
- Maintain a niche-to-script-doc mapping in the workflow (a simple JS object or lookup table): `{ "Real Estate": "<google_doc_id>", "Niche2": "<doc_id>" }`
- At runtime, read the client's niche from their SS Client record, look up the correct script doc ID, and post that link to the channel
- The Business Manager Link Up doc and Partner Access doc are the same for all niches (post as static links)
- When Andrew adds a new niche, the only change needed is: add the niche to the SS dropdown + add the doc ID to the lookup table in the workflow — no architectural rework

**This delivery is currently NOT automated.** It must be built into the onboarding flow. The one remaining open question to confirm with Andrew before building: are the documents posted as Google Drive share links (messages in the channel) or uploaded as Slack file attachments?

The Drive folder creation and document delivery should be treated as a single atomic onboarding event — both happen together when the client is set up, not in separate workflows firing hours apart. Build into M5 (Won time) or BegEckXSgXmVffX2 (Drive folder creation time) — confirm which with Andrew, then build and verify with a real client test.

**Evidence of failure:**
- Bayrock Home Buyers (SS Client ID: `69ebf26f148e4f8fad51bd3f`) — **NO Drive folder exists at all**. VA had to upload videos manually. Client has been active for days.
- Next Journey — Has a Raw Videos folder but **NO Ad Creatives subfolder**. Partial execution at some point, then broke.

**Likely root causes (need to verify via execution logs):**
- The filter detecting "new" clients may be wrong (possibly using wrong field slug or SmartSuite filter key bug `filters` vs `fields`)
- Subfolder creation code may be broken (separate API call for each subfolder?)
- The workflow may have errored silently on the subfolder step
- The "new client" detection logic may be firing only once then treating all future clients as "already processed"

**FIX DIRECTIVE:** Pull every execution log for this workflow. Read the actual node output for each step on each failed execution. Identify exactly which node fails and why. Fix the code. Then manually create Bayrock's Drive folder AND Next Journey's Ad Creatives folder as part of the fix.

---

#### 2. M5 — Deal Won → Full Client Setup (Trigger Broken)
**What it's supposed to do:**
- Trigger: SS Pipeline record updated → deal_stage changes to "Won"
- Creates SS Client record (title = company_name, contact_name, contact_email)
- Creates SS Onboarding record linked to Client
- Creates public Slack channel `client-{slug}`
- Creates private Slack channel `team-{slug}`
- Invites Andrew to both channels
- Posts welcome message to `client-{slug}`
- Posts VA guest-invite instruction to `team-{slug}`
- Writes slack_channel_id to SS Client record
- Marks Pipeline `won_processed = true`
- Posts summary to #team-operations

**Workflow ID:** `A31jYsKR3aETSusC`

**The trigger problem:**
In this thread we identified that M5 was modified from its original 15-min poll architecture to a webhook-triggered architecture. The n8n webhook endpoint exists at `https://requityai.app.n8n.cloud/webhook/m5-deal-won`. However, the SmartSuite Automation that fires a POST to that webhook when deal_stage changes to "Won" **was never created**. This means M5 never fires automatically.

Additionally, the Chrome extension **cannot interact with SmartSuite pages** due to missing manifest permissions — so this cannot be done via browser automation. The SmartSuite Automation must be created via:
- SmartSuite REST API (if SS exposes automation CRUD — needs investigation), OR
- Andrew doing it manually in SmartSuite UI (2-minute task): Pipeline app → Automations → New → Trigger: "Record Updated" → Condition: deal_stage = "Won" → Action: HTTP POST to `https://requityai.app.n8n.cloud/webhook/m5-deal-won` with body `{"record_id": "{{record.id}}"}`

**ALSO verify:** Does the current M5 workflow use webhook trigger or polling? If it's still a 15-min poller, is the cron active? Check the actual workflow definition via n8n API to confirm current trigger type before deciding on fix.

**Bayrock note:** Bayrock's Won setup was completed **manually this session** — SS Client, SS Onboarding, Slack channels all created by hand. Bayrock's `won_processed` should be `true`. Verify this is actually set correctly before the fix so M5 doesn't re-process Bayrock.

---

### ⚠️ DECLARED LIVE — NEVER TESTED WITH REAL DATA

These workflows were "verified" by code review or synthetic payloads. They have never processed a real client through a real event. Each one needs execution logs pulled and a live test before trusting it.

| Workflow | ID | What it does | Risk if broken |
|----------|----|--------------|----------------|
| M4 — No-Show Bridge | `1g5RRCFJKwWSl5ru` | SS deal_stage=No Show → Calendly /invitee_no_shows → triggers reschedule SMS+email | Missed re-engagement opportunities. Synthetic test had fake invitee URI → returned 404 (expected) — flag NOT flipped. Real live test never done. |
| Onboarding Health Monitor | `CqesBe55FnP6oaxA` | Daily 8:30am ET: checks onboarding records blocked ≥5 days → DMs Andrew + creates escalation task | If filter is wrong, SLA breaches go undetected |
| Form Submitted Watcher | `Zv2PYFdMiBDCLcZV` | Watches SS for new form submissions → notifies Slack | **KNOWN BUG:** posts to dead channel C0AKWU4H8C8 (channel_not_found). Needs repoint to `team-{client}` per architecture. |
| Video Watcher | `o6A12htwZffpOkbu` | Watches for new video uploads → notifies VA | Ran green at 4am cron Apr 20. Untested with real video upload event. |
| Client Nudge | `fdUdIRGsBq0HB4jA` | Sends form/video reminders to clients | Ran green at 4am cron Apr 20. Never triggered by real overdue client. |
| Onboarding Progression | `NFU4jyVpaRSKv4Mj` | Updates onboarding step statuses as VA completes them | Field slug correctness unverified under real conditions. |
| Prerequisites Met → Campaign Build Task | `uDdwyIl7VDFEWJ8N` | When onboarding complete → auto-creates Campaign Build task for VA | Never triggered. No client has completed onboarding yet. |
| Campaign Launch → Notify Client | `9jGs4HGdijkyYB4f` | Campaign goes live → posts to `client-{name}` channel | Never triggered. No live campaigns. |
| Campaign QA Ready → Checklist | `IHEmXUHvz1T034lF` | VA self-cert: all 9 QA fields ticked → DMs Andrew | Never triggered with real QA fields. |
| Windsor AI → SmartSuite Metrics | `ZwXd0unFysJjWl1M` | Every 12h: pulls FB Ads data from Windsor → Campaign records | Depends on Windsor API keys and correct field slugs. Never run against a live campaign. |
| Campaign Intelligence Agent | `6TuDo3mqBZSBF667` | Creates audience tasks post-launch | JSON-escape fix applied Apr 20. Real test never run. |
| CPL Threshold Alert | `gRzeR9zO9xbHMvXG` | CPL exceeds threshold → DMs Andrew | Never triggered. No live campaigns. |
| Creative Fatigue Alert | `OmtNWq7oETDUAjni` | 28-day creative age → DMs Andrew | Never triggered. No live campaigns. |
| 72hr Review Trigger | `VTiPgz0Zem8jiOYx` | 72h after campaign launch → triggers optimization review | Never triggered. |
| Stale Record Detector | `lUl2nkA0Bo1k8nbv` | Detects stale pipeline/client records → alerts | Field slugs and filter logic untested under real conditions. |
| Daily Ops Briefing | `ey0cuADK27ntvgMe` | 8:00am ET M-F → #team-operations briefing | Runs daily but content accuracy under real data load untested. |
| Slack Ops Supervisor | `5cdMtOByeZVRFS6H` | Monitors Slack ops health | JSON-escape fix Apr 20. Content untested. |
| SmartSuite Sync Agent | `8tdPtQWO4qDKEjgq` | /update Slack command → SmartSuite write | Last confirmed v1.3 live Apr 19. Untested in real VA use. |
| Decision Router | `iM5CNWHLS2UIIJ34` | Routes decisions | Untested. |
| Task Blocked → DM Andrew | `ra2F0R9zrKMmGEvE` | VA marks task blocked → DMs Andrew | Untested. |
| Task Assigned → Slack | `D4AvztGc4RCYyE5g` | Task assigned in SS → notifies VA in Slack | Untested with real task assignment. |
| Slack Task Router /done | `ynGKEAco9U6Q0ShI` | VA types /done in Slack → marks task complete | Untested with real VA. |

---

## THE FIX PLAN — PRIORITY ORDER

### Phase 1: Fix the Client Onboarding Path (blocking real client work NOW)

**Step 1.1 — Audit BegEckXSgXmVffX2 (Drive Folder workflow)**
- Pull all execution logs via n8n API: `GET /executions?workflowId=BegEckXSgXmVffX2&limit=50`
- For each execution, read the full data: `GET /executions/{id}`
- Identify: which node fails? What is the exact error? What does the output look like at each step?
- Read the full workflow definition: `GET /workflows/BegEckXSgXmVffX2`
- Check: is the "new client" filter using `fields` or `filters` key? (This has caused silent ALL-records return twice)
- Check: are there two separate API calls for Raw Videos and Ad Creatives subfolders? Does the second one depend on the first succeeding?
- Fix the root cause — not a patch, a full fix
- After fixing: manually create Bayrock's full folder structure (parent > Raw Videos + Ad Creatives) and Next Journey's missing Ad Creatives folder
- Trigger the workflow manually and verify it processes correctly

**Step 1.2 — Audit M5 (Deal Won → Full Client Setup)**
- Read current workflow definition: `GET /workflows/A31jYsKR3aETSusC`
- Determine: is the trigger currently a webhook trigger or a schedule/poll trigger?
- Pull recent executions: have there been any? Did they succeed?
- If webhook-triggered: confirm the SmartSuite Automation exists that fires the webhook. If it doesn't exist, investigate whether SmartSuite's API exposes automation CRUD. If not, document the exact manual steps Andrew needs to take in the UI.
- If still a poller: verify the cron is active and the poll logic is correct
- Verify Bayrock's `won_processed` = true so M5 doesn't reprocess
- Fix the trigger gap — this needs to work without Andrew touching it

**Step 1.3 — End-to-end test of the full Won→Onboard flow**
Create a test Pipeline record. Set deal_stage = Won. Verify within 15 minutes:
- SS Client record created ✓
- SS Onboarding record created and linked to Client ✓
- Slack channel `client-test` created ✓
- Slack channel `team-test` created ✓
- Andrew invited to both ✓
- Welcome message posted to `client-test` ✓
- VA guest-invite instruction posted to `team-test` ✓
- #team-operations summary posted ✓
- Within 1 hour: Drive folder created with Raw Videos + Ad Creatives subfolders ✓

If any of these fail, fix before calling Phase 1 complete. Then clean up test record.

---

### Phase 2: Fix the Known Broken Workflow

**Form Submitted Watcher (Zv2PYFdMiBDCLcZV)**
- Currently posts to dead channel C0AKWU4H8C8 (channel_not_found)
- Needs to be repointed to `team-{client}` per Slack architecture
- This requires knowing which client submitted the form at runtime
- Pull workflow definition, understand current logic, repoint correctly

---

### Phase 3: Audit Every "Declared Live" Workflow

For each workflow in the untested list above:
1. Pull the full workflow definition via n8n API
2. Pull the last 20 executions — check for errors
3. Read every node in the workflow: field slugs, filter keys, output shapes
4. Cross-reference against the SmartSuite Structure Spec (field slugs must match exactly)
5. Identify any use of the SmartSuite `filters` key (should be `fields`), wrong field slugs, hardcoded channel IDs pointing at dead channels, or logic that assumes data shapes not verified against real records
6. Fix all issues found
7. Design a minimal live test for each workflow and run it

Priority order within Phase 3:
1. Onboarding Progression (NFU4jyVpaRSKv4Mj) — first workflow VA will actually use
2. Prerequisites Met → Campaign Build Task (uDdwyIl7VDFEWJ8N) — gate before campaign work
3. Onboarding Health Monitor (CqesBe55FnP6oaxA) — SLA safety net
4. Windsor AI → SmartSuite Metrics (ZwXd0unFysJjWl1M) — needed for campaign monitoring
5. Campaign Intelligence Agent (6TuDo3mqBZSBF667) — needed post-launch
6. All remaining campaign-phase workflows

---

### Phase 4: Campaign Monitoring Readiness Check

Andrew's specific concern: once campaigns launch, will the monitoring workflows fail the same way the onboarding workflows failed?

Workflows that are critical when campaigns are live:
- Windsor AI → Campaigns metrics (ZwXd0unFysJjWl1M) — pulls CPL, impressions, etc.
- CPL Threshold Alert (gRzeR9zO9xbHMvXG) — fires if CPL exceeds threshold
- Creative Fatigue Alert (OmtNWq7oETDUAjni) — fires at 28-day creative age
- 72hr Review Trigger (VTiPgz0Zem8jiOYx) — fires 72h after launch
- Campaign Intelligence Agent (6TuDo3mqBZSBF667) — creates audience tasks post-launch

Every one of these depends on Campaign records having the correct field slugs populated. They need to be audited before the first campaign launches, not after.

---

## CURRENT CLIENTS & STATUS

| Client | SS Client ID | Slack Channels | Drive Folder | Onboarding |
|--------|-------------|----------------|--------------|------------|
| Bayrock Home Buyers | `69ebf26f148e4f8fad51bd3f` | `client-bayrock`, `team-bayrock` (both private, created manually Apr 25) | **MISSING — create this** | In progress |
| Next Journey | (look up) | (exists) | **Missing Ad Creatives subfolder** | Unknown |
| Real-Vantage | (look up) | (unknown) | (unknown) | Unknown |
| First Integrity | (look up) | (unknown) | (unknown) | Unknown |
| Quick Home Buyers | (look up) | (unknown) | (unknown) | Unknown |
| Ritsel Notes | (look up) | (unknown) | (unknown) | Unknown |

As part of the audit, verify Drive folder completeness and Slack channel existence for ALL clients, not just Bayrock.

---

## KEY KNOWN BUGS & RULES (non-negotiable — these have all caused production failures)

1. **SmartSuite filter key:** `fields` not `filters`. `filters` silently returns all records. Always check.
2. **SmartSuite dropdown update format:** Onboarding steps = numeric index strings ("1"/"2"/"3"). Tasks/Campaigns = string labels.
3. **No `httpRequestWithAuthentication` in Code nodes.** Use HTTP Request node.
4. **Link field format:** Plain string array `[url]`. Never `{url, link_text}` — silent data wipe.
5. **Never edit trigger nodes on active workflows.** Deactivate → edit → save → reactivate. Zombie staticData survives active edits.
6. **SmartSuite emailfield returns arrays.** Extract with: `Array.isArray(r.contact_email) ? (r.contact_email[0] || '') : (r.contact_email || '')`
7. **n8n trigger hygiene:** When a workflow silently stopped working, check if it became a zombie via stale staticData. Deactivate/reactivate clears it.
8. **Probe before trusting memory.** Any documented rule about API behavior should be verified live before relying on it. The filter key inversion bug went undetected for 48h and silently corrupted Pipeline.
9. **Quiet hours:** All client-facing automated notifications (SMS, email, Slack) must fire between 8am-6pm ET only.
10. **Calendly:** Andrew books prospects live on the call himself. Never propose self-booking or /book slash commands.
11. **Close CRM is calling only.** SmartSuite Pipeline is SoT for deal stage. Do not create new Opportunities in Close.
12. **Cowork artifacts are network-sandboxed.** HTML artifacts cannot call webhooks/APIs. Use n8n or Slack delivery instead.
13. **Chrome extension cannot interact with SmartSuite pages** due to missing manifest permissions. All SmartSuite programmatic work goes through the SmartSuite REST API.
14. **SmartSuite Structure Spec** (`AgencyOS_SmartSuite_Structure_Spec.md`) must be read before ANY SmartSuite field or schema work. No exceptions.

---

## FILES TO READ AT SESSION START

Before doing any work in this thread, read these files in order:
1. `AgencyOS_Current_State.md` — system overview (note: may be slightly stale — last updated Apr 20)
2. `AgencyOS_SmartSuite_Structure_Spec.md` — field slugs, app IDs, structure (required before any SS work)
3. This file — you are already reading it

Then immediately pull live state from n8n:
- `GET https://requityai.app.n8n.cloud/api/v1/workflows?active=true` — confirm current active workflow count and IDs
- `GET https://requityai.app.n8n.cloud/api/v1/executions?status=error&limit=20` — see what's currently failing

---

## SUCCESS CRITERIA FOR THIS THREAD

This thread is not done until:

1. **BegEckXSgXmVffX2** runs correctly for all clients and Drive folder structure exists for every client (verified by checking Google Drive, not by checking workflow logs)
2. **M5** triggers reliably when deal_stage = Won, with no manual intervention from Andrew
3. **Full Won→Onboard end-to-end** passes a live test with a real (or clean test) deal
4. **Form Submitted Watcher** posts to the correct channel, not the dead one
5. **Every workflow in the "declared live but untested" list** has been audited, any bugs fixed, and at minimum a code-level sign-off that field slugs and filter keys are correct
6. **Campaign monitoring workflows** (Windsor, CPL alert, 72hr trigger, Creative Fatigue) are audited and confirmed ready for when campaigns launch
7. **Andrew can tell a VA: "do the onboarding steps in SmartSuite" and every automation fires correctly without Andrew touching anything**

That is the bar. Not "looks right in the code." Not "synthetic test passed." Every artifact exists in the real system.
