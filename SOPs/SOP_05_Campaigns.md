# 📣 Campaigns App — How to Use It

**Purpose:** Build, track, and monitor every Facebook ad campaign for every client.
**Who uses this:** VAs (build campaigns, complete QA), n8n (writes metrics automatically), Andrew (monitors performance).
**Your default view:** Build Queue (for VAs) / All Campaigns (for Andrew)

---

## What This App Is For

The Campaigns app is where every Facebook ad campaign lives. Each record = one campaign. VAs build campaigns here and in Ads Manager simultaneously. n8n pulls metrics in automatically via Windsor AI. Andrew monitors performance across all campaigns from here.

*Note: No Facebook pixel is required. All lead capture uses native Facebook Lead Forms (prospects never leave the platform), and retargeting audiences are built from in-platform engagement (video view percentages), not pixel events.*

---

## The 3 Campaign Types

Every client runs a stack of 3 campaign types. Each one serves a different purpose.

| Campaign Type | Audience | Goal |
|---|---|---|
| **Video Views** | Cold — broad audience, no prior interaction required | Get videos in front of distressed sellers. Build the retargeting pool. |
| **Retarget** | Warm — people who watched 25%+ of a Video Views campaign | Different talking-head video, same "comment OPTIONS" CTA. Deepens engagement and pushes viewers toward 75%+ for Lead Ad. |
| **Lead Ad** | Hot — people who watched 75%+ or engaged with content | Capture contact details via Facebook Lead Form. This is the ONLY campaign that collects leads. |

> ⚠️ Retarget and Lead Ad audiences build automatically from Video Views campaign activity. They are NOT manually created during onboarding.

---

## Campaign Naming Convention

Every campaign record must follow this naming format exactly. This is what goes into Ads Manager too.

**Campaign Name:** `[CAMPAIGN TYPE] | [MARKET]`

Examples:
- `VIDEO VIEWS | PHOENIX AZ`
- `RETARGET | DALLAS TX`
- `LEAD AD | ATLANTA GA`

**Ad Set Name:** `[CLIENT CODE] | [AUDIENCE] | [DATE]`

Example: `APEX | 25PCT-VIEWERS | APR2026`

**Ad Name:** `[SCRIPT ID] | [SITUATION] | [VERSION]`

Example: `FC-B2-14 | FORECLOSURE | V1`

> ⚠️ Get the naming convention wrong and the whole reporting system breaks. Follow it exactly.

---

## Campaign Status — What Each Means

| Status | What It Means |
|---|---|
| **Draft** | Campaign record created but not yet built in Ads Manager. |
| **QA Ready** | Campaign is built in Ads Manager and ready for the QA checklist. |
| **Live** | Campaign passed QA and is running. Metrics are being tracked. |
| **Paused** | Campaign is temporarily paused (budget, review, client request). |
| **Cut** | Campaign has been killed — underperforming. Keep the record for reference. |
| **Completed** | Campaign has run its course and ended naturally. |

---

## How to Build a Campaign (VA Step by Step)

You'll get a Task in the Tasks app telling you to build a campaign. Here's what to do:

### Step 1: Open the Campaign Record
1. Go to **Campaigns** app → **Build Queue** view.
2. Find the campaign assigned to you (Status = Draft).
3. Open the record.

### Step 2: Confirm the Setup Info
Check these fields are filled in before you touch Ads Manager:
- **Client** — correct client is linked
- **Market** — geographic market is listed
- **Campaign Type** — Video Views / Retarget / Lead Ad
- **Daily Budget** — dollar amount is set
- **Script Link** — Google Drive link to the video script
- **Asset Link** — Google Drive link to the video file
- **Week** — which week of the quarter (W1–W13)

If any of these are blank, **do not start building**. Add a note to the Task record and tell Andrew what's missing.

### Step 3: Get the Video
1. Click the **Asset Link** to open Google Drive.
2. Download the video file.
3. Confirm it's the right video (matches the Script Link/script ID).

### Step 4: Build in Ads Manager
1. Find the client's Ad Account ID in the **Clients** app (Ad Acct ID field). Log into their Facebook Ads Manager via their Business Portfolio.
2. Create the campaign using the naming convention above.
3. Set the campaign objective:
   - Video Views → **Video Views** objective
   - Retarget → **Engagement** objective
   - Lead Ad → **Leads** objective (uses Facebook Lead Form)
4. Set the audience:
   - Video Views → broad audience (state or major metro, no custom audiences)
   - Retarget → use the 25%/50% video viewer custom audiences (these auto-build from the Video Views campaign — check they exist before proceeding)
   - Lead Ad → use the 75%/95% video viewer custom audiences (also auto-built from Video Views activity)
5. Set the budget to match the **Daily Budget** field.
6. Upload the video.
7. Set the CTA based on campaign type:
   - Video Views → **No CTA button**. The ad copy tells viewers to comment "OPTIONS" for more info. This drives engagement and builds your retargeting pool.
   - Retarget → **No CTA button**. Same approach — ad copy tells viewers to comment "OPTIONS". Uses a different talking-head video to deepen engagement and push viewers toward 75%+ watch time for the Lead Ad.
   - Lead Ad → **Facebook Lead Form**. This is the only campaign that captures contact details. Targets hot viewers (75%/95% video watchers).
