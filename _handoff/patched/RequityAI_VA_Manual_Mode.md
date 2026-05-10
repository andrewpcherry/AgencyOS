# 🤖➜🙋 RequityAI — Manual Mode Manual

**Version:** 2026-05-10
**Who this is for:** Andrew, the VA, or anyone who needs to run RequityAI **without the robots**.
**How to read it:** front to back, once. Then keep it open as a backup when something breaks.

---

## ⚠️ Read this first — why this manual exists

The robots (n8n automations) do most of the boring work for you. Good.

But two things are true:

1. **Robots break.** When they do, the work still has to happen. You need to know how to do it by hand.
2. **If you can't do a job by hand, you don't really understand it.** And if you don't understand it, you can't trust the robot to do it right.

So this manual shows you the **manual version of every job** the robots normally do. Plus the hands-on VA work that is yours either way.

You won't use this every day. You'll use it:
- When a robot breaks and Andrew tells you "just do it by hand for now."
- When you want to learn what's actually happening under the hood.
- When you onboard a new VA and want them to understand the system.

**Rule:** if a robot is working, **let it work**. Don't do its job and the robot's job at the same time — you'll get duplicate records.

---

## 🧭 How the agency works (90 seconds)

RequityAI runs Facebook ads for real-estate investors who buy houses off-market.

We use a **3-stage funnel** for every client:

| Stage | Campaign | What it does |
|---|---|---|
| **TOF** (top) | Video Views | A short talking-head video. People watch. The watchers become our retargeting pool. **No CTA button** — copy says "comment OPTIONS." |
| **MOF** (middle) | Retarget | A second video. Shown only to people who watched 25%+ of the TOF video. Pushes them to watch more. |
| **BOF** (bottom) | Lead Ad | A Facebook Lead Form. Shown only to people who watched 75%+. **This is the only campaign that captures leads.** |

That's the whole product.

Your job sits in the middle. You move a client from **Won deal → live campaigns → optimized loop**.

Two phrases to lock in:

- **SmartSuite holds the truth.** If it's not in SmartSuite, it doesn't exist.
- **Don't ping Andrew for what an SOP can answer.** Read the manual, do the work, then tell him what you did.

---

## ✅ Before Day 1 — your logins

Tick each box once you've confirmed it works.

