# RequityAI — Campaign Optimization SOP
## Script-Driven Review & Decision System · $50/Day Minimum Spend

**Date:** 2026-04-12
**Status:** DRAFT — Needs Andrew's review
**Companion to:** Client Facebook Campaign SOP (VA execution) + AgencyOS SmartSuite Structure Spec
**Core rule:** Andrew / client chooses which videos run. The VA builds, launches, checks, tracks, and recommends. Andrew approves all kill/scale decisions.

---

## How This Works

Windsor AI pulls metrics into SmartSuite via n8n every 24 hours. The VA reviews at the 72-hour mark using the 5-step framework below, writes a recommendation, and Andrew approves or overrides. The optimization tracker is not a diary — it is a decision system. Every row must end with a decision and a next action.

****Script ID is the primary key** for everything.** The script library already carries the property situation, bucket, hook, and file name. The VA never recreates that metadata. The naming convention embeds Script ID into every ad set name in Ads Manager, so Windsor metrics map directly back to the exact script. This is how you see "TL-B4-14 is a $0.03 CPT winner across Dallas and Phoenix — test it in C2" instead of "some video is doing well somewhere."

---

## The Naming Convention Chain

This chain must be unbroken from script creation to optimization tracking. If any link breaks, you lose the ability to trace performance back to the source.

```
SCRIPT ID FORMAT:  [SITUATION CODE]-B[#]-[SCRIPT ##]
Example:           FC-B2-14  (Foreclosure, Bucket 2, Script 14)

SITUATION CODES:
  PRO = Probate / Inherited Properties
  VAC = Vacant Properties
  TL  = Tired Landlords / Problem Tenants
  REP = Major Repairs & Code Issues
  CLN = Heavy Cleanouts
  FC  = Foreclosure
  TAX = Tax Delinquency
  OOS = Out-of-State / Remote Owners
  DIV = Divorce
  DWN = Downsizing & Relocation
  FWD = Fire & Water Damage
  GTP = General Timeline Pressure

SCRIPT LIBRARY (Google Drive)
  File: [Property Situation] - Bucket [#] - Script [##].mp4
  Example: Foreclosure - Bucket 2 - Script 14.mp4
  Script ID: FC-B2-14

        ↓ maps to ↓

ADS MANAGER (Campaign 1 — Video Views)
  Campaign:  TOF | EDU VIDEO | [MARKET]
  Ad Set:    W[1-4] | [WEEKLY THEME] | [SCRIPT ID]
  Ad:        [SCRIPT ID] | V1
  Example:   W1 | Urgency | FC-B2-14

        ↓ Windsor AI pulls metrics ↓

SMARTSUITE — CAMPAIGNS APP
  Campaign Record Name:  TOF | EDU VIDEO | Dallas
  Script ID:             FC-B2-14
  Script File:           Foreclosure - Bucket 2 - Script 14.mp4
  Script Link:           [Google Drive URL]
  All metrics attached to this record

        ↓ 72-hour review triggers ↓

SMARTSUITE — OPTIMIZATION APP
  Script ID:   FC-B2-14
  Market:      Dallas
  Decision:    KEEP
  Why:         Strong 75% depth, 6 saves, 2 "OPTIONS" comments
  Next Action: Queue for MOF retarget test at Week 3
  Re-Review:   2026-04-18
```

**The VA's job at every step:** confirm the Script ID matches end-to-end before looking at a single metric. If the naming is wrong, fix it first.

---

## Budget Reality at $50/Day

| Campaign | Launch | Budget | Notes |
|----------|--------|--------|-------|
| C1 — Video Views | Day 1 | $10/day per ad set (5 videos = $50) | Full budget at launch |
| C2 — Retarget | ~Week 3 | $10–20/day (freed from C1 kills) | Only when warm audiences exist (1,000+ in VV75) |
| C3 — Lead Ads | ~Month 2 | $10–15/day (freed from C1 kills + optional client increase) | Only when hot audiences exist (500+ in VV95) |

Every day a bad video runs at $10 is $10 that could be building the right audience or generating leads. The optimization system's first job is killing C1 losers fast to free budget for C2/C3.