8. Set **Special Ad Category = Housing** → ⚠️ THIS IS REQUIRED BY LAW. Never skip this.
9. Do NOT use zip code targeting. Use city/state level only (Facebook Housing category requirement).
10. Turn **CBO (Campaign Budget Optimisation) OFF**.
11. Save as draft in Ads Manager. Do not publish yet — QA first.

### Step 5: Fill in the Campaign Record
Back in SmartSuite, update the campaign record:
- **Campaign Name** → paste the exact campaign name from Ads Manager
- **Ad Set Name** → paste the exact ad set name
- **Ad Name** → paste the exact ad name
- **Platform Campaign ID** → the Facebook Campaign ID (find in Ads Manager URL or campaign settings)
- **Owner** → set to your name (VA / Operator)
- **Status** → change from **Draft** to **QA Ready**

### Step 6: Complete the QA Checklist
Go through every QA field in the record. Each is a Yes/No tick. Only tick Yes when you have personally confirmed it.

| QA Check | How to Confirm |
|---|---|
| ✅ Correct Video Uploaded | Play the video in the ad preview. Compare to the Asset Link. |
| ✅ Correct Page & IG Identity | Check the "Identity" section in Ads Manager — correct FB page and IG account selected. |
| ✅ Correct Geo/Market | Check the location targeting matches the client's market. |
| ✅ Correct Budget Set | Daily budget matches what's in the SmartSuite Campaign record. |
| ✅ Naming Convention Matches | Campaign/Ad Set/Ad names exactly match the naming convention. |
| ✅ Special Ad Category = Housing | Open campaign settings. Confirm "Housing" is selected under Special Ad Category. |
| ✅ Placements Correct | Check placements are set correctly (usually Facebook + Instagram feeds + Reels). |
| ✅ CBO Off | Confirm Campaign Budget Optimisation is toggled OFF. |
| ✅ CTA Correct | Video Views + Retarget: no CTA button, ad copy says "comment OPTIONS". Lead Ad: Facebook Lead Form is attached and working. |

> ⚠️ **All 9 QA checks must be ticked Yes before you publish.** If any is No, fix it first.

### Step 7: Publish and Update
1. Once all 9 QA checks are Yes, go back to Ads Manager and **publish the campaign**.
2. In the SmartSuite record, change **Status** to **Live**.
3. Set **Launch Date** to today's date.
4. Tick **Client Launch Notified** → Yes (n8n will send the notification, but confirm it happens).
5. Mark your Task in the Tasks app as **Done**.

---

## How Metrics Work (Automatic)

You don't manually enter metrics. Windsor AI pulls performance data from Facebook daily and n8n writes it into these fields automatically:

- Spend, ThruPlays, Cost/ThruPlay
- 50% Views, 75% Views, 95% Views
- Saves, Shares, Comments, DMs
- Leads, Cost/Lead
- Last Pull Date (shows when the data was last synced)

If **Last Pull Date** is more than 48 hours ago, something may be wrong with the Windsor sync. Flag to Andrew.

---

## Key Fields Explained

| Field | What It's For |
|---|---|
| **Campaign Record Name** | The name of this record in SmartSuite. Use the same naming convention as Ads Manager. |
| **Script Link** | Google Drive link to the video script used for this campaign. |
| **Asset Link** | Google Drive link to the actual video file used in the ad. |
| **Platform Campaign ID** | The Facebook Campaign ID. Used by Windsor AI to pull metrics. Critical — don't leave blank. |
| **Week** | Which week of the quarter this campaign launched (W1–W13). Used for reporting. |
| **Saves** | The Hormozi metric. High saves = the content is resonating. This is your winner signal. |
| **Owner** | Who built/owns this campaign record (VA / Operator). |
| **Launch Date** | The date the campaign went live. Set this when you publish. |
| **Campaign Type** | Video Views / Retarget / Lead Ad — which type of campaign this is (see table above). |

---

## Views

| View | When to Use It |
|---|---|
| **Build Queue** | VA default. Shows all campaigns with Status = Draft. Your work queue. |
| **QA Ready** | Campaigns built and waiting for QA. Work through these before starting new builds. |
| **Live** | All running campaigns with metrics visible. |
| **All Campaigns** | Andrew's view. Everything across all clients. |

---

## What NOT to Do

- ❌ Never skip **Special Ad Category = Housing**. This is a legal requirement. Skipping it can get the client's ad account banned.
- ❌ Never use zip code targeting. Facebook's housing rules prohibit it. City/state only.
- ❌ Never publish without completing all 9 QA checks.
- ❌ Never change the **Platform Campaign ID** once it's set. Windsor AI uses this to pull metrics.
- ❌ Never mark Status as Live until the campaign is actually published and running in Ads Manager.
- ❌ Never leave the **Asset Link** or **Script Link** blank. If you can't find the file, ask Andrew before building.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Metrics haven't updated in 48+ hours | Check Last Pull Date. Flag to Andrew — Windsor sync may have failed. |
| Campaign is Live in Ads Manager but Draft in SmartSuite | Update the Status field. Don't let them get out of sync. |
| Asset Link is broken or goes to the wrong file | Do NOT proceed with the build. Tell Andrew — wrong video in the wrong ad is a real problem. |
| Special Ad Category warning in Ads Manager | This means Housing wasn't selected. Fix it before publishing. |
| Facebook rejected the ad | Flag to Andrew immediately with the rejection reason. |
| Retarget/Lead Ad audiences don't exist yet | The Video Views campaign hasn't run long enough to build audiences. Flag to Andrew — do not proceed without audiences. |
