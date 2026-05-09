# AgencyOS Hardening Plan — April 19, 2026

**Source:** AgencyOS_Architecture.docx (Apr 2026) — pressure-test section
**Scope:** All 8 weaknesses + 6 bottlenecks + 2 missing steps = 16 items
**Goal:** Remove Andrew's daily operational anxiety so he can focus 100% on sales.

---

## Sequencing principle

Items are ordered by **daily anxiety reduction**, not the report's P1/P2/P3 impact ranking. The report ranks by "system impact." Andrew's ranking is: *what mental load does this take off my plate today?*

Anxiety sources (mapped to items):
- "Did the sync run?" → **W2**
- "Do I need to be at my desk to QA?" → **B1**
- "Is that client about to stall in onboarding?" → **W5**
- "Why is the VA waiting 12 hours?" → **W1, M2, B5**
- "Has that client heard from us?" → **B2**
- "Did the lead even reach the client?" → **B3**
- "Is anyone about to churn?" → **B4**
- "Are we quietly losing Windsor data?" → **W6**
- "What if SmartSuite gets nuked?" → **W8**
- Rest (W3, W4, W7, B6, M1) = hygiene + long-term intelligence. No daily anxiety.

---

## The 5 waves

| Wave | Theme | Items | Days | Outcome (DoD) |
|---|---|---|---|---|
| **1** | Kill daily anxiety | W2, W5, B1 | 3–5 | Silent failures alert to #system-errors. Onboarding auto-escalates stuck steps. VA self-certifies clean QA builds; Andrew reviews edge cases only. |
| **2** | Real-time ops | W1, M2, B5 | 3–4 | 6 critical workflows webhook-triggered (not polled). Deal Won in Close → instant client creation in SmartSuite. Retarget audience task auto-created at 1,000+ thruplays. |
| **3** | Client-facing confidence | B2, B3, B4 | 4–5 | 5 automated client touchpoints live (welcome, 50%/100% onboarding, campaigns live, weekly perf, monthly PDF). Lead delivery verification step in onboarding. Client Health Score computed weekly, churn flag to Andrew DM. |
| **4** | Data integrity | W6, W8 | 1–2 | Unmatched Windsor campaigns reported to Slack. FB Campaign ID stored on SmartSuite records. Weekly SmartSuite export to Drive (4-week rolling). Weekly n8n workflow definition export. |
| **5** | Hygiene + intelligence | W3, W4, W7, B6, M1 | 3–4 | API keys moved to n8n credentials/env. Client alias codes generated on creation. Optimization.decision_outcome field + feedback loop in Intelligence Agent prompt. Creative Log app/sub-table. Organic posting tracked in Onboarding. |

**Total:** ~14–20 days focused build over 3–5 weeks. Most anxiety relief: Waves 1–2 (~1 week).

---

## Execution rules

1. **One wave at a time.** Wave N's DoD is met before Wave N+1 starts. Non-negotiable.
2. **Each item = Manus-ready prompt** with: input, output, definition of done. Signal drafts; Andrew approves; Manus builds.
3. **No new features during hardening.** If a gap surfaces, it goes in **Wave 6 Backlog** at the bottom of this doc. Do not start it.
4. **After each wave:** 24-hour soak test before declaring done. Run the system, watch for regressions, THEN move on.
5. **Sales block is protected.** Wave work happens in 2-hour build blocks, not all-day grinds. Sales calls take priority.

---

## Wave 1 — Kill daily anxiety (3–5 days)

### Item 1.1 — W5: Onboarding SLA enforcement — daily schedule

**Smallest first step (do this first — 2 minutes):** Open n8n → "Onboarding Health Monitor" workflow → change trigger from Manual to Schedule (daily, 7am ET) → save → activate. That's it. Instant anxiety reducer — the system now checks stuck onboardings every morning without you remembering to trigger it.

**Full DoD:**
- Workflow runs daily 7am ET
- Adds `step_started_date` field to Onboarding app (19 step fields → 19 date fields, or one composite "current_step_started" field)
- SLA logic: if step In Progress ≥ 5 days, DM Andrew with client name, stuck step, days stuck
- SLA logic: if step In Progress ≥ 10 days, auto-create Escalation Follow-Up task in SmartSuite

