# 🚦 Onboarding App — How to Use It

**Purpose:** Track every step a new client must complete before their campaigns can go live.
**Who updates this:** n8n (automatically). Andrew and VAs read it and act on blockers.
**Your default view:** Onboarding Board

---

## What This App Is For

The Onboarding app is the **gate** before campaigns. Every client that gets created from a won deal gets an onboarding record here. n8n tracks progress through each step automatically.

Think of it as a traffic light system:
- 🔴 **Not Started** — hasn't been done yet
- 🟠 **In Progress** — being worked on
- 🟢 **Complete** — done and confirmed

When every step is 🟢 Complete, n8n triggers the campaign build phase and notifies the VA.

**VAs do not manually update these steps.** n8n does. Your job is to read the status and take action if something is blocking a step.

---

## The 5 Phases of Onboarding

### Phase 1: Account Access
Getting the VA access to the client's Meta accounts.

| Step | What Needs to Happen |
|---|---|
| Business Portfolio Access | VA requests access to client's Meta Business Portfolio. Client approves it. |
| Ad Account Visible | The client's ad account appears in the VA's Business Manager. |
| Facebook Page Confirmed | The correct Facebook page has been identified and is accessible. |
| Instagram Connected | The client's IG account is linked to their Facebook page. |
| Meta Ads App Installed | Client has installed the Meta Ads Manager app on their phone (needed for lead notifications). |

### Phase 2: Lead Setup
Making sure leads flow correctly from Facebook to the client.

| Step | What Needs to Happen |
|---|---|
| Leads Access Confirmed | VA can see leads inside the ad account's Lead Centre. |
| Lead Notifications Set | Client is receiving email/push notifications when a new lead comes in. |
| Lead Centre to CRM | Leads are flowing from Facebook Lead Centre to the client's CRM (GoHighLevel, spreadsheet, etc.). |
| Lead Destination Confirmed | Client has confirmed where they want leads to go. |
| FB Lead Centre Connected | Facebook Lead Centre is fully set up and connected. |

### Phase 3: Videos
Getting the client's talking head videos ready for ads.

| Step | What Needs to Happen |
|---|---|
| Video Brief Sent | Andrew or VA has sent the client the video recording brief document. |
| Videos Received | Client has sent back their recorded videos. |
| Videos Edited | Videos have been edited and processed (moved from Raw Video folder to Ad Creative folder). |
| Approved Videos Exist | Videos have been reviewed and are approved for use in ads. |

### ~~Phase 4: Audience Build~~ — REMOVED
> Retargeting audiences are NOT created during onboarding. They auto-build from Video Views campaign activity. The Campaign Intelligence Agent monitors when enough video views have accumulated, then creates a "Create Retargeting Audiences" task for the VA with specific specs (which client, page, thresholds, lookback window). See the Campaigns SOP and Tasks SOP for details.

### Phase 4: Campaign Launch
Building, checking, and launching the campaigns.

| Step | What Needs to Happen |
|---|---|
| Campaign Built | VA has built the campaign structure in Ads Manager. |
| QA Passed | Campaign passed the full QA checklist (see Campaigns SOP). |
| Campaign Launched | Campaign has been set to Active and is running. |
| Launch Notification Sent | Client has been notified that their campaign is live. |

---

## How to Read the Onboarding Board

1. Go to the **Onboarding** app.
2. Open the **Onboarding Board** view (Kanban).
3. Each column = a phase (Access Setup → Video Briefing → Awaiting Videos → Videos Received → Campaign Build → QA → Live).
4. Find the client card. Look at what phase they're in.
5. If a client is stuck in a phase, open their record to see which specific steps are still 🔴 or 🟠.

---

## How to Read the Checklist View

1. Switch to the **Checklist** view.
2. This is a grid that shows every client with all 19 steps visible.
3. You'll see a wall of red/orange/green. Any red (🔴) that's been sitting for a while = a blocker.
4. Use **Blocker Notes** field to log why something is stuck.

---

## What the VA Does in This App

The VA's job in the Onboarding app is:
1. **Read** — check what steps are assigned to them (Tasks app will have corresponding tasks for each step).
2. **Action** — complete the actual work (e.g., request access to Meta Business Portfolio, confirm lead centre setup).
3. **Report blockers** — if a step can't be completed (e.g., client hasn't given access), log the reason in **Blocker Notes** and notify Andrew via the Tasks app.

> ⚠️ Do NOT manually change step dropdowns. n8n updates these when the work is confirmed. If you complete a step and n8n hasn't updated it, tell Andrew — there may be a workflow error.

---

## Key Fields Explained

| Field | What It's For |
|---|---|
| **Client Name** | The client this onboarding record belongs to. |
| **Client** | Linked record to the Clients app. |
| **Onboarding Stage** | The current phase: Access Setup / Video Briefing / Awaiting Videos / Videos Received / Campaign Build / QA / Live. n8n sets this automatically. |
| **Onboarding Notes** | General notes about this client's onboarding. Andrew fills this. |
| **Blocker Notes** | What's stopping progress. VA or Andrew fills this when something is stuck. |
| **Onboarding Complete** | Master flag. Goes 🟢 only when all 19 steps are complete. n8n then triggers campaign creation. |

---

## Views

| View | When to Use It |
|---|---|
| **Onboarding Board** | Daily check. See where every client is in the funnel at a glance. |
| **Checklist** | Detailed view. See every step for every client. Spot blockers fast. |

---

## What NOT to Do

- ❌ Do not manually flip step dropdowns to Complete. n8n does this. If a step isn't updating, escalate.
- ❌ Do not skip steps. Every step exists for a reason. Skipping Phase 2 (leads) means the client won't get their leads even if the campaign is live.
- ❌ Do not create onboarding records manually. They're created automatically when a client is added.
- ❌ Do not edit the **Onboarding Stage** field manually. n8n controls this.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Step is complete in Ads Manager but still showing 🔴 in SmartSuite | n8n workflow may have failed. Log in Blocker Notes and tell Andrew. |
| Client has been in "Awaiting Videos" for more than 7 days | Check if the video brief was actually sent. If yes, Andrew needs to follow up with the client. |
| A new client doesn't have an onboarding record | The n8n workflow that creates it may have failed. Tell Andrew immediately. |
| "Onboarding Complete" is still 🔴 but all steps look green | Reload the page. If still wrong, tell Andrew — may be a formula/logic issue. |
