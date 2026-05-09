# 💬 Conversation Tracker App — How to Use It

**Purpose:** Log every prospect conversation with its outcome so Andrew can see daily activity and Close CRM stays in sync.
**Who uses this:** Andrew only. VAs do not touch this app.
**Your default view:** Active

---

## What This App Is For

Every time Andrew has a conversation with a prospect — whether it's a cold DM reply, a discovery call, or a follow-up — the outcome gets logged here. This is the daily activity tracker. It also syncs with Close CRM automatically via n8n.

This is NOT where you track deals. That's the Pipeline app. This is where you track *conversations* — one record per interaction.

---

## How to Log a Conversation (Step by Step)

1. Go to the **Conversation Tracker** app.
2. Click **+ Add Record**.
3. Fill in these fields:

   **Company** → The company name of the person you spoke to.

   **Decision Maker** → The name of the person you spoke to.

   **Date** → Today's date (or the date the conversation happened).

   **Outcome** → Pick one:
   - **Interested** — They want to know more. Positive energy. A call is likely.
   - **Maybe** — Neutral. Not a no, but not excited either. Needs more follow-up.
   - **Not Interested** — Clear no. Don't chase this one.

   **Call Booked** → Set to **Yes** if a discovery call was booked as a result of this conversation. Otherwise leave as **No**.

   **Notes** → 1–3 sentences on what was said, any objections, or context for the next follow-up.

4. The **Title** field auto-generates as *"Company — Outcome"*. You don't need to edit it.
5. The **Close Activity ID** field is auto-populated by the n8n sync. Don't touch it.

---

## Key Fields Explained

| Field | What It Means |
|---|---|
| **Outcome** | The result of the conversation. Interested / Maybe / Not Interested. |
| **Call Booked** | Yes/No toggle. Was a discovery call booked from this conversation? |
| **Close Activity ID** | The ID from Close CRM. Used to prevent duplicate entries. Never edit this manually. |
| **Notes** | What happened. Keep it short and useful. |

---

## Outcome vs Call Booked — Important Distinction

These are two separate fields because a conversation can be **Interested** without a call being booked yet (e.g., they replied positively but need to check their calendar). And a call can be booked from a **Maybe** too.

- **Outcome** = their level of interest
- **Call Booked** = did a meeting get scheduled as a direct result?

Always fill in both.

---

## The n8n Sync — What Happens Automatically

The n8n workflow "Close CRM → SmartSuite Conversation Tracker" runs daily. It pulls conversation activity from Close CRM and creates records here automatically. This means:

- If you logged a call in Close CRM, it will appear here automatically overnight.
- If you manually log something here that's already in Close, the Close Activity ID prevents duplicates.
- You can also add conversations manually here for anything not in Close (e.g., a cold DM on Facebook).

---

## Views

| View | When to Use It |
|---|---|
| **Active** | Your main view. Recent conversations sorted by date. |

---

## What NOT to Do

- ❌ Do not edit the **Close Activity ID** field. This is the sync key — touching it will cause duplicate records.
- ❌ Do not leave the **Outcome** field blank. Every record needs an outcome.
- ❌ Do not use this to track deals. That's the Pipeline app. This is for logging conversation activity.
- ❌ Do not delete records. If a conversation was a duplicate, flag it to Andrew.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Duplicate records appearing | Check if Close Activity ID is the same on both. Tell Andrew — the dedup logic may have failed. |
| Records not appearing from Close CRM | The n8n sync may have failed. Check #team-tasks on Slack for error notifications. |
| An outcome looks wrong | Only Andrew edits these. Don't change someone else's logged outcome. |
