# Claude Code — AgencyOS Full Audit + VA Handoff Mission (May 9, 2026)

You are Claude Code working inside Andrew Cherry's RequityAI AgencyOS repo. This document is your full brief. It is self-contained — do not assume any prior conversation context.

---

## THE REAL GOAL

Andrew is in mass-confusion mode on AgencyOS. There are stale docs, overlapping SOPs, retired workflows still referenced in copy, and contradictions across the 6 most recent V2 drafts. He cannot hand AgencyOS to a VA today and have them plug-and-play.

**Your job has two parts:**

1. **Audit + reconcile.** Find every error, overlap, and contradiction across docs, n8n, SmartSuite, Slack, and Drive. Fix the doc layer. For system-layer fixes (n8n, SS schema, Slack channels), flag and escalate per CLAUDE.md — do not edit live infra without approval.

2. **Produce ONE VA handoff document** — a single, comprehensive, plug-and-play Operator Manual that lets any new VA execute the full client lifecycle without ambiguity. This document supersedes the current scattered SOPs from the VA's perspective. Andrew will keep the SOP-per-app structure for system maintenance, but the VA reads ONE document.

Quality bar: a VA who has never seen RequityAI before can read this document, open SmartSuite + Slack + Ads Manager, and execute their first day correctly without asking Andrew anything that the doc could have answered.

---

## MANDATORY PRE-FLIGHT (read in this order)

1. `CLAUDE.md` — your operator role, escalation rules, scope boundaries.
2. `AgencyOS_Current_State.md` — last updated Apr 20. **Treat as partial truth — verify against live.**
3. `AgencyOS_SmartSuite_Structure_Spec.md` — SmartSuite reference. **Read before any SS probe or write. No exceptions.**
4. `AgencyOS_Architecture_AtoZ_Apr26.md` — most current architecture map.
5. `AgencyOS_Handoff_Apr25.md` — recent handoff context.
6. `AgencyOS_SS_Automation_Wave6.md` — deferred Tier 2 items.
7. `AgencyOS_Audit_Verdict_Apr20.md` and `AgencyOS_Hardening_Plan_Apr19.md` — prior audits. Calibration only; do not assume conclusions still hold.
8. The six V2 draft artifacts in `_handoff/`:
   - `RequityAI_Operator_Guide_V2.txt`
   - `SOP_03_Clients_V2.txt`
   - `SOP_04_Onboarding_V2.txt`
   - `SOP_05_Campaigns_V2.txt`
   - `SOP_06_Tasks_V2.txt`
   - `SOP_09_Slack_Communication_V2.txt`
9. Existing markdown SOPs in `SOPs/` (01–08). Compare against V2 — there will be drift.

If any are missing, stop and ask Andrew before proceeding.

---

## PHASE 1 — LIVE SYSTEM AUDIT

You have n8n Cloud API access (key `signal-new-never-expires`, no expiry) and SmartSuite API access. Pull live truth before trusting any doc.

### 1.1 SmartSuite — full inventory of all 8 apps

For each of: Pipeline, Conversation Tracker, Clients, Onboarding, Campaigns, Tasks, Optimization, Finance:

- App ID + slug
- All field labels, slugs, types, choice lists (full enumeration of every dropdown)
- Record count
- Status of any workflow-controlled fields (which n8n workflow writes them)

Save raw output to `_handoff/audit/smartsuite_inventory.md`.

**Specific must-capture choices:**
- Tasks `type` field — full ordered list with slugs
- Tasks `status` field — full list
- Pipeline `deal_stage` field — full list (memory says 10 per Apr 18; SOP_09 V2 says 11 with NDM — find the truth)
- ConvTracker `last_call_outcome` field — should be 15 per May 6 expansion
- Onboarding step fields — 3-state dropdowns. Count them. SOP_04 V2 prose says 19, enumerates 18; resolve.
- Clients `status` and `niche` fields
- Campaigns `status` and `campaign_type` fields

### 1.2 n8n — full inventory of active workflows

- Pull all workflows. Mark active vs inactive.
- Memory says count went 28→21 on Apr 26 audit. State doc still says 24. Verify.
- For each active workflow: ID, name, trigger type (cron / webhook / errorTrigger), what it writes, last execution result.
- Look specifically for: zombie scheduleTriggers (stale `staticData` — memory has 3 candidates pending forensics post-Apr 19 incident); workflows referencing retired entities (Close Pipeline, "Create Retargeting Audiences" task, dead channel `C0AKWU4H8C8`); workflows that duplicate each other.
- Capture the SmartSuite Sync Agent parser (`8tdPtQWO4qDKEjgq`) — extract its hardcoded valid task type list, status enums, app routing logic. This is the runtime contract that the docs must match.

