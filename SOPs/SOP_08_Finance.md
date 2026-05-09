# 💰 Finance App — How to Use It

**Purpose:** Track every dollar in and every dollar out for RequityAI.
**Who uses this:** Andrew only. VAs do not touch this app.
**Your default view:** All Records

---

## What This App Is For

The Finance app is the money ledger for the agency. Every setup fee, every monthly retainer, every VA cost, and every software subscription gets logged here. It's not accounting software — it's a running record so Andrew can see at a glance what's been paid, what's outstanding, and how much the agency is making.

---

## Record Types — What Goes Where

| Record Type | What It Covers |
|---|---|
| **Setup Fee** | One-time payment from a new client when they sign. ($1,000–$6,000 depending on the deal) |
| **Retainer** | Monthly recurring payment from an active client. ($1,500–$3,500/month) |
| **Bonus** | Any additional payment from a client outside the standard retainer. |
| **VA Cost** | Money paid to a VA for their work in a given month. |
| **Software Cost** | Tool subscriptions — n8n, SmartSuite, Windsor AI, etc. |
| **Other Income** | Any revenue that doesn't fit Setup Fee, Retainer, or Bonus. |
| **Other Cost** | Any expense that doesn't fit VA Cost or Software Cost. |

---

## How to Log a New Record (Step by Step)

### Logging a Setup Fee (New Client Payment)
1. Go to **Finance** app → **All Records** view.
2. Click **+ Add Record**.
3. Fill in:
   - **Title** → Use format: `[Client Name] — Setup Fee — [Month Year]` (e.g., *Apex Homes — Setup Fee — Apr 2026*)
   - **Record Type** → Setup Fee
   - **Amount** → The dollar amount invoiced
   - **Month** → The month this fee applies to
   - **Invoice Date** → Date you sent the invoice
   - **Payment Status** → **Unpaid** (until you confirm they've paid)
   - **Client** → Link to the client record in the Clients app
   - **Invoice Document** → Upload the invoice file (PDF)
4. Save.
5. When payment is received, open the record and update:
   - **Payment Status** → Paid
   - **Payment Date** → Date you received the payment
   - **Payment Method** → Wire / Stripe / PayPal / Cash / Other

### Logging a Monthly Retainer
1. At the start of each month, create a new record for each active client's retainer.
2. Fill in:
   - **Title** → `[Client Name] — Retainer — [Month Year]` (e.g., *Apex Homes — Retainer — Apr 2026*)
   - **Record Type** → Retainer
   - **Amount** → Their monthly retainer amount (check their Client record)
   - **Month** → The month this retainer covers
   - **Invoice Date** → Date you send the invoice (usually 1st of the month)
   - **Payment Status** → **Unpaid**
   - **Client** → Link to their client record
3. Update Payment Status to **Paid** when received.

### Logging a VA Cost
1. At the end of each month (or when you pay the VA), create a record:
   - **Title** → `VA — [VA Name] — [Month Year]` (e.g., *VA — Maria — Apr 2026*)
   - **Record Type** → VA Cost
   - **Amount** → Amount paid
   - **Month** → Month the work was for
   - **Payment Date** → Date paid
   - **Payment Status** → Paid (if already paid) or Unpaid (if pending)
   - **Payment Method** → How you paid them

### Logging a Software Cost
1. When a software subscription renews or is billed:
   - **Title** → `[Tool Name] — [Month Year]` (e.g., *SmartSuite — Apr 2026*)
   - **Record Type** → Software Cost
   - **Amount** → The billing amount
   - **Month** → Month it applies to
   - **Payment Status** → Paid (these are usually auto-billed)

---

## Payment Status — What Each Means

| Status | What It Means |
|---|---|
| **Unpaid** | Invoice sent. Payment not yet received. |
| **Paid** | Payment received and confirmed. |
| **Overdue** | Invoice is past the due date. Chase it. |
| **N/A** | No payment needed (e.g., internal tracking record). |

---

## Key Fields Explained

| Field | What It's For |
|---|---|
| **Title** | The name of this financial record. Follow the naming format above. |
| **Record Type** | What kind of money movement this is. |
| **Amount** | The dollar value. Always in USD. |
| **Month** | Which month this record belongs to. Used for monthly P&L view. |
| **Invoice Date** | When you sent the invoice. |
| **Payment Status** | Unpaid / Paid / Overdue / N/A. Keep this current. |
| **Payment Date** | The actual date money was received or paid out. |
| **Payment Method** | Wire / Stripe / PayPal / Cash / Other. |
| **Client** | Links this record to the correct client in the Clients app. |
| **Invoice Document** | Upload the actual invoice PDF here for reference. |
| **Notes** | Anything important about this payment (e.g., "Client paid in 2 instalments"). |

---

## How to Check What's Unpaid

1. Go to **Finance** app → **Unpaid** view.
2. This shows every record where Payment Status = Unpaid.
3. If something is overdue (Invoice Date was more than 7 days ago and still unpaid), change Payment Status to **Overdue** and follow up with the client.

---

## Monthly Revenue Check

To see how much came in this month:
1. Go to **All Records** view.
2. Filter by **Month** = current month.
3. Filter by **Record Type** = Setup Fee, Retainer, Bonus (income only).
4. Look at the total Amount column.

> For a quick mental maths check: If you have 5 active clients at $2K/month retainer average = $10K MRR. Add setup fees for new clients on top of that.

---

## Views

| View | When to Use It |
|---|---|
| **All Records** | Full picture of everything in and out. |
| **Unpaid** | What needs chasing. Check this weekly. |

---

## What NOT to Do

- ❌ VAs do not touch this app. Finance is Andrew's responsibility only.
- ❌ Do not delete records. If something was logged incorrectly, mark it N/A and add a note explaining why.
- ❌ Do not leave Payment Status as Unpaid for more than 14 days without chasing the client.
- ❌ Do not log an amount as Paid before you've actually confirmed the payment hit your account.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Client says they paid but record shows Unpaid | Check your bank/Stripe/PayPal. If confirmed, update Payment Status to Paid with the Payment Date. |
| A retainer record is missing for an active client | Create it manually. Check the client's retainer amount in their Client record. |
| A software cost looks higher than expected | Check the tool's billing settings. Flag if there's an unexpected charge. |
| Total revenue doesn't add up | Filter by Month and Record Type to isolate the gap. |