**Housing Category tax:** Special Ad Category = Housing removes detailed targeting. Expect CPMs 1.5–2× higher than non-housing. All thresholds below account for this.

---

## Review Cadence

| Review | When | Who Reviews | Who Approves |
|--------|------|-------------|-------------|
| 72-Hour First Review | 72hrs after any ad set launches | VA | Andrew |
| Day 7 Follow-Up | 7 days (for "WATCH" decisions only) | VA | Andrew |
| Weekly Review | Every Friday | VA pulls, recommends | Andrew decides |
| Monthly Review | 1st of month | Andrew | Andrew |

---

## The 5-Step Review Framework

Every review follows these 5 steps in order. No skipping.

### Step 1 — Confirm the Asset

Before touching a single metric, verify:

| Check | What to Confirm |
|-------|----------------|
| Script ID | Matches the script library |
| File name | Correct video file uploaded |
| Campaign name | Matches naming convention |
| Ad set name | Contains correct Script ID, bucket, market |
| Ad name | Matches convention |
| Market / Geo | Correct client market |
| Identity | Correct Facebook Page + Instagram account |

If anything is wrong here, flag it. Don't review performance on a misattributed asset.

### Step 2 — Check Attention Quality

**Metrics:** ThruPlay volume, Cost / ThruPlay, 50% / 75% / 95% view depth.

This tells you whether people are watching. The deeper they watch, the more valuable the warm audience being built.

| Metric | What It Tells You |
|--------|------------------|
| Cost / ThruPlay | How efficiently you're buying attention. ThruPlay = 15-second view. |
| 75% View Rate | The money metric for C1. These people go into your retarget audiences. |
| 95% View Rate | Your hottest viewers. These feed C3 lead ads. |
| View depth ratio (95% ÷ ThruPlay) | How compelling the content is after the hook. High ratio = strong message, not just a good hook. |

**Guideline thresholds for C1 at 72 hours ($30 spent):**

| Signal | Strong | Acceptable | Weak |
|--------|--------|------------|------|
| Cost / ThruPlay | < $0.03 | $0.03–$0.08 | > $0.08 |
| 75% View Rate | > 25% | 15%–25% | < 15% |
| 95% View Rate | > 12% | 5%–12% | < 5% |
| View depth ratio | > 40% | 20%–40% | < 20% |

These are guidelines, not laws. A video with a $0.09 CPT but 30% 75-view rate might be worth keeping — the audience quality is high even if cost is above the line. Use the thresholds to orient, then apply judgment.

### Step 3 — Check Response Quality

**Metrics:** Saves, shares, total comments, OPTIONS comments.

This tells you whether people care enough to act. Attention without response builds audiences; response signals intent.

| Signal | What It Means |
|--------|--------------|
| Saves | Strongest passive signal. Person wants to come back to this. Content resonated personally. |
| Shares | Organic reach multiplier. Person found it valuable enough to send to someone else. |
| Comments (Total) | Volume signal — people are responding. Pulled automatically by Windsor. |
| OPTIONS Comments | **The intent signal.** The CTA is "comment OPTIONS below." This is someone raising their hand. VA counts these manually at each review by checking the actual ad comments. |

Windsor pulls total comment count automatically. But it can't read the content of those comments — it just gives you a number. So the VA's job at every review is to check the ad's comment section and count how many are "OPTIONS" or similar intent language ("interested", "need help", "what are my options", etc.) versus noise ("nice video", spam, irrelevant).

**Two comment fields in SmartSuite:**
- **Comments (Total)** — Windsor via n8n (automated)
- **OPTIONS Comments** — VA manual count at review (the number that actually matters)

**Guideline thresholds for C1 at 72 hours:**

| Signal | Strong | Some Signal | Weak |
|--------|--------|-------------|------|
| Saves | > 5 | 2–5 | < 2 |
| Shares | > 3 | 1–3 | 0 |
| OPTIONS Comments | > 2 | 1 | 0 |
| Total Comments | > 5 | 2–5 | < 2 |