**Windsor metrics pipeline — explicit verification (paid plan activated 2026-05-09):**
- Workflow `ZwXd0unFysJjWl1M` ("Windsor AI → SmartSuite Metrics"). Pull last 14 days of executions. Confirm green status. Flag any red run with the error message.
- Confirm sync interval. Default 12h. Andrew's recommended new target: 4h. Note current value, flag for change if not 4h.
- Pull the list of FB Ad Accounts connected as Windsor data sources (via Windsor API or workflow node config). Cross-reference against the 4 active clients in the Clients app. Report which are connected and which are missing.
- For each connected ad account, confirm n8n knows the SmartSuite Client record it maps to (so metrics land on the right Campaign). If the mapping is missing/broken for any client, that's a P1 finding.
- Capture the Campaign Intelligence Agent workflow (`6TuDo3mqBZSBF667`) — confirm it reads from the Campaigns metric fields, document its decision thresholds, and confirm it's currently active (it's described as dormant in SOP_09; verify whether "dormant" means deactivated or just idle-with-no-data).

Save to `_handoff/audit/n8n_inventory.md`. Save Windsor-specific findings to `_handoff/audit/windsor_pipeline_status.md`.

### 1.3 Slack — channel inventory

- Confirm `#team-operations` (C0AKWU4835E) is live; `#team-tasks` is the old name; `C0AKWU4H8C8` is dead.
- For each active client (Real-Vantage, First Integrity Home Buyers, Quick Home Buyers, Ritsel Notes): confirm both `#team-<slug>` (private) and `#client-<slug>` (public) exist. Note exact slugs.
- Identify any orphaned channels (old clients) and any missing pairs.

Save to `_handoff/audit/slack_inventory.md`.

### 1.4 Google Drive — folder structure

