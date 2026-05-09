# Security Findings — surfaced during Phase 1 audit

**Generated:** 2026-05-09 during raw API dump sanitization.

## P1 — Anthropic API Key leaked in n8n workflow config

**Severity:** High. Production secret embedded in workflow node JSON.

**Detected by:** GitHub Push Protection (secret scanner) when attempting to commit raw n8n workflow exports.

**Token:** `<REDACTED — see Andrew direct for actual value to revoke>`

**Where it lives:**
- At minimum, embedded in workflow `8tdPtQWO4qDKEjgq` (SmartSuite Sync Agent — Slack /update Parser) node config
- Likely also in other Anthropic-using workflows (Campaign Intelligence Agent `6TuDo3mqBZSBF667`, Slack Ops Supervisor `5cdMtOByeZVRFS6H`, Decision Router `iM5CNWHLS2UIIJ34`) — verify by grepping the live workflow set for `sk-ant-`

**Why this matters:**
1. Anyone with read access to n8n workflows in your instance can see the live key
2. The key is billed against Andrew's Anthropic account — exfil = uncapped spend
3. Hardcoded secrets cannot be rotated atomically — rotation requires a workflow edit per occurrence
4. n8n has a credential abstraction (`Credentials` storage) specifically for this — using literals in node `parameters` defeats it

**Remediation (in order):**
1. Rotate the leaked key in Anthropic console: https://console.anthropic.com/settings/keys → revoke `<REDACTED — see Andrew direct for actual value to revoke>` → mint replacement
2. Create an n8n Credential of type `Anthropic API` with the new key. Get its credential ID
3. For each workflow using the literal key, edit the node to reference the Credential instead of the literal
4. Save + reactivate workflows (per memory rule: deactivate → edit → reactivate to avoid zombie schedulers)
5. Verify each affected workflow runs green after the swap

**Other secrets to scrub from workflows the same way:**
- Slack bot token `<REDACTED_SLACK_BOT_TOKEN>` (M5 Code node, hardcoded per memory)
- SmartSuite API token `<REDACTED_SS_TOKEN>` (likely embedded in HTTP Request nodes) → use n8n SmartSuite credential
- n8n's own API key `<REDACTED_N8N_JWT>` if any workflow self-calls n8n

## P2 — Old n8n API key expiry was tracked in repo doc

**Severity:** Low. Operational hygiene, not a leak.

**Detected:** `AgencyOS_Build_Status_April13_2026.md` referenced the previous JWT that expired 2026-04-29. Current key (`signal-new-never-expires`) has no expiry per memory `reference_n8n_api_key.md`.

**Action:** No action — the expired key is dead. Memory entry already tracks the current state.

## Notes on this audit's data handling

- All raw dumps in `_handoff/audit/raw/` have been sanitized before commit
- Replaced patterns: JWTs, Slack `xoxb-/xoxp-/xapp-`, OpenAI `sk-`/`sk-proj-`, Anthropic `sk-ant-`, GitHub `ghp_`, Google `AIza`, AWS `AKIA`, generic 40-char hex, 64-char hex
- Replacements preserve JSON structure and field count — CC can still parse field schemas, choice lists, node connections, workflow shape
- If CC encounters a `<REDACTED_*>` placeholder in a context that needs the real value, escalate — Andrew rotates the secret first, then we re-fetch