**Important:** A single "OPTIONS" comment outweighs 10 saves. Someone publicly asking for help is the highest-intent signal in the C1 funnel. Two OPTIONS comments on a $30 ad set = RETARGET TEST minimum, regardless of view depth.

### Step 4 — Check Pain-Angle Clarity

This is the qualitative step that n8n cannot automate. The VA asks:

**"Is the reason this video worked (or didn't) obvious and strategically useful?"**

| Good clarity | Bad clarity |
|-------------|------------|
| "Foreclosure urgency resonated — comments reference timeline pressure" | "Numbers are okay but I don't know why" |
| "Pre-foreclosure hook got attention but message lost them — 95% view rate dropped hard" | "It just didn't work" |
| "Inherited property angle driving OPTIONS comments — people tagging family members" | "Low engagement" |

If you can't articulate *why* a video worked or failed, the recommendation is incomplete. The "Why" column in the tracker is not optional — it's how you learn which pain angles convert and which don't. Over time, this data tells you: "Foreclosure + urgency hooks are 3× more efficient than probate + empathy hooks in the Dallas market."

### Step 5 — Make One Recommendation

Every reviewed Script ID gets exactly one recommendation. No fence-sitting.

| Decision | Use When | Next Move |
|----------|----------|-----------|
| **KEEP** | Watch depth is healthy, audience-building value is good, engagement is relevant | Leave active, review again next cycle |
| **CUT** | Watch depth is weak, relevance is weak, not building useful warm audiences | Pause and reallocate budget to next best option |
| **RETARGET TEST** | Pain angle is clear and audience feels warmed but not ready for direct lead ask | Queue MOF version with stronger proof/options messaging |
| **LEAD AD CANDIDATE** | Message naturally supports a direct downstream CTA, intent is visible | Flag for BOF test when warm audience is ready |
| **SCALE** | Exceptional performance across all metrics — proven winner | Increase budget to $15–20/day, pull from killed ad sets |
| **WATCH** | Mediocre but not dead — some signal exists | Keep at current budget, final decision at Day 7 |

**Day 7 rule for WATCH decisions:** If metrics improved, move to KEEP. If flat or declined, CUT. No second extensions. Day 7 is the last call.

---

## Campaign-Specific Rules

### Campaign 1 — Video Views (TOF)

This is where 100% of the optimization action happens in Month 1. One video per ad set, $10/day, 72-hour review.

**Quick decision matrix (all four columns must align for an auto-recommendation):**

| Decision | Cost/ThruPlay | 75% View Rate | 95% View Rate | Saves |
|----------|--------------|---------------|---------------|-------|
| CUT | > $0.08 | < 15% | < 5% | < 2 |
| WATCH | $0.03–$0.08 | 15%–25% | 5%–12% | 2–5 |
| KEEP | < $0.05 | > 20% | > 12% | > 3 |
| SCALE | < $0.03 | > 30% | > 15% | > 5 |

