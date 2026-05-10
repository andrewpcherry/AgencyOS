# 📋 Pipeline App — How to Use It

**App:** Pipeline (`6908636826cfbf4238a34f31`, slug `tb_pipeline`)
**Last updated:** 2026-05-10
**Purpose:** Track every sales deal from first conversation to closed client.
**Who uses this:** Andrew only. VAs do not touch this app.
**Your default view:** Active Deals
**Source of truth:** Live SmartSuite Pipeline app + this markdown SOP. The 10 `deal_stage` values below mirror the live dropdown; if they ever diverge, the live dropdown wins.

---

## What This App Is For

The Pipeline is where Andrew tracks every prospect moving toward becoming a paid client. A record in here is a *deal*, not a client. Once a deal hits **Won**, n8n automatically creates the client record and kicks off onboarding.

---

## Pipeline Stages — What They Mean

| Stage | What It Means |
|---|---|
| Conversation - Positive | Had a good first conversation. They're interested. |
| Follow Up / Reschedule | Need to follow up or rebook a cancelled/missed call. |
| Booked | Discovery call is scheduled. |
| No Show | They didn't show up to the call. Move to Follow Up or Lost. |
| Cancelled | They cancelled. Decide: follow up or move to Lost. |
| Proposal - Decision - Pending | Proposal has been sent. Waiting on their yes/no. |
| Ghosted | They've gone silent after a conversation. |
| Signed - Invoice Sent | Deal is signed. Invoice is out. Waiting on payment. |
| **Won** | ✅ Payment received. This triggers client creation automatically. |
| Lost | Dead deal. Archive it. |

---

## How to Add a New Deal (Step by Step)

1. Go to the **Pipeline** app in the left sidebar.
2. Make sure you're on the **Active Deals** view.
3. Click **+ Add Record** at the bottom of the list (or the + button in the top right).
4. Fill in these fields first:
   - **Deal Name** → Use format: `[Company Name] — [Month Year]` (e.g., *Apex Homes — Apr 2026*)
   - **Company Name** → Their business name
   - **Contact Name** → The person you spoke to
   - **Contact Email** → Their email
   - **Contact Phone** → Their phone number
   - **Stage** → Set to where they currently are in the pipeline
   - **Deal Value** → Estimated total value (setup + 3 months retainer minimum)
   - **Next Action** → What needs to happen next (e.g., *Send proposal*, *Follow up Thursday*)
   - **Next Action Date** → The date that next action needs to happen
5. Add any notes from your conversation in the **Notes** field.
6. Save the record.

---

## How to Move a Deal to Won

1. Open the deal record.
2. Change **Stage** to **Won**.
3. Fill in **Close Reason** if relevant (e.g., *Setup $3K + $2K/mo retainer*).
4. The **M5 Deal Won** workflow fires within ~30 seconds and atomically creates: the Client record, the Onboarding record, the Google Drive folder (`Raw Video/` + `Ad Creative/`), the `#team-<slug>` (private) and `#client-<slug>` Slack channels, and posts the niche-aware welcome brief into the team channel.
5. You'll get a Slack notification in `#team-operations` confirming the chain completed. New `#client-<slug>` channels default to **private** — flip to public manually only after the client has been invited as a guest.

> ⚠️ **Do not manually create a Client record.** Let M5 do it when you mark the deal Won.

---

## How to Move a Deal to Lost

1. Open the deal record.
2. Change **Stage** to **Lost**.
3. Fill in **Close Reason** — always do this. It helps you see patterns over time. (e.g., *Price objection*, *Not enough ad budget*, *Went with another agency*)
4. Done. The record stays for reference in the **Won/Lost** view.

---

## Key Fields Explained

| Field | What to Put Here |
|---|---|
| **Deal Value** | Your best estimate of total contract value. Setup fee + first 3 months retainer. |
| **Health Status** | On Track / At Risk / Stalled. Be honest. At Risk = they've gone quiet or pushed back on price. |
| **Probability %** | Your gut feeling on close likelihood. 0–100%. |
| **Next Action + Next Action Date** | These two fields together = your follow-up system. Always fill both. |
| **ICP Score** | How well this prospect fits the ideal client profile. 1–10. High budget, motivated, has videos = 9–10. |
| **Close Deal ID** | Auto-populated by the Close CRM sync. Don't touch this. |

---

## Views

| View | When to Use It |
|---|---|
| **Active Deals** | Your daily dashboard. All deals not yet Won or Lost. Sorted by Next Action Date. |
| **Won/Lost** | Reference view. Review to spot patterns in what's closing and what's dying. |

---

## What NOT to Do

- ❌ Do not create a Client record manually. Win the deal → n8n handles it.
- ❌ Do not leave Next Action Date blank. If you don't date it, it won't show up when it needs to.
- ❌ Do not leave deals in Ghosted forever. Either move to Lost or schedule a final follow-up.
- ❌ Do not delete deal records. Move to Lost instead.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Marked Won but no Client record appeared | Check Slack #team-operations for an error notification. Tell Andrew. |
| Close CRM sync not working | Check n8n for a failed workflow. Andrew handles this. |
| A deal is missing from Active Deals view | Check if Stage was accidentally set to Won or Lost. |