- [ ] **SmartSuite** — `app.smartsuite.com` (workspace `sl181chl`). You should see the 10 business apps.
- [ ] **Slack** — RequityAI workspace. You should be in `#all-requityai`, `#team-operations`, every `#team-<client>`, and any `#client-<client>` channels you've been invited to.
- [ ] **Google Drive** — the `RequityAI` parent folder (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`). You should see one subfolder per active client.
- [ ] **Meta Business Manager** — invite accepted. You can see the RequityAI Business Portfolio.
- [ ] **Meta Ads Manager** — access to each client's ad account (added per client during Phase 1).
- [ ] **Close CRM** — read access. You'll need this for Manual Job 4.
- [ ] **Calendly** — admin access on the RequityAI Calendly account. You'll need this for Manual Jobs 1 and 2.
- [ ] **Password manager** — every login above is in there so you're not asking Andrew twice.

If anything is blocked, post in `#team-operations` (not a DM). Andrew sees it, the system sees it.

---

## 📚 How to use Part 1 (the Robot Jobs)

Each Robot Job follows the same shape:

**🟢 What just happened** — the trigger. Something changed in the world.
**🤖 What the robot normally does** — one paragraph. So you understand what you're replacing.
**🙋 Do this by hand** — numbered steps, click by click.
**⚠️ Don't mess this up** — common mistakes.
**✅ How you know it worked** — what to check after.

You don't have to memorize the whole manual. You just have to find the right Robot Job when something happens, then follow the recipe.

---

# PART 1 — THE 9 ROBOT JOBS

---

## Robot Job 1 — A new lead books a call

### 🟢 What just happened
Someone clicked your Calendly link. They picked a time. They booked a discovery call with Andrew.

### 🤖 What the robot normally does
Calendly fires a webhook to n8n (M3). n8n creates a new record in the SmartSuite **Pipeline** app, sets the deal stage to **Booked**, hydrates the deal with name + email + phone + Close CRM context, and posts to `#team-operations`.

### 🙋 Do this by hand

**Step 1 — Get the booking info from Calendly.**
1. Open Calendly.
2. Click **Scheduled Events**.
3. Find the new booking.
4. Copy: name, email, phone, company (if given), the time of the call, and the answers to any intake questions.

**Step 2 — Make the Pipeline record.**
1. Open SmartSuite.
2. Click **Pipeline** (left side).
3. Click **+ Add new** at the top.
4. Fill in:
   - **Deal Name:** `Booked — [First Last] — [Company if given]`
   - **Deal Stage:** `Booked`
   - **Email:** the email from Calendly
   - **Phone:** the phone from Calendly
   - **Source:** `Calendly`
   - **Booked Date:** the date they booked the call (today)
   - **Call Date:** the date/time of the actual call
5. Click **Save**.

**Step 3 — Check Close CRM.**
1. Open Close CRM.
2. Search for the email.
3. If a Lead exists, copy the Lead ID. Paste it into the Pipeline record's **close_lead_id** field.
4. If no Lead exists, leave **close_lead_id** blank. Andrew creates the Close lead live during the call.

**Step 4 — Tell the team.**
1. Open Slack → `#team-operations`.
2. Post: `📅 New call booked — [Name] — [Company] — [Date/Time]. Pipeline record created.`

### ⚠️ Don't mess this up
- ❌ Don't make a duplicate. Search Pipeline first by email — if a record exists, **update it**, don't make a new one.
- ❌ Don't post in `#client-<anything>`. The lead isn't a client yet.
- ❌ Don't set the deal stage to anything but `Booked`. Andrew updates it after the call.

### ✅ How you know it worked
- Pipeline shows the new record in the **Active Deals** view.
- `#team-operations` has your post.

---

## Robot Job 2 — A lead doesn't show up

### 🟢 What just happened
The call time came. The lead didn't show. Andrew flips the Pipeline deal stage to **No Show**.

### 🤖 What the robot normally does
M4 watches Pipeline for `deal_stage = No Show`. When it sees one, it tells Calendly the invitee was a no-show, which triggers Calendly's reschedule workflow (an SMS + email goes to the lead asking them to pick a new time).

### 🙋 Do this by hand

**Step 1 — Confirm the no-show.**
1. Open SmartSuite → **Pipeline**.
2. Find the deal. Confirm **Deal Stage** = `No Show`.

**Step 2 — Mark them no-show in Calendly.**
1. Open Calendly.
2. Click **Scheduled Events** → find the original booking.
3. Click **Actions** → **Mark as no-show**.

**Step 3 — Send the reschedule message yourself.**
Calendly's workflow normally fires here. If it doesn't, you do it:
1. Email the lead from your RequityAI inbox. Subject: `Sorry we missed you — let's reschedule`
2. Body:
   > Hi [Name], sorry we missed you on the call today. Things come up. Pick a new time that works for you here: [Calendly link]. — Andrew, RequityAI
3. Send.

**Step 4 — Quiet hours rule.**
Only send between **8am–6pm ET**. If the no-show happens outside that window, schedule the email to send at 8am the next morning.

**Step 5 — Update Pipeline.**
1. Add a note in the deal record: `No-show reschedule sent [date/time]`.
2. Leave the stage as `No Show` until they rebook (then it goes back to `Booked`).

### ⚠️ Don't mess this up
- ❌ Don't send the reschedule outside quiet hours. People hate that.
- ❌ Don't pester. One reschedule email. If they don't rebook in 5 days, flip the stage to `Ghosted`.

### ✅ How you know it worked
- Calendly shows the booking marked **No Show**.
- Pipeline note has your reschedule timestamp.

---

## Robot Job 3 — A DEAL IS WON 🏆

This is the big one. The robot does about 8 things at once. Get a coffee.

### 🟢 What just happened
Andrew flipped a Pipeline deal stage to **Won**.

### 🤖 What the robot normally does
M5 (workflow `A31jYsKR3aETSusC`) fires within 30 seconds and atomically does ALL of this:
1. Creates a **Client** record in SmartSuite (hydrated with the deal info).
2. Creates an **Onboarding** record linked to the Client.
3. Creates the Google Drive folder structure: `RequityAI/<Client>/Raw Video/` + `Ad Creative/`.
4. Creates two Slack channels: `#team-<slug>` (private, internal) and `#client-<slug>` (private by default; Andrew flips public after guest invite).
5. Invites Andrew to both Slack channels.
6. Posts the niche-aware welcome doc into `#team-<slug>` (script library + recording brief).
7. Posts a confirmation in `#team-operations`.
8. Marks the Pipeline deal as `won_processed = true` so it doesn't run again.

You do all of that. Take it one step at a time.

### 🙋 Do this by hand

**Step 1 — Open the Won deal in SmartSuite Pipeline.**
1. Find the deal. Confirm `Deal Stage = Won`.
2. Copy these into a notes app (you'll paste them in 6 places):
   - Client business name (e.g., `Quick Home Buyers`)
   - Email
   - Phone
   - Company website
   - Niche (REI / Notes / Other — Andrew tells you)
   - The `close_lead_id` if it's filled in

**Step 2 — Make the slug.**
The slug is the lowercase, hyphenated version of the client name. No spaces. No special characters.

Examples:
- `Quick Home Buyers` → `quick-home-buyers`
- `Real-Vantage` → `real-vantage`
- `Ritsel Notes` → `ritsel-notes`

Write the slug down. You'll use it 4 times.

**Step 3 — Make the Client record.**
1. SmartSuite → **Clients** → **+ Add new**.
2. Fill in:
   - **Title** (the client name): `Quick Home Buyers`
   - **Status:** `Onboarding` (this is the canonical `status` field — ignore `client_status`)
   - **Niche:** the niche from Andrew (default `REI`)
   - **Email**, **Phone**, **Company website**, **close_lead_id**: paste from your notes
3. Leave the Meta IDs, Drive Folder URL, and Slack Channel IDs blank for now. You fill those in shortly.
4. Click **Save**. Note the Client record ID.

**Step 4 — Make the Onboarding record.**
1. SmartSuite → **Onboarding** → **+ Add new**.
2. Fill in:
   - **Title:** `Onboarding — [Client Name]`
   - **Client:** link to the Client record you just made.
   - **Niche:** same niche.
   - All 18 step fields stay at `Pending` (value `1`).
   - **Onboarding Complete:** `Pending`.
3. Click **Save**.

**Step 5 — Make the Google Drive folders.**
1. Open Google Drive.
2. Go to the `RequityAI` parent folder (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`).
3. Click **+ New** → **Folder** → name it the client name exactly: `Quick Home Buyers`.
4. Open the folder you just made.
5. Click **+ New** → **Folder** → name it `Raw Video`.
6. Click **+ New** → **Folder** → name it `Ad Creative`.
7. Right-click the parent client folder → **Share** → **Get link** → set to **Anyone with the link** can view → copy the URL.
8. Go back to the Client record in SmartSuite. Paste the URL into **Drive Folder URL**. Save.

**Step 6 — Make the two Slack channels.**
1. Open Slack.
2. Click the **+** next to **Channels** → **Create channel**.
3. Channel name: `team-[slug]` (example: `team-quick-home-buyers`).
4. Set it to **Private**.
5. Click **Create**.
6. Invite Andrew. Invite yourself.
7. Repeat for the second channel:
   - Channel name: `client-[slug]` (example: `client-quick-home-buyers`).
   - **Set it to Private** by default. Andrew flips it to public manually after the client is invited as a guest. **Do not flip it public yourself.**
   - Invite Andrew. Invite yourself.

**Step 7 — Save the Slack channel IDs to the Client record.**
1. In Slack, right-click each channel → **Copy link**. The link looks like `https://requityai.slack.com/archives/C0AVAJ5KM0U`. The part after `/archives/` is the channel ID (`C0AVAJ5KM0U`).
2. In SmartSuite Client record:
   - Paste the `team-` channel ID into **Slack Channel ID**.
   - Paste the `client-` channel ID into **Client Slack Channel ID**.
3. Save.

**Step 8 — Post the welcome brief into `#team-[slug]`.**
1. Open the niche script library doc (Andrew keeps the link in the Drive `Templates` folder).
2. Open the recording brief template doc.
3. In `#team-[slug]`, post:
   ```
   👋 Welcome aboard [Client Name]!
   Niche: [Niche]
   Drive folder: [paste Drive URL]
   Script library: [paste link]
   Recording brief: [paste link]
   Onboarding starts now. Phase 1 = Meta access.
   ```

**Step 9 — Confirm in `#team-operations`.**
1. Post in `#team-operations`:
   ```
   ✅ Manual Won-deal processing complete for [Client Name].
   • Client + Onboarding records created
   • Drive folder live
   • #team-[slug] + #client-[slug] created
   • Welcome brief posted
   ```

**Step 10 — Mark the Pipeline deal as processed.**
1. Open the Pipeline deal record.
2. Set the **won_processed** field to `True` (or tick the checkbox).
3. Save.

This stops you (or the robot, if it comes back online) from doing it again.

### ⚠️ Don't mess this up
- ❌ **Slug must be lowercase + hyphenated.** Slack channel names won't accept caps or spaces.
- ❌ **Don't flip `#client-<slug>` to public.** Andrew does that after the client is invited as a guest. Default = private since Apr 25.
- ❌ **Don't forget step 10.** If `won_processed` stays false, the robot will redo the whole thing when it wakes back up. Duplicate records everywhere.
- ❌ **Don't skip the welcome brief.** That's how the VA (you) gets the niche scripts.

### ✅ How you know it worked
- Client record in SmartSuite, status `Onboarding`.
- Onboarding record exists, linked to the Client.
- Drive folder visible in `RequityAI/`.
- Both Slack channels exist.
- Welcome brief is in `#team-[slug]`.
- Pipeline deal has `won_processed = true`.

---

## Robot Job 4 — A call happens in Close CRM

### 🟢 What just happened
Andrew made a sales call in Close. He logged the disposition (e.g., `Owner - Booked`, `Voicemail`, `Non-Decision Maker (NDM) Interested`).

### 🤖 What the robot normally does
M2b polls Close every 30 minutes (M-F, 8am–3:30pm ET). It pulls every new call activity, dedupes, and writes a row into the SmartSuite **Conversation Tracker** app. It also writes the disposition into the `last_call_outcome` field.

### 🙋 Do this by hand

**Step 1 — Check Close for new calls.**
1. Open Close CRM.
2. Click **Calls** in the left sidebar.
3. Filter by date = today (or whatever range you're catching up).
4. For each call you see that **isn't already in ConvTracker**, do the next steps.

**Step 2 — Make the ConvTracker record.**
1. SmartSuite → **Conversation Tracker** → **+ Add new**.
2. Fill in:
   - **Title:** `Call — [Lead Name] — [Date]`
   - **Lead Name:** from Close.
   - **Phone:** from Close.
   - **Email:** from Close.
   - **Date:** the call date.
   - **Outcome:** pick one of 6 (this is the conversation-level signal you fill in manually):
     - `Interested` · `Maybe` · `Not Interested` · `No Contact` · `Gatekeeper` · `LVM`
   - **Last Call Outcome:** copy the EXACT disposition from Close. Allowed values (15):
     `Owner - Booked` · `Owner - Talked` · `Owner - Maybe` · `Owner - Callback Requested` · `Owner - Not Interested` · `Non-Decision Maker (NDM) Interested` · `Gatekeeper` · `Voicemail` · `No Answer` · `Wrong Number` · `Do Not Call` · `Hung Up - Owner` · `Left Voicemail` · `Voice Agent` · `Invalid`
   - **Call Booked:** `Yes` if the call resulted in a booked appointment, else `No`.
   - **Close Activity ID:** copy from Close (this prevents duplicates if the robot wakes up later).
3. Save.

**Step 3 — If a call was booked, update Pipeline too.**
1. SmartSuite → **Pipeline** → search for the lead.
2. If there's no Pipeline record, make one (see Robot Job 1).
3. Set **Deal Stage** to `Booked`.

### ⚠️ Don't mess this up
- ❌ **Don't make duplicates.** Always check Close Activity ID before adding. If it's already in ConvTracker, skip.
- ❌ **Last Call Outcome must match Close exactly.** "Voicemail" and "Left Voicemail" are different values.
- ❌ **Don't edit anyone else's logged outcome.** Outcome is the conversation-level signal — only the person who had the conversation edits it.

### ✅ How you know it worked
- ConvTracker shows the new row.
- If the call was booked, Pipeline shows `Booked` for that lead.

---

## Robot Job 5 — Make a Drive folder for a new client

### 🟢 What just happened
Either you're processing a Won deal manually (see Robot Job 3, Step 5) or a Client record exists with a blank **Drive Folder URL**.

### 🤖 What the robot normally does
Workflow `BegEckXSgXmVffX2` runs daily at 8am ET. It looks for Client records with no Drive Folder URL, creates the parent folder + `Raw Video/` + `Ad Creative/`, writes the URL back to the Client record, and posts in `#team-<slug>`.

### 🙋 Do this by hand

This is identical to Step 5 of Robot Job 3. Repeating here for quick lookup:

1. Google Drive → `RequityAI` parent folder.
2. **+ New** → **Folder** → name it the client name exactly.
3. Open it. **+ New** → **Folder** → `Raw Video`.
4. **+ New** → **Folder** → `Ad Creative`.
5. Share the parent client folder → **Anyone with the link** can view → copy URL.
6. Paste the URL into the Client record's **Drive Folder URL** field. Save.
7. Post in `#team-[slug]`: `📁 Drive folder live: [URL]`.

### ⚠️ Don't mess this up
- ❌ **Folder name must match client name exactly.** Including spaces, capitals, dashes. Reports break otherwise.
- ❌ **Don't put files in `Raw Video/` that haven't come from the client.** That folder is the source of truth for what the client sent you.
- ❌ **Don't put raw uncut files in `Ad Creative/`.** That folder is finished cuts only.

### ✅ How you know it worked
- Client record's **Drive Folder URL** is filled in.
- The link opens. You see two subfolders.

---

## Robot Job 6 — Save your work to SmartSuite

### 🟢 What just happened
You finished a task. Or hit a blocker. Or got a campaign to QA Ready. Normally you'd post a `/update` message in Slack and the Sync Agent would write the change to SmartSuite for you.

### 🤖 What the robot normally does
The Sync Agent (workflow `8tdPtQWO4qDKEjgq`) reads your `/update` Slack message within 60 seconds. It parses the app, the client, and the field changes. It writes them to SmartSuite. It reacts ✅ or ⚠️ to your message.

### 🙋 Do this by hand

**You skip Slack and edit SmartSuite directly.** That's it.

For each kind of update:

**Tasks update**
1. SmartSuite → **Tasks** → find the task.
2. Change **Status** to `To Do` / `In Progress` / `Blocked` / `Done`.
3. If `Blocked`, fill in **Blocker Notes** with what's blocking you.
4. Save.

**Campaigns update**
1. SmartSuite → **Campaigns** → find the campaign.
2. Change **Status** (Draft / QA Ready / Live / Paused / Cut / Completed).
3. If going Live, also fill in **Launch Date** = today.
4. Save.

**Onboarding step update**
1. SmartSuite → **Onboarding** → find the client's record.
2. Find the right `step_*` field.
3. Change the value (`1` = Pending, `2` = In Progress, `3` = Complete).
4. Save.
5. **Note:** normally the robot does this. The robot also recomputes `Onboarding Stage`. If you changed a step, also update **Onboarding Stage** to match the latest phase the client is in.

**Pipeline stage update** (Andrew only normally — but if you're covering)
1. SmartSuite → **Pipeline** → find the deal.
2. Change **Deal Stage** (10 valid values — see SOP_01).
3. Save.

### ⚠️ Don't mess this up
- ❌ **Don't post `/update` in Slack and edit SmartSuite at the same time.** You'll get the change written twice if the robot is alive.
- ❌ **Don't make up status values.** Use the exact dropdown labels.
- ❌ **Don't edit Optimization Decision fields.** Those are the agent's. Even in manual mode, the *decision* is Andrew's.

### ✅ How you know it worked
- Refresh the SmartSuite record. Your change is there.
- Anyone else looking at the record sees the same thing.

---

## Robot Job 7 — Daily ops check

### 🟢 What just happened
It's 8am. The day is starting.

### 🤖 What the robot normally does
The Daily Ops Briefing (`ey0cuADK27ntvgMe`) and Slack Ops Supervisor (`5cdMtOByeZVRFS6H`) post a snapshot to `#team-operations` at 8am and 8pm ET. The Daily Sales Brief (`pa7I1FKd50TQRFrV`) posts at 8:05am ET M-F with calls/booked/conversion ratios.

### 🙋 Do this by hand

Open these tabs in this order:

**Step 1 — Pipeline check (5 min)**
1. SmartSuite → **Pipeline** → **Active Deals** view.
2. Count: how many deals are in `Booked`, `Follow Up / Reschedule`, `Proposal - Decision - Pending`?
3. Look for any deal that's been in the same stage for more than 7 days. Flag it.

**Step 2 — Sales numbers (5 min)**
1. SmartSuite → **Conversation Tracker** → filter Date = today.
2. Count today's calls. Of those, how many were `Owner - Booked`?
3. Filter Date = this week. Same counts.
4. Filter Date = this month. Same counts.
5. Compute conversion: `Booked ÷ Calls` for each window.

**Step 3 — Onboarding check (5 min)**
1. SmartSuite → **Onboarding** → **Onboarding Board** view.
2. For each active client, look at the step dropdowns. Anything red (Pending) for >5 days = blocker.
3. Make a list of blockers.

**Step 4 — Tasks check (3 min)**
1. SmartSuite → **Tasks** → **My Queue**.
2. Anything `Blocked`? Read the Blocker Notes.
3. Anything `In Progress` for >24h? Decide: keep going or move to `Blocked`.
4. Anything overdue? Surface it.

**Step 5 — Post the briefing.**
1. Slack → `#team-operations`.
2. Post (fill in the actuals):
   ```
   ☀️ Daily Ops Briefing — [Date]

   📞 Sales (Today / WTD / MTD)
   • Calls: X / X / X
   • Booked: X / X / X
   • C→B: X% / X% / X%

   📋 Pipeline
   • Booked: X
   • Follow Up: X
   • Proposal: X
   • Stale (>7 days): [list]

   🚦 Onboarding
   • Blockers: [list, or "none"]

   ✅ Tasks
   • Blocked: X
   • Overdue: X
   ```

### ⚠️ Don't mess this up
- ❌ **Don't skip days.** A daily briefing missed = a daily blocker missed.
- ❌ **Don't post placeholders.** If you can't get a number, write `N/A` and explain why.

### ✅ How you know it worked
- The post is in `#team-operations`.
- Andrew reacts or replies with anything to act on.

---

## Robot Job 8 — Nudge stuck onboarding

### 🟢 What just happened
A client has been stuck on the same Onboarding step for more than 5 days.

### 🤖 What the robot normally does
The Onboarding Health Monitor (`CqesBe55FnP6oaxA`) runs daily at 8:30am ET. It looks at every Onboarding record. If a step has been `In Progress` or `Pending` for >5 days, it DMs Andrew with the client + step + days stuck.

### 🙋 Do this by hand

**Step 1 — Find the stuck steps.**
1. SmartSuite → **Onboarding** → **Onboarding Board** view.
2. Open each active Onboarding record.
3. Look at every `step_*` field. Compare its **Last Updated** date to today.
4. Anything that hasn't moved in >5 days is stuck.

**Step 2 — Diagnose.**
For each stuck step, ask: **why isn't this moving?**
- Waiting on the client? (e.g., they haven't sent video yet)
- Waiting on you? (e.g., you haven't done your part)
- Waiting on Andrew? (e.g., approval needed)
- Genuinely blocked? (e.g., Meta flagged the account)

**Step 3 — Fix or escalate.**
- **Waiting on you:** stop reading this and do the work.
- **Waiting on the client:** send a friendly nudge. In `#client-[slug]`:
  > Hi [Client] — we're ready for the next step. Quick reminder we still need [the thing]. Thanks!
- **Waiting on Andrew:** DM Andrew with the client name + step + what you need.
- **Genuinely blocked:** post in `#team-[slug]` with the diagnosis. Add a Task with Status `Blocked` and put the diagnosis in Blocker Notes.

**Step 4 — Log the nudge.**
1. Open the Onboarding record.
2. Add a note in **Blocker Notes**: `[Date] — nudged client about [step]`.

### ⚠️ Don't mess this up
- ❌ **Don't nudge twice in one day.** One nudge per day per client. Pestering kills relationships.
- ❌ **Don't nudge outside 8am–6pm ET.** Quiet hours rule.
- ❌ **Don't escalate to Andrew before you've tried the obvious thing.** "Have you sent the video yet?" first.

### ✅ How you know it worked
- Stuck steps either move within 24–48 hours or get formally Blocked with a diagnosis.

---

## Robot Job 9 — Pull Facebook ad numbers into Campaigns

### 🟢 What just happened
A campaign is Live. Numbers are accumulating in Facebook Ads Manager. Normally Windsor AI pulls them every 12 hours and writes them to the SmartSuite Campaign record.

### 🤖 What the robot normally does
The Windsor AI workflow (`ZwXd0unFysJjWl1M`) pulls metrics every 12h: Spend, ThruPlays, Cost/ThruPlay, 50% / 75% / 95% Views, Saves, Shares, Comments, DMs, Leads, Cost/Lead. Writes them to the matching SmartSuite Campaign record (matched by Platform Campaign ID). Updates the **Last Pull Date**.

### 🙋 Do this by hand

**Step 1 — Open the live campaigns list.**
1. SmartSuite → **Campaigns** → **Live** view.
2. For each campaign, do steps 2–4.

**Step 2 — Find it in Ads Manager.**
1. Open Facebook Ads Manager for the client's ad account.
2. Find the matching campaign by name (or by the **Platform Campaign ID** stored in SmartSuite).
3. Set the date range to the **same window Windsor uses** (last 7 days is standard).

**Step 3 — Read the numbers.**
From Ads Manager, for each campaign read:
- **Spend** (USD)
- **ThruPlays** (or Video Plays at 100%)
- **Cost per ThruPlay**
- **50% / 75% / 95% video views** (find these in the column picker → Video Engagement)
- **Saves / Shares / Comments**
- **DMs** (if you can get them — otherwise leave blank)
- **Leads** (only relevant for Lead Ad campaigns)
- **Cost per Lead** (only relevant for Lead Ad campaigns)

**Step 4 — Write them into the SmartSuite Campaign record.**
1. Open the campaign record.
2. Paste each value into the matching field.
3. Update **Last Pull Date** to today.
4. Save.

### ⚠️ Don't mess this up
- ❌ **Match the right campaign.** Use Platform Campaign ID, not just the name. Names can repeat.
- ❌ **Use the same date window each time.** Otherwise the trend doesn't make sense.
- ❌ **Don't enter zeros if Ads Manager shows blank.** Leave blank. Zero is data; blank is "no data."

### ✅ How you know it worked
- Campaign record's **Last Pull Date** is today.
- The numbers are in. Andrew can see trends.

---

# PART 2 — YOUR HANDS-ON WORK

These jobs are yours whether the robots are running or not. The robots track and notify around them — but the *doing* is always you.

---

## Phase 1 — Get into the client's Meta accounts

The goal: you (the VA) have full access to the client's Meta Business Portfolio so you can build ads.

### Step 1 — Send the access request
1. Open Meta Business Manager → **Business settings** → **Business Portfolios** → **Request access**.
2. Enter the client's Business Portfolio ID (it's in the SmartSuite Client record under **Business Portfolio ID**).
3. Request **Admin** access on the Ad Account.
4. Send.

### Step 2 — Tell the client to approve
In `#client-[slug]`:
> Hi [Client] — I've sent you a Business Portfolio access request from RequityAI. To approve: open **business.facebook.com → Business settings → Requests** → accept ours. Takes 30 seconds. Thanks!

### Step 3 — Confirm visibility
1. Once approved, refresh Meta Business Manager.
2. You should see the client's Ad Account.
3. Open the Ad Account. You should be able to view campaigns (even if there are none yet).

### Step 4 — Update SmartSuite
- **Onboarding** record → set `step_business_portfolio_access` = Complete.
- **Onboarding** record → set `step_ad_account_visible` = Complete (if it is).
- **Clients** record → fill in **Ad Acct ID**, **Business Portfolio ID** (confirm match), **Facebook Page URL**.

### Step 5 — Walk through the rest of Phase 1
- `step_facebook_page_confirmed` = Complete once you can see + post on the FB page.
- `step_instagram_connected` = Complete once IG is linked to the FB page.
- `step_meta_ads_app_installed` = Complete once the client confirms they have the Meta Ads app on their phone (for lead notifications).

---

## Phase 2 — Set up where leads go

The goal: when someone fills in the Lead Ad form, the lead lands somewhere the client can act on it.

### Step 1 — Confirm Lead Centre access
1. In Meta Business Manager → **Leads Access**. You should see Lead Centre for the client's page.
2. Mark `step_leads_access_confirmed` = Complete.

### Step 2 — Set up notifications
1. In Lead Centre → **Settings** → **Notifications** → enable email + push to the client.
2. Mark `step_lead_notifications_set` = Complete.

### Step 3 — Connect to the client's CRM
The client picks where leads go. Common destinations:
- **GoHighLevel** (most common): use the GHL native FB integration.
- **Google Sheet**: use Zapier or Make to push leads from Lead Centre → Sheet.
- **Their own CRM**: use whatever native or Zapier connector exists.

Set up the integration. **Send a test lead** from yourself. Confirm it lands.

Mark `step_lead_centre_to_crm` = Complete.

### Step 4 — Confirm with the client
In `#client-[slug]`:
> Hi [Client] — Lead Centre is connected to [destination]. I sent a test lead. You should see it in [destination]. Confirm when you do?

Once they confirm, mark `step_lead_destination_confirmed` = Complete.

### Step 5 — Final tick
Once everything above works, mark `step_fb_lead_centre_connected` = Complete. Phase 2 done.

---

## Phase 3 — Make videos work

The goal: client-recorded talking-head videos are in `Ad Creative/`, edited, approved.

**You own this end-to-end.** That includes the editing. (Decision: 2026-05-09. Expect a 4–6 week skill ramp before edit quality is consistent.)

### Step 1 — Send the video brief
1. Pick the niche-specific brief from Drive `Templates/`.
2. Personalize: client name, market, business specifics.
3. Send to the client (email or `#client-[slug]`).
4. Mark `step_video_brief_sent` = Complete.

### Step 2 — Wait for raw videos
The client uploads to `Raw Video/` in their Drive folder. When new files appear:
- Mark `step_videos_received` = Complete.
- Watch each video to check audio + lighting + framing. If it's unusable, ask for a re-record.

### Step 3 — Edit
For each raw video:
1. Pull it down to your editor (CapCut / Premiere / DaVinci — whichever you use).
2. Trim. Add captions. Add b-roll if it fits the script. Color-correct lightly.
3. Export at 1080×1080 (square) and 1080×1920 (vertical). Both formats are needed.
4. Drop the finished cuts into `Ad Creative/`.
5. Filename format: `[CLIENT-CODE]-[SCRIPT-ID]-[VERSION]-[FORMAT].mp4`
   Example: `QHB-FC-B2-14-V1-square.mp4`

Mark `step_videos_edited` = Complete.

### Step 4 — Get Andrew's approval
1. Post in `#team-[slug]`:
   > 🎬 Edits ready for [Client]. [N] cuts in `Ad Creative/`. Approve for ads?
2. Andrew watches, approves or sends notes.
3. On approval: mark `step_approved_videos_exist` = Complete.

---

## Phase 4 — Build, check, launch ads

The goal: campaigns live in Ads Manager, mirrored in SmartSuite.

This is covered in detail in **SOP_05_Campaigns.md**. Summary here:

### Step 1 — Get the build task
1. SmartSuite → **Tasks** → **My Queue** → find a `Build Campaign` task.
2. Open the linked Campaign record. Confirm: client, market, type, daily budget, script link, asset link, week.
3. If anything is missing, mark Task `Blocked`, fill Blocker Notes, post in `#team-[slug]`.

### Step 2 — Build in Ads Manager (per SOP_05)
- Naming convention exact (Campaign / Ad Set / Ad name format).
- Audiences: broad for Video Views; 25%/50% for Retarget; 75%/95% for Lead Ad.
- **Special Ad Category = Housing** (legally required — never skip).
- **No zip code targeting.** City/state only.
- **CBO off.**
- CTA: no button on Video Views/Retarget; Facebook Lead Form on Lead Ad.

### Step 3 — Mirror to SmartSuite
- Paste Campaign Name, Ad Set Name, Ad Name, Platform Campaign ID into the SmartSuite Campaign record.
- Set **Owner** = you. Set **Status** = `QA Ready`.

### Step 4 — Run the 9-point QA checklist
Each of these must be ✅ before publish:
1. Correct video uploaded.
2. Correct Page + IG identity.
3. Correct geo / market.
4. Correct daily budget.
5. Naming convention exact.
6. **Special Ad Category = Housing.**
7. Placements correct (FB + IG feeds + Reels).
8. CBO off.
9. CTA correct.

### Step 5 — Get Andrew's go/no-go
1. Post in `#team-[slug]`:
   > ✅ QA passed for [Campaign Name]. Ready to publish on your go.
2. Wait for Andrew's approval.
3. On approval: hit **Publish** in Ads Manager.

### Step 6 — Update SmartSuite
- Campaign **Status** → `Live`.
- Campaign **Launch Date** → today.
- Onboarding **step_campaign_launched** → Complete.
- Notify in `#client-[slug]` (with Andrew's approval):
  > 🚀 Your first campaign is LIVE: [Campaign Name]. We'll start tracking metrics now and report back in a week.
- Onboarding **step_launch_notification_sent** → Complete.
- Campaign Task → `Done`.

When `step_launch_notification_sent` flips Complete, master `step_onboarding_complete` flips to ✅. Client status flips to `Active`.

---

## The optimization loop (when campaigns are live)

Normally the **Campaign Intelligence Agent** (`6TuDo3mqBZSBF667`) reads metrics every 12h and writes a decision (Keep / Cut / Retarget / Swap Creative / Needs Review) into the Optimization record. The **Decision Router** (`iM5CNWHLS2UIIJ34`) executes the operational tasks (Cut/Pause, Swap Creative, Adjust Targeting).

In manual mode you do both yourself, with Andrew making the actual decisions.

### Daily during live campaign
1. Pull the numbers (Robot Job 9).
2. For each Live campaign, look at:
   - Cost per ThruPlay vs threshold.
   - 75%/95% video view counts (audience for retarget/lead ads).
   - Saves (the Hormozi metric — high saves = winner signal).
   - Cost per Lead (Lead Ad only).
3. If a campaign is under-performing for >72h: flag in `#team-operations` with the numbers + your read.
4. Andrew picks: Keep / Cut / Pause / Swap Creative / Adjust Targeting.
5. You execute in Ads Manager. Update SmartSuite Campaign record (Status, plus a note in Optimization Notes).

### When to escalate
- Cost per ThruPlay is double the target → flag.
- No Lead in 5 days on a Lead Ad → flag.
- Ad rejected by Facebook → flag immediately.
- Account flagged or paused by Meta → DM Andrew, do not touch.

---

# PART 3 — DAILY / WEEKLY / MONTHLY ROUTINE

A printable rhythm. Stick to it and the system runs even with no robots.

## ☀️ Every day

- [ ] **8:00am ET** — open SmartSuite + Slack + Drive.
- [ ] **8:00am** — read `#team-operations` (last 12h).
- [ ] **8:05am** — run **Robot Job 7** (Daily Ops Check). Post the briefing.
- [ ] **8:30am** — run **Robot Job 8** (Nudge stuck onboarding) for any clients stuck >5 days.
- [ ] **9:00am** — run **Robot Job 4** (pull Close → ConvTracker) for last 24h of calls.
- [ ] **All day** — work Tasks → My Queue from top to bottom. Update Status in SmartSuite as you go (**Robot Job 6**).
- [ ] **Whenever Andrew flips a deal to Won** — run **Robot Job 3** (the big one).
- [ ] **Whenever a no-show happens** — run **Robot Job 2**.
- [ ] **Whenever Calendly fires** (and no robot caught it) — run **Robot Job 1**.
- [ ] **6:00pm** — quiet hours start. No more outbound client messages.
- [ ] **End of day** — leave a one-line wrap in `#team-operations`: `EOD: [what closed], [what's open], [blockers]`.

## 📅 Every week

- [ ] **Monday 8am** — review the week's Campaign metrics (**Robot Job 9** for every Live campaign).
- [ ] **Monday** — for each active client, run a quick Onboarding sweep. Anything stuck?
- [ ] **Wednesday** — check the deprecation list for n8n workflows (the 14 tagged `deprecated` — see `_handoff/patched/n8n_cleanup_log.md`). Flag any you think can be deleted now.
- [ ] **Friday 4pm** — write the weekly client report (one per Live client). Post in `#client-[slug]`.

## 📆 Every month

- [ ] **First Monday** — pull MRR + ARR from Finance app. Update the Financial Metrics Dashboard if numbers are stale.
- [ ] **First Monday** — review every client's status (`Onboarding`, `Active`, `Paused`, `Churned`). Anything wrong?
- [ ] **Mid-month** — clean Drive: archive any test folders, confirm `Raw Video/` for inactive clients can be archived.
- [ ] **End of month** — Finance: confirm setup fees and retainers are invoiced (Andrew owns this — you confirm completeness).

---

# 🚨 WHEN SOMETHING IS WRONG

Stupid simple lookup table. Find the row, do the thing.

| What happened | What to do |
|---|---|
| You posted a `/update` and got ⚠️ | Re-read **Robot Job 6**. Most common: client name doesn't match SmartSuite exactly. Fix and repost. |
| Asset Link in Campaign record is broken | **Stop the build.** Mark Task `Blocked`. Ping Andrew. Wrong video in wrong ad is a real problem. |
| Special Ad Category warning in Ads Manager | Housing isn't selected. Fix in campaign settings before publishing. |
| Facebook rejected the ad | Flag to Andrew immediately with the rejection reason. Don't republish. |
| `Last Pull Date` on a campaign is >48h ago | Windsor sync failed. Run **Robot Job 9** by hand. Then ping Andrew. |
| Client record didn't appear after a Won deal | M5 normally fires within 30s + falls back to a 5-min poll. After 10 min, run **Robot Job 3** by hand. |
| New `#client-<slug>` channel is private | That's the default since Apr 25. Andrew flips public after the client is invited as a guest. **Don't flip it yourself.** |
| Retarget/Lead Ad audiences don't exist | Video Views campaign hasn't accumulated viewers yet. Mark Build Task `Blocked`. Don't proceed. |
| Slack bot says `not_in_channel` | Bot needs guest invite to that channel. Ping Andrew (he handles it). |
| SOP and architecture map disagree | SOP wins for VA-facing workflows. Ping `#team-operations`. |
| Two tasks tell you to do the same thing | **Stop.** Don't act on both. Post in `#team-<client>` — duplicate is a workflow bug, not your problem to paper over. |
| Can't find the SOP linked from a Task | **Stop.** Don't improvise. Post in `#team-<client>`: missing SOP for task `<task-id>`, what should I do? |
| Andrew is unreachable and a campaign needs an urgent decision | **Don't publish.** Pause anything risky. Wait for Andrew. The cost of waiting < cost of a wrong publish. |
| The robots came back online while you were doing manual work | Stop the manual work. Check what state SmartSuite is in. The robots will pick up wherever they are — don't double-write. |

---

# 📋 THE CHEAT SHEET (one-page reference)

## 9 Robot Jobs at a glance

| # | When this happens | You do this |
|---|---|---|
| 1 | New Calendly booking | Make Pipeline record `Booked` + check Close + post in `#team-operations` |
| 2 | Lead no-show | Mark Calendly no-show + send reschedule email (8am–6pm ET only) |
| 3 | Deal Won (Pipeline stage = Won) | **The Big One** — Client + Onboarding + Drive + 2 Slack channels + welcome brief + flip won_processed |
| 4 | A call happens in Close | Add ConvTracker row with exact `last_call_outcome` from Close |
| 5 | New Client missing Drive folder | Make `[Client]/Raw Video/ + Ad Creative/` and write URL back |
| 6 | You finished/blocked work | Edit SmartSuite directly (skip the `/update` Slack flow) |
| 7 | 8am every day | Daily ops briefing in `#team-operations` |
| 8 | A step stuck >5 days | Diagnose + nudge or escalate (one per day, quiet hours) |
| 9 | Live campaign needs metrics | Pull from Ads Manager → paste into Campaign record → update Last Pull Date |

## SmartSuite vocabulary — must match exactly

**Pipeline `Deal Stage`** (10):
`Conversation - Positive` · `Follow Up / Reschedule` · `Booked` · `No Show` · `Cancelled` · `Proposal - Decision - Pending` · `Ghosted` · `Signed - Invoice Sent` · `Won` · `Lost`

**ConvTracker `Last Call Outcome`** (15):
`Owner - Booked` · `Owner - Talked` · `Owner - Maybe` · `Owner - Callback Requested` · `Owner - Not Interested` · `Non-Decision Maker (NDM) Interested` · `Gatekeeper` · `Voicemail` · `No Answer` · `Wrong Number` · `Do Not Call` · `Hung Up - Owner` · `Left Voicemail` · `Voice Agent` · `Invalid`

**ConvTracker `Outcome`** (6, manual):
`Interested` · `Maybe` · `Not Interested` · `No Contact` · `Gatekeeper` · `LVM`

**Tasks `Type`** (13 canonical):
`Set Up Ad Account Access` · `Set Up Lead Forms` · `Send Video Brief` · `Upload Creative` · `Write Script` · `Build Campaign` · `QA Campaign` · `Launch Campaign` · `Cut / Pause Campaign` · `Swap Creative` · `Adjust Targeting` · `Update SmartSuite Records` · `Escalation Follow-Up`

**Tasks `Status`**: `To Do` · `In Progress` · `Blocked` · `Done`

**Onboarding step values**: `1` (Pending) · `2` (In Progress) · `3` (Complete)

**Clients `Status`** (canonical = `status`, ignore `client_status`):
`Onboarding` · `Active` · `Paused` · `Churned`

## Quiet hours

All client-facing comms: **8am–6pm ET only.** Internal Slack OK any time.

## When in doubt

1. Read the SOP for that app.
2. Search `#team-operations` for prior posts about it.
3. Post in `#team-[client]` as a thread (no `/update` prefix).
4. Only DM Andrew if it's urgent + private + above the SOP can answer.

---

*End of Manual Mode Manual. v2026-05-10. If something in this doc is wrong, it's because the system changed and the doc didn't catch up. Trust live SmartSuite and live n8n over the doc; flag the gap in `#team-operations`.*