**Override conditions (these beat the matrix):**
- **95% View Rate > 12% → KEEP minimum**, even if CPT and saves are weak. People who watch are watching *all of it*. The message is strong — the problem is likely the hook (first 3 seconds). Don't kill the script; re-record with a better opening and test again.
- 2+ OPTIONS comments → RETARGET TEST minimum, regardless of view depth
- 1 OPTIONS comment + saves > 3 → KEEP minimum, regardless of cost metrics
- View depth ratio > 50% with weak saves → KEEP (content is compelling, audience just isn't engaging publicly)
- High total comments but 0 OPTIONS → engagement without intent. Don't confuse noise for signal. Still a CUT if view depth is weak.

### Campaign 2 — Retarget (MOF)

**Launch gate:** VV75 | 90D audience ≥ 1,000 people AND at least $10/day freed from C1 kills.

| Check | Action |
|-------|--------|
| Frequency > 3 in 72hrs | Audience too small. PAUSE, let C1 build the pool. |
| CPM > $50 | Too expensive. Consolidate ad sets, focus on hottest pool only. |
| Zero engagement on warm audience | Creative problem, not audience problem. Test different proof/urgency angle. |
| Strong engagement, no downstream intent | KEEP. Warming is working but they're not ready for the ask yet. |

### Campaign 3 — Lead Ads (BOF)

**Launch gate:** VV95 | 30D audience ≥ 500 OR VV75 | 90D ≥ 2,000. Client has confirmed lead routing works (test lead received).

**CPL targets for RE investor leads:**

| Range | Assessment | Action |
|-------|-----------|--------|
| < $20 | Excellent | SCALE if quality holds |
| $20–$50 | Good | KEEP, monitor quality |
| $50–$80 | Acceptable | KEEP, tighten form or narrow audience if quality is weak |
| $80–$120 | Concerning | Review creative and audience. Consider Higher Intent form. |
| > $120 or $45+ with zero leads | CUT threshold | PAUSE, review everything before relaunch |

**Non-negotiable quality check after first 5 leads:**
- Response rate to client outreach: target > 40%
- Correct market: target 100%
- Real property situation: target > 60%

If quality fails: switch to Higher Intent form type and narrow to VV95 | 30D only.

---

## Required Tracker Format

Every optimization record in SmartSuite must include:

| Field | Example | Why It Matters |
|-------|---------|---------------|
| Script ID | FC-B2-14 | Primary key — tells you situation (Foreclosure), angle (Bucket 2 How-To), and script number at a glance |
| Market | Dallas | Same script can perform differently across markets |
| Campaign Type | Video Views / Retarget / Lead Ad | Determines which thresholds apply |
| Review Date | 2026-04-15 | When this review was done |
| Decision | KEEP / CUT / RETARGET TEST / LEAD AD CANDIDATE / SCALE / WATCH | One decision, no fence-sitting |
| Why | "Strong 75% depth (28%), 6 saves, 2 OPTIONS comments. Foreclosure urgency resonating." | The strategic insight. This is how you learn what works. |
| Next Action | "Queue MOF retarget test at Week 3" or "Pause and reallocate $10 to VAC-B2-07" | Specific, actionable |
| Re-Review Date | 2026-04-18 | When to look at this again |
| All metrics at time of review | Spend, CPT, view depths, saves, shares, total comments, OPTIONS comments, leads, CPL | Snapshot for trend analysis |

**The Why column is the most valuable data in the entire system.** After 20 reviews, you can pattern-match: "Every script with a deadline hook in Foreclosure outperforms open-ended empathy hooks by 2×." That's how you brief clients on what to record next.

---

## Monthly Budget Reallocation

### Month 1: Build the Warm Audience Machine

| Week | C1 (Video Views) | C2 (Retarget) | C3 (Lead Ads) | Total |
|------|------------------|---------------|---------------|-------|
| W1 | $50 (5 scripts × $10) | — | — | $50/day |
| W2 | $50 (reviewing at 72hr) | — | — | $50/day |
| W3 | $30 (3 keepers) | $10–20 (if audience gate met) | — | $50/day |
| W4 | $30 | $20 | — | $50/day |

*Killing 2 losers by end of W1 frees $20/day for C2.*

### Month 2: Start Generating Leads

| Week | C1 | C2 | C3 | Total |
|------|----|----|----|----|
| W5–6 | $20 (2 best scripts) | $15 | $15 (if audience gate met) | $50/day |
| W7–8 | $20 | $15 | $15 | $50/day |

*If zero leads by end of Month 2, escalate to Andrew for full creative review.*

### Month 3+: Optimize for ROI

| Focus | Budget | Logic |
|-------|--------|-------|
| C1 | $15–20 | Only proven winners + new script tests at $10/day |
| C2 | $10–15 | Maintain warm audience engagement |
| C3 | $15–25 | Shift budget toward cheapest quality leads |

**When client increases beyond $50/day:**
First $10 → C3 (more leads). Next $10 → C1 (test new scripts). Next $10 → C2 (broaden retargeting).

---

## n8n Automation Layer

### What n8n Does Automatically

1. **Every 24 hours:** Windsor AI pulls per-ad-set metrics, writes to SmartSuite Campaigns app. Parses Script ID from ad set name.
2. **At 72 hours after launch:** Creates a review record in the Optimization app with all metrics pre-populated. Sets status to "Pending Review."
3. **Flags obvious kills:** If Cost/ThruPlay > $0.10 AND 75% View Rate < 10% AND 95% View Rate < 5% AND Saves < 2, auto-flags as "RECOMMENDED: CUT" and notifies Andrew via Slack. If 95% is above 12%, blocks the kill — content is compelling, hook needs rework.
4. **Flags obvious winners:** If Cost/ThruPlay < $0.03 AND 75% View Rate > 30% AND 95% View Rate > 15% AND Saves > 5, auto-flags as "RECOMMENDED: SCALE" and notifies Andrew.

### What n8n Does NOT Do

- n8n does not pause or turn off ad sets. Andrew or the VA does that in Ads Manager after approval.
- n8n does not assess pain-angle clarity (Step 4). That's human judgment.
- n8n does not override Andrew's decisions.

### What the VA Does

1. Reviews the pre-populated 72-hour record in SmartSuite
2. Runs the 5-step framework (confirm asset, attention, response, pain-angle, decide)
3. Writes the recommendation: Decision + Why + Next Action + Re-Review Date
4. Submits for Andrew's approval

### What Andrew Does

1. Reviews VA recommendation in SmartSuite or Slack notification
2. Approves, overrides, or asks for more info
3. VA executes the approved action in Ads Manager

---

## Cross-Script Performance Analysis (Monthly)

This is the strategic payoff of Script ID tracking. At the monthly review, Andrew looks across all scripts and markets to answer:

| Question | How to Answer |
|----------|--------------|
| Which property situations convert best? | Group by property situation, compare avg CPT and save rate |
| Which buckets have the best hooks? | Group by bucket #, compare 75% view rate |
| Which scripts work in multiple markets? | Same Script ID across markets — compare CPT and engagement |
| What should the client record next? | Look at RETARGET TEST and LEAD AD CANDIDATE flags — which pain angles are the strongest? |
| Where is budget being wasted? | Scripts with WATCH → CUT pattern = slow decision-making costing money |

This analysis feeds directly back to the video brief sent to clients: "Record more Foreclosure urgency scripts like FC-B2-14, FC-B1-26. Stop recording probate empathy scripts — they're not converting in your market."

---

## Windsor AI — What's Automated vs. Manual

**Confirmed available via Windsor (n8n automates):**
- Spend, impressions, reach → `amount_spent`, standard fields
- Saves → `actions_onsite_conversion_post_save`
- Shares → `actions_post`
- Comments (total count) → `actions_comment`
- Post Engagement → `actions_post_engagement`
- 3-Second Video Views → `actions_video_view`

**Needs testing once Windsor is connected (likely available but unconfirmed):**
- ThruPlay (15-sec views), 50%/75%/95% video view depth, Frequency, CPM
- Windsor claims 560+ metrics from Meta's Marketing API which includes these — but their docs load dynamically so exact field names need a live test pull.

**Always manual (VA at each 72-hour review):**
- OPTIONS comments count — Windsor gives total comment count, not content. VA checks the actual ad comments and counts intent replies ("OPTIONS", "interested", "need help", etc.)
- Video depth metrics — IF Windsor doesn't expose ThruPlay/75%/95%, VA pulls from Ads Manager. 5 minutes per ad set.

**Action:** Once Windsor is connected to n8n, do a test pull on one live ad set and check which fields come back. That's the definitive answer. Everything above is the fallback plan.

---

## Remaining Open Questions

1. **CPL calibration:** The $20–$80 "good" range is based on general RE investor lead gen. If you have actual CPL data from prior campaigns, those should override.

2. **Auto-kill confidence:** Currently n8n flags but doesn't execute. Do you want a "high confidence auto-kill" tier (e.g., $60+ spent with zero ThruPlays = obvious broken delivery)?

3. ~~**Script ID format:**~~ **RESOLVED.** Format is `[SITUATION CODE]-B[#]-[SCRIPT ##]` (e.g., TL-B4-14 = Tired Landlords, Bucket 4, Script 14). 12 situation codes defined. Embeds property situation + content angle + script number in one identifier that flows through the entire system.