- Confirm RequityAI parent folder (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`).
- For each active client: confirm `RequityAI/<Client>/Raw Video/` and `RequityAI/<Client>/Ad Creative/` exist.
- Confirm script library + niche-specific video brief docs referenced by M5 (`SCRIPT_DOC_BY_NICHE` map).

Save to `_handoff/audit/drive_inventory.md`.

### 1.5 Cross-system referential integrity

- Every Client record's `slack_channel_id` resolves to a real channel.
- Every Client record's `drive_folder_url` resolves to a real folder.
- Every active Onboarding record has a Client link.
- Every active Campaign record has a Client link and a Platform Campaign ID (or is in Draft).
- Pipeline `close_lead_id` fields populated for Booked+ stage records (per Apr 26 hydration shipped).

Save findings to `_handoff/audit/referential_integrity.md`.

---

## PHASE 2 — RECONCILE

Compare live truth (Phase 1 outputs) against the documentation layer (V2 drafts + existing markdown SOPs + Operator Guide + Current_State doc + memory rules).

### 2.1 Known misalignments to confirm or resolve

These were identified in a prior diagnostic pass. Confirm each against your Phase 1 audit:

| ID | Issue | Source of truth |
|---|---|---|
| M1 | SOP_06 and SOP_09 list different "15 Task Types" — only ~4 overlap | Live Tasks `type` choices (1.1) AND Sync Agent parser (1.2) must agree |
| M2 | "Create Retargeting Audiences" task should be retired (May 5) but appears in 4 of 6 docs | Check live Tasks dropdown — if still present, escalate to Andrew before patching docs |
| M3 | SOP_04 says 19 onboarding steps, enumerates 18; SOP_09 enumerates 17 + master | Live Onboarding step field count (1.1) |
| M4 | Operator Guide section 2 implies prospects self-book | Memory rule: Andrew books on the call. Re-word to remove self-book implication |
| M5 | Operator Guide section 4 describes CIA as actively running | Live Campaigns app has 1 test record, 0 real builds → CIA is dormant. SOP_09 line 139 already says this |
| M6 | SOP_09 lists 11 Pipeline stages incl. NDM | Live Pipeline `deal_stage` (1.1). NDM may belong to ConvTracker `last_call_outcome` instead |
| M7 | `AgencyOS_Current_State.md` is Apr 20-stale | Update to today (2026-05-09) reflecting Apr 22, Apr 26, May 5, May 6 events |

### 2.2 Open-ended audit (find what wasn't enumerated)

Apply this lens to every doc and every active workflow:

- **Vocabulary drift.** Same concept, different name across docs (e.g., "Create Retargeting Audiences" vs no-such-task; "team-tasks" vs "team-operations"; "Prospect" vs "Lead"; "Build Campaign (CSV Import)" vs "CSV Import Build").
- **Retired workflows still referenced.** Anything pointing at Close Pipeline (retired Apr 19), the M2 webhook (replaced Apr 22), zombie cron triggers, or dead Slack channels.
- **Orphaned tasks/SOPs.** SOPs for apps or processes no longer in scope. Tasks types in the SmartSuite dropdown that no automation creates.
- **Missing SOPs.** Workflows that exist in n8n but have no corresponding doc explaining what the VA should do when they fire.
- **Contradictory rules.** Two docs giving different instructions for the same situation.
- **VA decision points without guidance.** Places where a VA must choose between options but no SOP tells them which.
- **Escalation gaps.** Things that should escalate to Andrew but the docs don't say so.

### 2.3 Reconciliation output

`_handoff/audit/reconciliation.md` — for each issue (M1-M7 + everything Phase 2.2 surfaced):

- What live truth says (cite probe)
- What the docs say
- Decision: which becomes canonical, why
- Patch target: which doc(s) need editing, and what
- Live system follow-up: anything that needs Andrew to fix in n8n/SS/Slack — flagged, NOT executed

**STOP HERE. Post a structured summary in chat. Wait for Andrew's approval before Phase 3.**

The summary should be:
- Count of issues found, grouped by severity (runtime / misleading / cosmetic)
- Top 5 issues with one-line each
- List of items requiring Andrew's approval before action (live infra changes, ambiguous calls)
- Estimated patch scope for Phase 3

---

## PHASE 3 — DELIVER (only after Phase 2 approval)

### 3.0 n8n cleanup — scoped autonomy

You have authority to clean up n8n workflows that are confusing, redundant, or zombie. Andrew's CLAUDE.md gives you "full autonomy on the stack — patch, fix, ship, report after the fact." This applies here, with rails.

**GREEN — execute without asking:**
- **Deactivate** any workflow that meets ALL of: (a) inactive logic — references retired entity (Close Pipeline writes, dead channel `C0AKWU4H8C8`, the original M2 webhook replaced Apr 22, "Create Retargeting Audiences" task creation if Phase 1 confirms the SS dropdown also dropped it), (b) no execution in last 14 days, (c) no other active workflow downstream-depends on its output.
- **Remove zombie `scheduleTrigger` nodes** from already-deactivated workflows where staticData is causing phantom cron fires (per the Apr 19 incident pattern). Memory rule: setting `disabled=true` does NOT stop the scheduler — the node must be removed entirely.
- **Rename** workflows whose names are misleading vs what they actually do. Match the "[id-prefix] — [what it does] — [trigger]" pattern used by the active 21.
- **Tag/group** workflows by lifecycle stage (active, deprecated, archived) using n8n tags so the active list reads cleanly.

**YELLOW — escalate before acting:**
- **DELETE** (vs deactivate) any workflow. Deletion is irreversible. Always deactivate first, run for 7 days, then come back for delete approval.
- Touch any workflow currently writing live data, even to deactivate it.
- Modify the Sync Agent parser (`8tdPtQWO4qDKEjgq`) to match a doc decision. If parser vocabulary diverges from live SS dropdowns, the parser may or may not be the right thing to change — could be the docs that bend instead. Andrew decides.
- Anything in `AgencyOS_SS_Automation_Wave6.md` — those are business-decisioned, not orphans.
- Combine or refactor multiple workflows into one. That's architectural.
- Add new workflows. Phase 3 is cleanup, not new build.

**RED — never:**
- Edit trigger nodes on an active workflow without first deactivating it. Memory rule: zombies hide in staticData. Sequence is always: deactivate → edit → save → reactivate.
- Touch credentials.
- Change anything that would break the M3 (Calendly), M4 (No-Show Bridge), M5 (Deal Won) chains. These are committed infra.

**For every n8n action you take, log:**
- Workflow ID + name
- What you did (deactivated / removed node X / renamed / tagged)
- Why (which audit finding it resolves)
- Reversibility note (how to undo)
- Verification (did downstream workflows still run green after?)

Save log to `_handoff/patched/n8n_cleanup_log.md`. Andrew reviews this as part of Phase 3 handback.

**Do not start n8n cleanup until Phase 2 reconciliation is approved.** The doc layer and the n8n layer must move together — fixing one without the other re-creates the misalignment in the opposite direction.

### 3.1 Patch the doc layer

For each affected doc, produce:

**a. Markdown source-of-truth** in `SOPs/`:
- `SOP_01_Pipeline.md` through `SOP_09_Slack_Communication.md`
- Overwrite or upgrade existing files. Preserve structure. Patch content per reconciliation decisions.
- Each SOP must include header: app name, app ID, last updated date, who it's for, source-of-truth statement.

**b. .docx versions** in `_handoff/patched/`:
- Use `python-docx`. Preserve V2 layout (heading, TL;DR card, table structure). Patch content only.
- Files: `SOP_03_Clients_V2_PATCHED.docx`, `SOP_04_Onboarding_V2_PATCHED.docx`, `SOP_05_Campaigns_V2_PATCHED.docx`, `SOP_06_Tasks_V2_PATCHED.docx`, `SOP_09_Slack_Communication_V2_PATCHED.docx`.

### 3.2 Update master state docs

- `AgencyOS_Current_State.md` — bump to 2026-05-09. Add "Changes since Apr 20" section. Keep the structure; patch the facts.
- `AgencyOS_Architecture_AtoZ_Apr26.md` — patch any drift surfaced by audit. Bump date if changed.

### 3.3 Build the VA Plug-and-Play Operator Manual

This is the headline deliverable. **One document. Comprehensive. Self-contained.** A new VA reads this and can work.

**Path:** `_handoff/patched/RequityAI_VA_Operator_Manual.docx` AND mirror as `_handoff/patched/RequityAI_VA_Operator_Manual.md`.

**Required sections (in this order):**

1. **Welcome + the 60-second mental model.** What RequityAI does (FB ads agency for real estate investors), the 3-stage funnel, where the VA fits.
2. **The plug-and-play promise.** What the system does for the VA. What the VA does for the system. The single rule: open My Queue, work top to bottom, follow the SOP linked on each task, post structured /update messages when done.
3. **Day 1 setup checklist.** Accounts the VA needs (SmartSuite login, Slack workspace, Drive access, Meta Business Manager invitation, Ads Manager access, password manager). Owner: Andrew, but the VA confirms each.
4. **The tools.** SmartSuite, Slack, Drive, Meta Business Manager, Ads Manager, Lead destinations. One paragraph per tool: what it's for, what the VA touches, what they don't touch.
5. **Channel map.** `#all-requityai`, `#team-operations`, `#team-<client>`, `#client-<client>`. Exact rule: structured /update messages NEVER go in `#client-<client>`. Currently active client channel pairs (4).
6. **The structured /update format.** Exact skeleton. Per-app templates (Tasks, Campaigns, Onboarding, Pipeline, Optimization, Finance, Clients). Worked examples — completed task, blocked task, QA-ready campaign, completed onboarding step, blocker note. ✅ vs ⚠️ bot reactions. The 5 "must remember" rules.
7. **The 4 phases of onboarding** with the exact step list (count and labels confirmed against live SmartSuite). Per-step: what needs to happen, what the VA does, what triggers the next step. Where blockers go.
8. **The campaigns workflow.** 3-stage funnel, naming convention, build sequence (10 steps), QA checklist (9 items), publish + record-update sequence. How retargeting audiences are handled (auto-built; VA confirms existence — NOT a separate task post-May 5).
9. **The Tasks app and the daily loop.** My Queue. Priority order. Status semantics. The exact list of valid task types (matches live SmartSuite dropdown verbatim). What each task type means.
10. **The 3 agents.** Campaign Intelligence (currently dormant — activates on first live campaign), Operations Supervisor, SmartSuite Sync. What each posts, what the VA does in response.
11. **Escalation paths.** When to DM Andrew. When to post in `#team-<client>`. When to escalate from a task to Andrew via /update Blocked. Exact list of decisions that are NOT the VA's call (pricing, contracts, scope, refunds, strategic ad changes, anything risky).
12. **Common mistakes — explicit, named.** Borrowed from V2 Operator Guide; expand with anything Phase 2 surfaced.
13. **Troubleshooting matrix.** "If X is wrong, do Y." One row per failure mode the VA might encounter (broken Asset Link, missing audiences, ⚠️ reaction, Special Ad Category warning, Last Pull Date stale, ad rejected, missing client record after deal Won, etc.).
14. **Quiet hours rule.** All automated client-facing notifications fire 8am–6pm ET only. If a system message arrives outside, it's a system issue — flag.
15. **What to do on Day 1 — concrete.** "Open these tabs. Read these channels. Look at these records. Identify the first task in My Queue. Walk through it with Andrew on the kickoff call."
16. **Glossary.** Every internal term, acronym, niche, and tool name used anywhere in the manual.

**Tone:** Direct, calm, professional. Same voice as the V2 Operator Guide but tighter. Every section earns its place.

**Verification at end of manual:** include a short self-test for the VA — 8-10 yes/no statements they should be able to answer correctly after reading. Used as a comprehension check on Day 1.

### 3.4 Patch summary for Andrew

`_handoff/patched/PATCH_SUMMARY_2026-05-09.md`:

- Every doc changed, with a one-line per-issue note (M1: did X; M2: did Y; etc.)
- Every n8n action taken (cross-link to `n8n_cleanup_log.md`)
- Every issue NOT changed and why (escalation needed, ambiguous, out of scope, hit YELLOW/RED rail)
- Live system follow-ups still pending for Andrew: e.g., "Tasks dropdown still has 'Create Retargeting Audiences' — needs SS UI cleanup. Workflow `XXX` recommended for deletion after 7-day deactivation soak."
- Workflow count: before → after, with deltas explained
- Validation results (see Phase 4)
- Estimated VA-readiness % before vs after

---

## PHASE 4 — VALIDATE

Run before declaring done. Include results in 3.4.

- [ ] Tasks `type` choices in SmartSuite ≡ list in SOP_06 ≡ list in SOP_09 ≡ list in VA Manual ≡ Sync Agent parser
- [ ] Onboarding step count: live SS = SOP_04 prose = SOP_04 enumeration = SOP_09 enumeration = VA Manual
- [ ] Pipeline `deal_stage` choices: live SS = SOP_01 = SOP_09 = VA Manual
- [ ] ConvTracker `last_call_outcome` choices: live SS = SOP_02 = Sync Agent map = any doc that lists them
- [ ] No doc references `#team-tasks` (renamed Apr 22)
- [ ] No doc references "Create Retargeting Audiences" as an active task type unless live dropdown still has it (in which case there's an open escalation flagged for Andrew)
- [ ] No doc references retired Close Pipeline as a writable system (it's calling-only post-Apr 19)
- [ ] No doc proposes prospect self-booking, /book slash command, or Google Calendar
- [ ] Operator Manual has zero references to retired/dead infra (channel `C0AKWU4H8C8`, M2 webhook, zombie crons, etc.)
- [ ] VA Manual passes the read-aloud test: a friend who has never seen RequityAI can read it and articulate what the VA's first hour looks like
- [ ] Every workflow in n8n inventory is either documented in the VA Manual / an SOP, OR explicitly excluded as system-internal (not VA-facing)
- [ ] Every escalation trigger in the VA Manual matches the escalation criteria in CLAUDE.md
- [ ] n8n active workflow count post-cleanup matches the count cited in the patched `AgencyOS_Current_State.md`. Every deactivation logged in `_handoff/patched/n8n_cleanup_log.md` with reversibility notes.
- [ ] No active workflow references retired entities (dead channels, retired Close Pipeline writes, retired task types). Spot-check by grep on workflow JSON for known dead strings: `C0AKWU4H8C8`, the old M2 webhook URL, "Create Retargeting Audiences" if confirmed retired in Phase 1.
- [ ] M3, M4, M5 chains all execute green after cleanup (synthetic test or recent real execution). If you can't verify green, flag immediately — that's a RED-line breach.

---

## CONSTRAINTS — DO NOT VIOLATE

1. **No live n8n edits in Phase 1 or 2.** Audit and reconcile only. **Phase 3 has scoped n8n cleanup autonomy — see section 3.0.** Deactivation of clearly-retired workflows and removal of zombie schedule trigger nodes is GREEN. Deletion, parser edits, and touching active workflows is YELLOW (escalate). M3/M4/M5 chains are RED (never).
2. **No live SmartSuite schema edits.** If a dropdown choice needs adding/removing, FLAG IT.
3. **No live Drive uploads or `sop_link` field updates.** Patched .docx files are draft artifacts; Andrew ships them.
4. **No live Slack channel changes.**
5. **Never edit n8n trigger nodes on active workflows.** Memory rule: zombies hide in staticData. (You shouldn't be editing n8n at all in this mission, but the rule applies if escalation comes back with approval.)
6. **Probe before trust.** Memory rules: SmartSuite filter inversion silently corrupted Pipeline. SmartSuite list filter key is `fields`, not `filters`. API existence ≠ view visibility. Verify everything live.
7. **Slack architecture is sacred.** `client-X` (public, external) + `team-X` (private, internal) per client is INTENTIONAL. Do not propose collapsing.
8. **Calendly is committed infra.** Apr 20 ship + Apr 22 decision. Do not resurface Google Calendar. Do not propose a /book slash command. Andrew books prospects manually in Calendly UI.
9. **Andrew books, prospects don't.** Memory rule: tested, self-booking kills conversion.
10. **Quiet hours.** All automated notifications (SMS, email, anything) fire 8am–6pm ET only.
11. **VAs don't:** create tasks, update Onboarding step dropdowns directly, touch Finance, touch Optimization records, change Client.Status, invite externals to internal channels, post structured /update in `#client-<client>`.
12. **One recommendation, not a menu.** Per CLAUDE.md.
13. **Stop at Phase 2 boundary** for approval. Do not blow through to Phase 3 autonomously — this mission has reversibility implications (the VA Manual sets the operational tone for the agency).

---

## ESCALATION TRIGGERS — STOP AND ASK ANDREW BEFORE ACTING

Per CLAUDE.md, escalate before acting on:
- Destructive changes that could lose live data
- Cost-impacting changes
- Architectural shifts that move the system off its current foundations

Add for this mission:
- Any time Phase 1 audit reveals something materially different from what the docs claim and the resolution requires changing live infra (n8n, SS schema, Slack)
- Any time two docs contradict and the right answer isn't obvious from live state
- Any time the VA Manual would need to instruct VAs to do something not currently covered by an existing SOP (you may be inventing a workflow that hasn't been agreed)

---

## FILES YOU NEED (already in repo unless noted)

| Path | Why |
|---|---|
| `CLAUDE.md` | Operator role + escalation rules |
| `AgencyOS_Current_State.md` | Apr 20 snapshot — patch in 3.2 |
| `AgencyOS_SmartSuite_Structure_Spec.md` | Required reading before SS work |
| `AgencyOS_Architecture_AtoZ_Apr26.md` | Most current architecture |
| `AgencyOS_Handoff_Apr25.md` | Recent handoff context |
| `AgencyOS_SS_Automation_Wave6.md` | Tier 2 deferred items |
| `AgencyOS_Audit_Verdict_Apr20.md` | Prior audit (calibration only) |
| `AgencyOS_Hardening_Plan_Apr19.md` | Wave 1 hardening (calibration only) |
| `SOPs/SOP_01_Pipeline.md` … `SOP_08_Finance.md` | Existing markdown SOPs |
| `_handoff/RequityAI_Operator_Guide_V2.txt` | V2 source (extracted) |
| `_handoff/SOP_03_Clients_V2.txt` … `SOP_09_Slack_Communication_V2.txt` | V2 SOP sources (extracted) |

**Live API access required:**
- n8n Cloud API key (`signal-new-never-expires`)
- SmartSuite API token

If a credential is missing, stop and tell Andrew which one.

---

## EXECUTION ORDER

1. Pre-flight reading (all files above)
2. Phase 1 — full live audit → 5 inventory files in `_handoff/audit/`
3. Phase 2 — reconciliation → `_handoff/audit/reconciliation.md`
4. **STOP. Post structured summary. Wait for Andrew's approval.**
5. Phase 3 — patch SOPs, regenerate .docx, update Current_State, write VA Manual, write patch summary
6. Phase 4 — validation checklist, results into patch summary
7. Final handback to Andrew — paths to all deliverables, open escalations, recommended next move

Terse handback per phase. No filler. No trailing summaries. If anything contradicts what's in this brief, raise it before acting.

End of brief.
