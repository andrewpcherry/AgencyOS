# SS Automations — M4 + M5 Build (5 min of clicks)

Two automations to build in SmartSuite UI. Once built, reply with "done" and I'll deactivate both polling crons within minutes.

---

## Automation 1 — M5 Deal Won

**Where:** Pipeline app → Automations tab → New Automation

**Name:** `M5 — Deal Won → n8n`

**Trigger:**
- Type: `When record is updated`
- Condition: `Stage` (deal_stage) `is changed to` `Won`

**Action:**
- Type: `Send webhook` (or "HTTP Request" depending on SS naming)
- Method: `POST`
- URL: `https://requityai.app.n8n.cloud/webhook/m5-deal-won`
- Headers: `Content-Type: application/json`
- Body (JSON):
  ```json
  {"record_id": "{{record.id}}"}
  ```

**Save + activate.**

---

## Automation 2 — M4 No-Show

**Where:** Pipeline app → Automations tab → New Automation

**Name:** `M4 — No Show → n8n`

**Trigger:**
- Type: `When record is updated`
- Condition: `Stage` (deal_stage) `is changed to` `No Show`

**Action:**
- Type: `Send webhook`
- Method: `POST`
- URL: `https://requityai.app.n8n.cloud/webhook/m4-no-show`
- Headers: `Content-Type: application/json`
- Body (JSON):
  ```json
  {"record_id": "{{record.id}}"}
  ```

**Save + activate.**

---

## After you reply "done"

I will:
1. Synthetic-test both webhooks against a temp Pipeline record (verify no regression).
2. Deactivate the M5 schedule trigger (every-15min poll) — workflow stays active, only fires on webhook.
3. Deactivate the M4 schedule trigger (every-15min biz poll) — same.
4. Update memory + state doc.

**Net result:** ~3,700 wasteful executions/month removed. Both flows go from "up to 15 min latency" to "instant."

## Belt-and-suspenders option (recommended for first 48h)

If you'd rather leave the polls running in parallel for 48h to verify the SS Automation actually fires, say so when you reply. I'll keep them running but bump the cadence way down (M5 to every 60 min, M4 to twice/day). After 48h soak with both paths firing the same record, kill the polls.
