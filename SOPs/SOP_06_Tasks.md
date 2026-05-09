# ✅ Tasks App — How to Use It

**Purpose:** The VA's single work queue. Every action item for every client lives here.
**Who uses this:** VAs (work tasks), n8n (creates tasks automatically), Andrew (monitors).
**Your default view:** My Queue ← THIS IS YOUR HOME SCREEN

---

## What This App Is For

The Tasks app is where VAs go to find out what to do. Every task in here was created by n8n automatically based on what's happening in the system. You don't need to wonder "what should I work on?" — open **My Queue** and work top to bottom.

> 🎯 Rule: If it's not in Tasks, it's not a priority. Work the queue, don't invent work.

---

## Your Daily Workflow (VA)

1. Open SmartSuite → go to **Tasks** app → **My Queue** view.
2. The queue is sorted by **Priority** (Urgent → High → Normal → Low), then by **Due Date**.
3. Start at the top. Open the first task.
4. Read the task name, linked client, and any notes.
5. Do the work.
6. Update the **Status** to **Done** when complete.
7. Move to the next task.

That's it. Top to bottom. Do not skip tasks without a reason.

---

## Task Types — What They Mean

These are the 15 types of tasks you'll see in your queue. Each one tells you what kind of work is needed.

| Task Type | What It Means |
|---|---|
| **Set Up Ad Account Access** | Get access to the client's Meta Business Portfolio and confirm the ad account is visible. Send the access guide if the client hasn't granted access yet. |
| **Set Up Lead Forms** | Set up Facebook Lead Centre and connect it to the client's CRM/destination. Confirm leads flow correctly. |
| **Request Videos** | Send the client the video recording brief and follow up until videos are received. |
| **Upload Creative** | Client has sent raw videos. Move them from the Raw Video folder to the Ad Creative folder in Google Drive once edited and ready. |
| **Write Script** | Edit/finalize an AI-generated script. Claude writes the draft, VA reviews and edits for the client's voice. |
| **Admin** | General admin task. Always check the Notes field for context. |
| **Build Campaign (CSV Import)** | Build campaigns using the CSV import method — the primary method for duplicating campaigns across clients at scale. Follow the Campaign SOP. |
| **Build Campaign (Manual)** | Build a single campaign manually in Ads Manager and SmartSuite. Follow the Campaign SOP. |
| **QA Campaign** | Run through the 9-point QA checklist before publishing (see Campaigns SOP). |
| **Launch Campaign** | Publish the approved campaign in Ads Manager. Update SmartSuite Status to Live. Set Launch Date. |
| **Campaign Review** | Review a campaign flagged by n8n/Campaign Intelligence Agent for a performance check (see Optimization SOP). |
| **Cut / Pause Campaign** | Pause or kill an underperforming campaign as flagged by the Intelligence Agent. Update Status to Paused or Cut. |
| **Create Retargeting Audiences** | Create custom audiences in Ads Manager. The Campaign Intelligence Agent creates this task with specific specs: which client, FB page, percentage thresholds, and lookback window. Follow the specs in the Notes field exactly. |
| **Update SmartSuite Records** | Update records in SmartSuite as instructed. Check Notes for which app/record/fields to update. |
| **Escalation Follow-Up** | A blocker or issue has been escalated. Read the Notes field carefully and follow up with the relevant person. |

---

## How to Work a Task (Step by Step)

1. Open **My Queue**.
2. Click the top task to open it.
3. Read:
   - **Task** name — what you're doing
   - **Client** link — which client this is for. Click through to see their details.
   - **Campaign** link (if applicable) — which campaign this relates to.
   - **Type** — confirms the type of work
   - **Priority** — Urgent means do it now before anything else
   - **Due Date** — when it needs to be done by
   - **Notes** — any specific instructions or context
4. Do the work (in Ads Manager, the Campaigns app, or wherever applicable).
5. When done:
   - Change **Status** → **Done**
   - If you can't complete it, change **Status** → **Blocked** and fill in the **Blocker Notes**
