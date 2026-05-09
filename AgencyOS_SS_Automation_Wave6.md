# Wave 6 — SS Automation Conversions (poll → webhook)

**Goal:** Eliminate the last 8 polling cron schedules by replacing each with a SmartSuite Automation that POSTs to a new n8n webhook on the actual state change.

**Status:** Specs ready. Each requires (a) a SmartSuite Automation built in the SS UI and (b) a small n8n workflow rewrite to accept a webhook trigger. Sign off the list, then I'll execute one-by-one and decommission the cron after each goes live.

**Why this matters:** State-change polling is wasteful and adds latency. SS Automation pushes the change instantly to n8n, n8n acts, done. No 8-hour blind window where a VA could be staring at "Task Assigned" with no Slack ping.

---

## The 8 Conversions

For each: trigger condition in SS, what SS Automation should send, what n8n workflow does on receipt.

### 1. Onboarding Progression — `NFU4jyVpaRSKv4Mj`
- **Currently:** daily 8am poll over Onboarding records
- **SS Automation:** trigger on Onboarding record updated where ANY step field changes value
- **Webhook payload:** `{record_id, changed_step, new_value, client_id}`
- **n8n action:** evaluate next-step gating, write checkbox/status updates, post Slack `team-{client}` if step completed

### 2. Prerequisites Met → Auto-Create Campaign Build Task — `uDdwyIl7VDFEWJ8N`
- **Currently:** daily 8am poll over Onboarding records, looking for last step = Done
- **SS Automation:** trigger on Onboarding record updated where `step_19_*` (or whatever the last step slug is) flips to "3"
- **Webhook payload:** `{onboarding_id, client_id}`
- **n8n action:** create Campaign Build Task in Tasks app with all linked refs

### 3. Task Assigned → Slack — `D4AvztGc4RCYyE5g`
- **Currently:** daily 8am poll over Tasks
- **SS Automation:** trigger on Task record updated where `assignee` becomes set OR `status` flips to "Assigned"
- **Webhook payload:** `{task_id, assignee_id, task_type, client_ref}`
- **n8n action:** DM the assignee in Slack with task link + brief; on completion, confirm

### 4. Task Blocked → DM Andrew — `ra2F0R9zrKMmGEvE`
- **Currently:** daily 8am poll over Tasks
- **SS Automation:** trigger on Task record updated where `status` becomes "Blocked"
- **Webhook payload:** `{task_id, blocker_reason, client_ref}`
- **n8n action:** DM Andrew with blocker context

### 5. Campaign QA Ready → Slack Checklist — `IHEmXUHvz1T034lF`
- **Currently:** daily 8am poll over Campaigns
- **SS Automation:** trigger on Campaign record updated where `status` becomes "QA Ready"
- **Webhook payload:** `{campaign_id, client_id, campaign_type}`
- **n8n action:** post QA checklist into `team-{client}` channel, branch for VA self-cert

### 6. Form Submitted Watcher — `Zv2PYFdMiBDCLcZV`
- **Currently:** daily 8am poll over Clients, derives "form just completed" by Onboarding state
- **SS Automation:** trigger on Onboarding record updated where `step_ad_account_visible` flips to "3"
- **Webhook payload:** `{client_id, ad_account_id, page_url}`
- **n8n action:** post form-completion alert to `team-{client}` (existing logic)

### 7. Video Watcher — `o6A12htwZffpOkbu`
- **Currently:** daily 8am poll, but actually checks Drive folders not SS state — this one's harder
- **Two paths:**
  - **(a) Keep as cron** at daily-8am (already throttled). Drive doesn't push events to n8n directly without Drive watch channels. Cost: 30 execs/mo.
  - **(b) Drive watch channel** — set up Google Drive watch on each client's Raw Videos folder. Heavier setup, real-time. Probably overkill.
  - **Recommendation:** leave as daily cron. Negligible waste post-throttle.

### 8. Client Nudge — `fdUdIRGsBq0HB4jA`
- **Currently:** daily 8am poll for clients overdue on Form/Video reminders
- **This one IS legitimately time-based** (overdue = age check, not state change)
- **Recommendation:** leave as daily cron. Already throttled. Not Tier 2.

---

## Refined: 5 actual conversions, not 8

After re-classifying, only 5 of the 8 are true state-change polls worth converting:
1. Onboarding Progression
2. Prerequisites Met
3. Task Assigned
4. Task Blocked
5. Campaign QA Ready
6. Form Submitted Watcher

Video Watcher and Client Nudge are time-based, leave as daily crons.

---

## Build sequence (Andrew approves, I execute)

For each of the 6:
1. Add a webhook trigger node to the n8n workflow (POST `/<wf-name>`).
2. Test webhook fires correctly with synthetic payload.
3. Build the matching SS Automation in SmartSuite UI (HTTP action → n8n webhook).
4. Synthetic SS state-change to verify end-to-end.
5. Deactivate the cron schedule trigger on the n8n workflow.
6. Commit project memory with status.

ETA: ~1–2 hours of work per conversion if SS Automations are simple. ~6–12 hours total. Can run as a single dedicated session.

---

## Approval needed

Sign off on:
- [ ] Convert all 6 (recommended)
- [ ] Convert subset — specify which
- [ ] Hold all conversions for now (current throttled state is acceptable)