**Manus prompt scope:** Add schedule trigger + add field + add SLA branch nodes + Slack DM. ~2 hours.

### Item 1.2 — W2: Error recovery + #system-errors channel

**DoD:**
- New Slack channel `#system-errors` created
- New n8n workflow `Global Error Handler` (trigger: error workflow) that posts to `#system-errors` with: workflow name, node name, error message, timestamp, execution URL
- All 22 workflows assigned to use this as their error workflow (n8n Settings → Error Workflow)
- 5 critical workflows get retry-on-failure node wrapping (3 retries, exponential backoff): Pipeline Sync, Windsor Metrics, Campaign Intelligence Agent, Deal Won, Sync Agent

**Manus prompt scope:** Create error workflow, assign to all 22, add retry wrappers. ~3 hours.

### Item 1.3 — B1: QA bottleneck → VA self-certification

**This is the big one.** Cannot be Manus-built. Requires Andrew to document his QA brain.

**Phase A — Document (Andrew does this, 30 min during next real QA):**
- Open the next campaign in QA Ready status
- As you QA it, voice-record or type every check you make, in order
- For each check: what you look at, pass criterion, fail criterion
- Output: raw QA checklist v1 (messy is fine)
- Save to: `/Agency OS/SOPs/SOP_05_Campaign_QA_Checklist.md`

**Phase B — Structure (Signal does this, 30 min):**
- Clean Andrew's raw capture into structured checklist
- Split into "Deterministic" (naming convention, budget set, audience matches spec, creative attached — these can be automated in n8n) and "Judgment" (creative feel, copy tone — these need human eyes)
- VA self-cert form built in SmartSuite (checkbox per item, VA signs off)

**Phase C — Build (Manus, ~3 hours):**
- Add `qa_self_cert_status` and `qa_self_cert_by` fields to Campaigns
- Modify `Campaign QA Ready → Slack Checklist` workflow: if VA has self-cert'd all deterministic items AND campaign is a repeat-client standard build, auto-move to "Ready to Launch" with 4-hour hold; Andrew gets DM, reviews only if he wants to
- For first-time clients and non-standard builds: Andrew still reviews (no change)

