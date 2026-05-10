# 📊 Optimization App — How to Use It

**App:** Optimization (`69ce67e01cc0855f89fee02e`, slug `sph5lmp9`)
**Last updated:** 2026-05-10
**Purpose:** Track performance review cycles for live campaigns. n8n flags what to review. Andrew decides what to do.
**Who uses this:** n8n (creates review records and writes data), Andrew (reviews and decides).
**Your default view:** Pending Reviews
**Source of truth:** Live SmartSuite Optimization app + Decision Router workflow output. VAs do not touch this app.

---

## What This App Is For

The Optimization app is where campaign performance decisions get made. Every live campaign gets reviewed on a schedule — n8n creates the review record, pulls in the latest metrics, and flags whether the campaign should be killed, scaled, or left running.

Andrew looks at the flagged review, checks the numbers, and makes the call. The decision gets logged here so there's a full history of what was done and why.

**VAs do not work in this app.** This is Andrew's decision layer.

---

## How the Review Cycle Works

### The Trigger
n8n automatically creates a review record in this app when:
- A campaign has been live for **72 hours** (first review)
- A campaign has been live for a set number of days after the last review (ongoing reviews)

### What n8n Fills In
When a review record is created, n8n pulls in the latest metrics from Windsor AI:
- Spend
- ThruPlays and Cost/ThruPlay
- Views (50%, 75%, 95%)
- Saves, Shares, Comments, DMs
- Leads and Cost/Lead

### What Andrew Does
1. Open **Optimization** app → **Pending Reviews** view.
2. Find the review record (sorted by Review Date).
3. Look at the metrics and the n8n recommendation (if one has been generated).
4. Apply the decision rules below.
5. Log the decision in the record.
6. The campaign record in the Campaigns app gets updated accordingly.

---

## Decision Rules — What to Do With the Numbers

These are the rule-based thresholds. Apply them consistently.

### Video Views Campaigns

| Metric | Threshold | Action |
|---|---|---|
| Cost/ThruPlay | > $0.15 | ⚠️ Review — consider new creative or new audience |
| Cost/ThruPlay | < $0.05 | ✅ Scale — increase daily budget by 20% |
| Saves rate | High relative to other campaigns | 🏆 Winner — flag as a winning creative. Increase budget. |
| ThruPlays < 100 after $50 spend | | ❌ Kill — creative or audience isn't working |

### Retarget Campaigns

| Metric | Threshold | Action |
|---|---|---|
| Audience size < 1,000 | | ⚠️ Hold — retargeting pool is too small. Keep Video Views running longer. |
| Cost/result | High with no engagement | ❌ Kill — the warm audience isn't converting to engagement |
| DMs or link clicks | Strong | ✅ Scale — this is working |

### Lead Ad Campaigns

| Metric | Threshold | Action |
|---|---|---|
| Cost/Lead | > $50 | ❌ Kill or Pause — not efficient |
| Cost/Lead | < $20 | ✅ Scale — increase budget. This is working. |
| No leads after $100 spend | | ❌ Kill — the offer or audience isn't right |

---

## How to Log an Optimization Decision

1. Open the review record.
2. Look at the metrics. Apply the decision rules above.
3. Decide: **Scale / Hold / Pause / Kill / New Creative**
4. Update the linked **Campaign** record in the Campaigns app:
   - If Killing → change Campaign Status to **Cut**
   - If Pausing → change Campaign Status to **Paused**
   - If Scaling → update the **Daily Budget** field to the new amount (then update in Ads Manager)
5. Log your decision in the review record notes so there's a paper trail.
6. Change the review record Status to **Reviewed**.
7. The record will move from **Pending Reviews** to **Decision Log**.

---

## Key Fields Explained

| Field | What It's For |
|---|---|
| **Review Date** | When this review is due. Work reviews in date order — oldest first. |
| **Next Review Date** | When the next review should happen after this one. n8n sets this automatically. |
| **Campaign** | The linked campaign record being reviewed. |
| **Decision** | Scale / Hold / Pause / Kill / New Creative. Your call based on the numbers. |
| **Decision Notes** | Why you made this decision. Brief is fine — 1–2 sentences. |

> ⚠️ The **Review Date** field was previously mislabelled "Launch Date" in the UI. If you see "Launch Date" in the Optimization app column header, it's actually the Review Date. Same for "72hr Review Date" = Next Review Date. Andrew needs to rename these in the UI (it's a 30-second fix — right-click the column header → Rename).

---

## Winner Identification

A **Winner** is a campaign where:
- Saves rate is significantly higher than other campaigns running at the same time
- ThruPlays are high and Cost/ThruPlay is low
- The content is resonating (comments like "this is exactly my situation", DMs coming in)

When you identify a winner:
1. Note it in the review record.
2. Flag it in the linked Campaign record (there's a **Winner Reviews** count field).
3. The winning video should be used as a base for new ad creative — same topic, different framing or opening hook.

---

## Views

| View | When to Use It |
|---|---|
| **Pending Reviews** | Andrew's daily check. Campaigns that need a decision today. |
| **Decision Log** | Historical record of every optimization decision made. Use to spot patterns over time. |

---

## What NOT to Do

- ❌ VAs do not touch this app. Optimization decisions are Andrew's responsibility.
- ❌ Do not skip a review because the campaign looks fine. Even good campaigns need the review logged.
- ❌ Do not kill a campaign without logging the reason. You need the data trail.
- ❌ Do not scale a campaign by more than 20% at a time. Facebook's algorithm needs time to adjust.

---

## If Something Looks Wrong

| Problem | What to Do |
|---|---|
| Metrics look blank or zero in the review record | Windsor sync may have failed. Check Last Pull Date in the Campaigns app. |
| No review records appearing for campaigns that have been live 72+ hours | n8n may have failed to create the review. Check #team-operations Slack channel. |
| Review Date says "Launch Date" | The column header needs renaming in the UI. This is a known issue — see above. |
| A campaign I killed is still showing as Live in Campaigns app | Manually update the Campaign Status to Cut. Then investigate why n8n didn't update it. |