6. Move to the next task in the queue.

---

## If You're Blocked

A task is **Blocked** when you cannot complete it due to something outside your control.

1. Change **Status** → **Blocked**
2. Fill in **Blocker Notes** — describe what's blocking you. Be specific so Andrew can unblock it.
3. Send a message to Andrew in Slack. Don't just quietly mark it blocked and move on.

Common blockers:
- Client hasn't given access yet
- Client hasn't sent videos yet
- A field in the Campaign record is missing (e.g., no Asset Link)
- Ad account has a policy issue

Once the blocker is resolved, n8n or Andrew will unblock the task and it'll come back to your queue.

---

## Priority Levels — What They Mean

| Priority | What It Means | Response Time |
|---|---|---|
| **Urgent** | Do this before anything else. Something is time-sensitive or blocking the whole client. | Within 1–2 hours |
| **High** | Important. Do today. | Same day |
| **Normal** | Standard work. Do within 24–48 hours. | 1–2 days |
| **Low** | Nice to do but not urgent. Work it when the queue is clear. | 3–5 days |

---

## Task Status — What Each Means

| Status | What It Means |
|---|---|
| **To Do** | Task is in your queue, ready to work. |
| **In Progress** | You've started this task. |
| **Blocked** | You can't complete this due to an external blocker. See above. |
| **Done** | Task is complete. |

> ⚠️ Do not leave tasks as **In Progress** for more than 24 hours without an update. If you're still working on something, add a note and keep the status as In Progress, then message Andrew on Slack.

---

## Key Fields Explained

| Field | What It's For |
|---|---|
| **Task** | The name of the task. Tells you what to do. |
| **Client** | Which client this task is for. Click through to see their details in the Clients app. |
| **Campaign** | Which campaign record this task is related to (if applicable). |
| **Type** | The category of task. Tells you what kind of work it is. |
| **Status** | Where this task is in the workflow: To Do / In Progress / Blocked / Done. |
| **Priority** | Urgent / High / Normal / Low. Work in this order. |
| **Assigned To** | Who owns this task. You should only work tasks assigned to you. |
| **Due Date** | The deadline. Never ignore this. |
| **Blocker Notes** | Only fill in if Status = Blocked. Describe what's blocking you — be specific so Andrew can unblock it. |
| **Notes** | Context, instructions, or links you need to complete the task. Always read this. |

---

## Views

| View | When to Use It |
|---|---|
| **My Queue** | ← YOUR HOME SCREEN. Tasks assigned to you, sorted by priority then due date. |
| **Blocked** | All tasks currently blocked. Check this daily — you may be waiting on something that's been resolved. |
| **Done This Week** | All tasks completed this week. For reference and reporting. |

---

## What NOT to Do

- ❌ Do not create tasks manually. n8n creates tasks. If you think a task is missing, tell Andrew.
- ❌ Do not mark a task Done if you haven't actually completed the work. Be honest.
- ❌ Do not ignore blocked tasks. Flag them to Andrew in Slack and keep checking back.
- ❌ Do not work on tasks assigned to someone else without being asked.
- ❌ Do not skip Urgent tasks to work on easier Normal tasks. Work priority order.
- ❌ Do not delete tasks. Even if a task seems wrong, mark it Done and flag it to Andrew.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| My Queue is empty but I know there's work to do | Check the Onboarding app — there may be steps awaiting completion. Tell Andrew. |
| A task is assigned to me but I don't know what it means | Read the Notes field and the linked Campaign/Client record. If still unclear, ask Andrew. |
| A task was created for the wrong client | Flag to Andrew. Don't move it yourself. |
| I completed work but n8n didn't create the next task | Tell Andrew — the automation may have failed. |
| I see tasks from other clients in My Queue | Check if the Assigned To filter is correct. The view should only show your tasks. |
