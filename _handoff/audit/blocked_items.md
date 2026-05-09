# Blocked Items — What Needs Live API Access

**Generated:** 2026-05-09
**Status:** These items cannot be resolved without n8n + SmartSuite API credentials. Everything else is unblocked and proceeding.

## What's blocked and why

### 1. n8n workflow inventory (full)
Cannot connect to n8n Cloud API without `N8N_API_KEY`. Specifically blocked:
- Confirming active workflow count (memory says 21 after Apr 26 audit; state doc says 24)
- Pulling each workflow's trigger config + last 14 days of executions
- Identifying zombie scheduleTrigger nodes (3 candidates pending forensics from Apr 19 incident)
- Inspecting the SmartSuite Sync Agent parser (`8tdPtQWO4qDKEjgq`) — its hardcoded valid task type list is the runtime contract
- Verifying Windsor → SmartSuite sync workflow (`ZwXd0unFysJjWl1M`) executions are green post-paid-plan
- Checking M3 (Calendly), M4 (No-Show Bridge), M5 (Deal Won) chain health
- Identifying workflows that reference retired entities (dead channel, retired Close Pipeline writes, retired task types)

### 2. SmartSuite schema dump (all 8 apps)
Cannot connect to SmartSuite API without `SMARTSUITE_API_TOKEN` + `SMARTSUITE_WORKSPACE_ID`. Specifically blocked:
- Tasks app `type` field choices — the canonical task vocabulary that the docs must match
- Onboarding app step field count + labels (resolves the SOP_04 "19 vs 18" question)
- Pipeline app `deal_stage` choices (resolves the SOP_09 "11 with NDM" question vs memory's "10 from Apr 18 fix")
- ConvTracker app `last_call_outcome` choices (memory says expanded to 15 on May 6 — unverified live)
- Clients app `niche` and `status` choices
- Campaigns app `status` and `campaign_type` choices
- Per-app field-level inventory for the doc patching work

### 3. Per-client SmartSuite record audit
Cannot verify:
- Whether all 6 active clients (Slack confirmed 6, state doc says 4) have records in the Clients app
- Whether each Client record has a corresponding Onboarding record (M5 should auto-create on Won)
- Whether `slack_channel_id` and `drive_folder_url` fields are populated on all records
- Whether Pipeline records' `close_lead_id` fields hydrated correctly post-Apr 26 hydration ship

### 4. Windsor AI per-client coverage
Cannot probe Windsor's connected ad accounts list without n8n API access (the workflow node config holds the Windsor connection details).

## What's NOT blocked (proceeding now)

- ✅ Slack channel inventory — done via Slack MCP (see `slack_inventory.md`)
- ✅ Drive parent folder confirmed — done via Drive MCP (see `drive_inventory.md`)
- ⏳ Drive per-client subfolder check — proceeding with Drive MCP
- ⏳ Doc layer cross-reference — proceeding via sub-agent against all 14 docs
- ⏳ SOP markdown patches — proceeding for the confident fixes (channel rename, retired task type removal, CIA dormancy clarification, booking phrasing fix, state doc bump)
- ⏳ VA Plug-and-Play Operator Manual draft — proceeding once doc recon completes

## Smallest unblock action for Andrew

Pick one:

**Option A — paste 3 values into the file I created.** Open `_handoff/.env_audit`, replace 3 `PASTE_...` placeholders with real values. Total time: ~2 minutes if you have the values handy.

**Option B — log into both services in the Chrome browser the extension is connected to.** I'll then navigate to each API page myself and pull the values. Total time: ~3 minutes (two logins).

**Option C — paste keys directly in our chat.** I'll write them to disk immediately and use them. Slightly less secure (sits in conversation history) but fastest if you trust the channel.

Whichever you pick, the audit's remaining 30% completes within 15 minutes after I have the credentials. Until then, the 70% I can do is going.
