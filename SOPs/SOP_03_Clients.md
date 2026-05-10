# 👤 Clients App — How to Use It

**App:** Clients (`69ce5f18cb8a07430bfee02d`, slug `shybuqst`)
**Last updated:** 2026-05-10
**Purpose:** The master directory of every client — who they are, their account details, and their current status.
**Who uses this:** Andrew (manages), VAs (read-only reference).
**Your default view:** Dashboard
**Source of truth:** Live SmartSuite Clients app. Canonical status field is `status` (labelled "Status (OLD)" in UI — the legacy label is cosmetic). The duplicate `client_status` field is deprecated; ignore it.

---

## What This App Is For

The Clients app is the **source of truth** for client information. It stores everything about who a client is — their contact details, their Facebook/Meta account IDs, their status, and links to everything else in the system.

**What this app is NOT:**
- It is NOT where you track onboarding progress → that's the **Onboarding** app
- It is NOT where you build campaigns → that's the **Campaigns** app
- It is NOT where you manage tasks → that's the **Tasks** app

---

## How a Client Record Gets Created

> ⚠️ **You do NOT create client records manually.**

When a deal is marked **Won** in the Pipeline app, the **M5 Deal Won workflow** (`A31jYsKR3aETSusC`) atomically creates everything within ~30 seconds:
- A new **Client** record here, hydrated with deal info + Close CRM context (company, phone, lead reference)
- An **Onboarding** record bi-linked to the Client
- The Google Drive folder structure: `RequityAI/<Client>/Raw Video/` + `Ad Creative/`
- Two Slack channels: `#team-<slug>` (private, internal) and `#client-<slug>` (defaults **private** — Andrew flips public manually after the client is invited as a guest)
- The niche-aware welcome doc (script library + recording brief) posted into `#team-<slug>`
- A confirmation post in `#team-operations`

Andrew fills in account-specific details (Meta IDs, Facebook page, etc.) as the client completes their setup.

---

## Client Status — What Each Means

The canonical field is **Status** (slug `status`, labelled "Status (OLD)" in the SS UI — the legacy label is cosmetic). A second field, **Client Status** (slug `client_status`), is **deprecated** — every automation writes only to `status`. Ignore Client Status entirely.

| Status | What It Means |
|---|---|
| **Onboarding** | Client is new. Onboarding steps are in progress. Campaigns not yet live. |
| **Active** | Campaigns are live. Client is in the monthly retainer phase. |
| **Paused** | Campaigns are paused (e.g., client is travelling, budget pause). |
| **Churned** | Client has left. Keep the record — don't delete it. |

---

## How to Update a Client Record (VA)

VAs reference client records to find account IDs and contact info. Here's how:

1. Go to the **Clients** app.
2. Use the **Dashboard** view.
3. Find the client you're looking for (search by business name or scroll).
4. Click the record to open it.
5. **Read-only for VAs** — find the info you need:
   - **Ad Account ID** → for building campaigns in Ads Manager
   - **Facebook Page URL** → to confirm the correct page
   - **Business Portfolio ID** → for access requests
   - **Drive Folder URL** → to find the client's scripts and creative assets
6. Do NOT edit any fields unless Andrew has specifically instructed you to.

---

## How to Update a Client Record (Andrew)

When a client completes a setup step, update their record:

1. Open the client record.
2. Update the relevant field (e.g., add their **Ad Account ID** once they've shared it).
3. If their status changes (e.g., they go from Onboarding → Active), update the **Status** field.
4. Add any important context to the **Notes** field.

---

## Key Fields Explained

| Field | What It's For |
|---|---|
| **Business Name** | The primary identifier. Use their actual business name. |
| **Status** | Onboarding / Active / Paused / Churned. Always keep this current. |
| **Niche** | REI (real estate investor wholesaler) / Notes (notes business) / Other. Important — Ritsel Homes is Notes, not REI. |
| **Market / Region** | Their geographic target market (e.g., "Phoenix, AZ" or "Dallas-Fort Worth"). |
| **Ad Account ID** | The Facebook Ad Account ID. Find this in Meta Business Manager. Format: numbers only. |
| **Business Portfolio ID** | The Meta Business Portfolio ID. Needed for the VA to request access. |
| **Facebook Page URL** | The full URL to their Facebook business page. |
| **Drive Folder URL** | Link to their Google Drive folder with scripts and creative assets. |
| **Slack Channel ID** | Used by n8n to send notifications. M5 populates this with the `#team-<slug>` (private internal) channel ID at Won. |
| **Client Slack Channel ID** | The `#client-<slug>` (external) channel ID. Defaults to private at creation; Andrew flips public after inviting the client as a guest. |
| **Assigned VA** | Which VA is handling this client's campaigns. |
| **Link to Onboarding** | Connects to the Onboarding app record. Auto-created by n8n. |
| **Link to Campaigns** | Connects to all campaign records for this client. |
| **Live Campaigns** | Auto-counted from linked campaigns. Shows how many are currently live. |
| **Open Tasks** | Auto-counted from linked tasks. Shows how many VA tasks are pending. |

---

## Views

| View | When to Use It |
|---|---|
| **Dashboard** | Main view. All clients with status, live campaigns, open tasks at a glance. |
| **Client Onboarding Form** | The form new clients fill out. Do not edit this view. |

---

## What NOT to Do

- ❌ Do not create client records manually. Win the deal in Pipeline → n8n creates the record.
- ❌ Do not delete client records. Even churned clients stay in the system as historical data.
- ❌ Do not edit the Slack Channel ID unless Andrew has told you the correct ID.
- ❌ VAs: do not change the Status field. Only Andrew manages status changes.
- ❌ Do not store video scripts or creative assets in this app. Those go in Google Drive. Put the link in Drive Folder URL.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Client record wasn't created after a deal was Won | Check #team-operations in Slack for an error. Tell Andrew. |
| Ad Account ID is blank | The client hasn't shared it yet. Check the Onboarding app for the step status. |
| Client shows wrong status | Flag to Andrew — only Andrew changes status. |
| Drive Folder URL is empty | The client's Google Drive folder hasn't been set up yet. Check with Andrew. |