**Wave 1 DoD:** All three items done + 24h soak test passed (watch the error channel, confirm SLA DMs fire, run one VA self-cert'd campaign end-to-end).

---

## Wave 2 — Real-time ops (backlog — detail when Wave 1 DoD met)

- **W1 — 6 workflows migrated from 12h poll to SmartSuite webhook:** Task Assigned, Onboarding Progression, Prerequisites Met, Campaign QA Ready, Task Blocked, 72hr Review Trigger
- **M2 — Close CRM webhook on Opportunity stage change = Won:** fires Deal Won workflow instantly (not manual trigger)
- **B5 — Retarget Audience auto-trigger:** new n8n workflow, polls Windsor Facebook data every 12h, when any Video Views campaign hits ≥1,000 thruplays AND retarget audiences not yet built, auto-creates "Create Retargeting Audiences" task

---

## Wave 3 — Client-facing confidence (backlog)

- **B2 — 5 automated client touchpoints** via transactional email (Postmark/Resend or Gmail API):
  1. Welcome email on Deal Won
  2. Onboarding 50% complete milestone
  3. Onboarding 100% complete / campaigns being built
  4. Campaigns live notification
  5. Monthly performance report PDF (auto-generated from Campaigns data)
- **B3 — Lead delivery verification:** new Onboarding step (step_lead_delivery_verified), test lead submitted post-Lead Ad launch, `lead_delivery_verified` field on Campaigns, weekly reconciliation check
- **B4 — Client Health Score:** computed field on Clients app, inputs: days since last comm, payment status, campaign performance trend (7-day rolling CPL delta), onboarding completion speed. Weekly n8n job computes score; clients <threshold DM Andrew

---

## Wave 4 — Data integrity (backlog)

- **W6 — Windsor unmatched report + FB Campaign ID:** modify Windsor workflow to collect unmatched rows, post daily summary to Slack. Add `fb_campaign_id` field to Campaigns, store on creation, use for deterministic matching (fallback to name)
- **W8 — Backup automation:** weekly workflow exports all SmartSuite records per app to JSON, drops in `/Agency OS/_Backups/YYYY-MM-DD/`, rolling 4-week retention. Weekly workflow exports all n8n workflow definitions via API to `/Agency OS/_Backups/n8n/`

---

## Wave 5 — Hygiene + intelligence (backlog)

- **W3 — API keys to n8n credentials/env:** mechanical replace across all workflows, reference via `$env.SMARTSUITE_TOKEN`, `$env.CLOSE_API_KEY`, etc. Delete hardcoded strings. Document key rotation runbook
- **W4 — Client alias codes:** 3-letter auto-generated code on Client creation (collision check), Sync Agent accepts either full name or code
- **W7 — Decision feedback loop:** add `decision_outcome` field to Optimization (Correct/Overridden/Pending), override reason field. Include last 10 outcomes in Intelligence Agent prompt
- **B6 — Creative Log:** new sub-table or linked app, entries auto-created on creative swap, Intelligence Agent prompt includes creative history
- **M1 — Organic posting tracked:** add `step_organic_posting` to Onboarding, "Post Organic Content" task type, include in Prerequisites Met check

---

## Tracking

| Wave | Item | Status | Manus Prompt | Notes |
|---|---|---|---|---|
| 1 | W5 — daily schedule toggle | ✅ Done | N/A | Confirmed already active (8:30am daily) |
| 1 | W5 — SLA logic + escalation | ✅ Done | Signal (deployed) | Added Filter + DM Andrew + idempotent Escalation Follow-Up task creation (>=5d blocked) |
| 1 | W2 — Global Error Handler workflow | ✅ Done | Signal (deployed) | New workflow ePyAmNK7lpzoXPgo: Error Trigger → Format → DM Andrew |
| 1 | W2 — wire error handler to all 22 | ✅ Done | Signal (deployed) | 21 wired cleanly + 1 (Task Blocked) also fixed missing Slack credential |
| 1 | W2 — retry wrappers on 5 critical | ✅ Done | Signal (deployed) | 22 nodes wrapped (3 tries, 3s backoff): Pipeline Sync, Windsor, Campaign Intel, Deal Won, Sync Agent |
| 1 | B1 — QA self-cert branch | ✅ Done | Signal (deployed) | User clarified: checklist = SOP_05 9 fields (exist in app). Workflow now splits certified → DM Andrew vs pending → channel checklist |
| 2 | W1 — 6 webhook migrations | ☐ Not started | TBD | |
| 2 | M2 — Close CRM webhook | ☐ Not started | TBD | |
| 2 | B5 — thruplay auto-trigger | ☐ Not started | TBD | |
| 3 | B2 — 5 client touchpoints | ☐ Not started | TBD | |
| 3 | B3 — lead delivery verification | ☐ Not started | TBD | |
| 3 | B4 — Client Health Score | ☐ Not started | TBD | |
| 4 | W6 — Windsor match hardening | ☐ Not started | TBD | |
| 4 | W8 — backup automation | ☐ Not started | TBD | |
| 5 | W3 — API keys to env | ☐ Not started | TBD | |
| 5 | W4 — client alias codes | ☐ Not started | TBD | |
| 5 | W7 — decision feedback loop | ☐ Not started | TBD | |
| 5 | B6 — Creative Log | ☐ Not started | TBD | |
| 5 | M1 — organic posting tracked | ☐ Not started | TBD | |

---

## Wave 6 Backlog (things that surface during Waves 1–5)

*Do not start these during hardening. Log here and review after Wave 5.*

- Resend API key vaulted in n8n credentials (id: `wdhGGFni4NSjAv1d`, name "Resend API (B2 client emails)") — ready for Wave 3 B2 build
- `#system-errors` channel: Slack MCP has no channel-create. Currently routing errors to Andrew DM. Andrew can create the channel manually later (30 sec in Slack UI) and ask Signal to swap the target in Global Error Handler (1 line change)
- Close CRM admin access confirmed — unblocks Wave 2 M2 (Opportunity Stage Change = Won webhook → Deal Won workflow)

---

## Filter for every decision during this build

> Does this close a deal, deliver for a client, or build the system that does one of those two things? If not, it's noise.

If any item expands beyond the spec above, Signal flags it as scope creep. No negotiation.
