# Anthropic API Key Rotation — Runbook (5 clicks)

**Why:** Your Anthropic key `sk-ant-api03-5m7…cAAA` (named `RequityAI-n8n` in the console) is hardcoded as a literal string inside n8n workflow nodes. GitHub's secret scanner caught it during a repo push. Risk is bounded (only you have n8n access right now), but treat the key as compromised and rotate at next clean session.

**How long:** 5 minutes when you're not fried.

## Step 1 — Open the keys page

https://platform.claude.com/settings/keys

(Sign in with the iCloud-linked Google account if needed.)

## Step 2 — Revoke the leaked key

- Find the row labelled **RequityAI-n8n** (it's the one whose key starts `sk-ant-api03-5m7…cAAA`)
- Click the **⋮** (three vertical dots) at the far right of that row
- From the dropdown, click **Delete**
- Confirm in the modal that pops up

## Step 3 — Create the replacement

- Click the **+ Create key** button at the top-right of the page
- Name it `RequityAI-n8n-rotated-2026-05-09` (or whatever date you do this on)
- Click **Create**
- A modal shows the new key as plain text — **one time only**
- Copy it immediately (Cmd-C the value, or use the copy button if there is one)
- Don't close the modal until you've copied it

## Step 4 — Add it to n8n as a Credential (NOT a literal)

This is the part that prevents the same leak happening again.

- Open n8n: https://requityai.app.n8n.cloud
- Click your profile icon (top-right) → **Credentials** (or use the left-nav `Credentials` link)
- Click **Add Credential** → search for `Anthropic` → select **Anthropic API**
- Paste the new key into the API Key field
- Name the credential `Anthropic — RequityAI n8n` (or similar)
- Click **Save**

## Step 5 — Swap workflows from literal to credential

For each workflow that uses the old hardcoded key, edit it to reference the new Credential instead. Memory rule: **deactivate workflow → edit → save → reactivate** (zombies hide in staticData if you edit live triggers).

Workflows known to use Anthropic (verify by grepping each for `sk-ant-`):
- `8tdPtQWO4qDKEjgq` — SmartSuite Sync Agent
- `6TuDo3mqBZSBF667` — Campaign Intelligence Agent
- `5cdMtOByeZVRFS6H` — Slack Ops Supervisor
- `iM5CNWHLS2UIIJ34` — Decision Router

For each:
1. Open the workflow
2. Toggle **Active → Off**
3. Open the node that calls Anthropic (HTTP Request or Anthropic node)
4. Change the auth from "Generic / Header / inline" to **Credential** → pick the new Credential you just created
5. Delete the literal `sk-ant-…` value if the field still shows it
6. Save the workflow
7. Toggle **Active → On**
8. Run a test execution to confirm it still works

## Step 6 — Verify the kill on the old key

- Back in https://platform.claude.com/settings/keys
- The old `RequityAI-n8n` row should be gone
- After ~24 hours, check there's no usage on it (would show as failed calls in your Anthropic logs if anything is still trying to use it)

## Same hygiene for two other secrets in the same workflows

While you're cleaning up:
- **Slack bot token** `xoxb-9815813665076-…` — hardcoded in the M5 Code node per memory. Same pattern: rotate (in Slack admin), add as n8n Credential, swap.
- **SmartSuite API token** `716c2356a4f…` — likely hardcoded in HTTP Request nodes that call SS. Same pattern: rotate (in SS profile → API access), add as n8n Credential, swap.

## When you're done

Delete this runbook from the repo (or move to `_archive/`). It's not VA-facing material.

Also delete `_handoff/.env_audit` from your Mac — credentials are gitignored but the file itself shouldn't sit around once the audit is done.
