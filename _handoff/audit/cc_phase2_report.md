# Claude Code — Phase 2 Boundary Report

**Date:** 2026-05-09
**Status:** STOP — awaiting Andrew's approval before Phase 3
**No live infra has been touched.**

---

## Phase 2 deliverables (saved by CC to repo)

- `_handoff/audit/smartsuite_inventory.md` — 12 apps, key dropdown vocabularies extracted live
- `_handoff/audit/n8n_inventory.md` — 21 active / 34 inactive, full Sync Agent parser extraction, stale-ref scan
- `_handoff/audit/reconciliation.md` — merged M1–M28 register, 9 open Q's, full live-system follow-up slate

CC merged the original M1–M20 doc reconciliation with its live-probe findings, surfacing 8 additional misalignments → final register is **M1–M28**.

---

## Severity counts

| Severity | Count | Items |
|---|---|---|
| **RUNTIME** (broken or about to break) | 3 | M1, M10, M22 |
| **MISLEADING** (VA would do wrong thing) | 14 | M3, M4, M5, M6, M7, M8, M9, M11, M12, M15, M21, M23, M25, M26 |
| **COSMETIC** | 7 | M13, M14, M17, M18, M24, M27, M28 |
| **No-op / closed** | 4 | M2, M16, M19, M20 |

---

## Top 5 issues to address first

1. **YELLOW-N1 — Slack Ops Supervisor + Onboarding Health Monitor have been silently failing for ~17 days.** Both ACTIVE, both write to the renamed `#team-tasks` channel. Daily ops health DMs to Andrew have been blocked for over two weeks. **Highest-priority runtime fix.**

2. **M22 — Tasks `type` dropdown has 6 choices sharing `value='2'`.** Either real data corruption (records can't uniquely resolve type) or a sanitization artifact in the dump CC parsed. **One-call probe resolves it; can't proceed with task-vocabulary patches until known.**

3. **M15 — Pipeline `deal_stage` has 10 stages live.** SOP_09 V2 says "11 stages with NDM" and the architecture map says "7 stages (Booked/Engaged/Qualified)" — **both fabricated**. None of those vocabulary strings exist in live SmartSuite. NDM is in ConvTracker, not Pipeline. **Single biggest factual error in the doc set.**

4. **M25 — Architecture map's active/inactive workflow split is wrong.** Says Campaign Intelligence Agent + Decision Router + Windsor AI are active; live shows them inactive. Says Campaign QA Ready Checklist is inactive; live shows active. Need Q-N1 answer to know if intentional.

5. **M23 — Clients app has duplicate status fields** (`status` "OLD" + `client_status`). Sync Agent writes only to `status`. Q8 needs picking.

---

## Decisions Andrew must make before Phase 3 ships

| # | Question | CC's recommendation |
|---|---|---|
| Q1 | M5 default channel privacy for new `#client-{slug}` | Default private; you flip public after guest invite |
| Q3 | Video editor: separate role or VA work? | Need your call — drives Operator Guide / SOP_04 / SOP_06 wording |
| Q6 | Delete or backfill `AgencyOS_Current_State.md`? | Delete; arch map already supersedes |
| Q7 | Financial Metrics Dashboard + SOPs apps — keep or scope-creep? | Keep; document briefly; exclude from VA scope |
| Q8 | Clients duplicate status — canonical = `status` or `client_status`? | Keep `status`; deprecate the other |
| Q9 | Two parallel V2 SOP sets (`_handoff/*.txt` vs `SOPs_VA_v2_May2026/*.docx`) — same or divergent? | CC will diff and report in Phase 3 prep |
| Q-N1 | Were Campaign Intelligence Agent + Decision Router + Windsor AI deactivated intentionally? | If yes: document rationale. If no: reactivate. |

---

## Phase 3 patch scope estimate (CC will execute once approved)

**Doc layer:**
- 14 docs to patch
- Master state doc to retire
- ~5 architecture map sections to rewrite
- 1 new VA Operator Manual to write (~3,000 words)
- Estimate: meaningful but tractable

**Live SmartSuite YELLOW changes (3):**
- Tasks `type` dropdown cleanup (removals/collapse)
- Clients duplicate-status decision (depends on Q8)

**Live n8n YELLOW changes (4):**
- `team-tasks` → `team-operations` patch in 2 active workflows
- CSV-Import → Build-Campaign patch in workflow `uDdwyIl7VDFEWJ8N`
- UTF-8 name fixes
- Secrets rotation per security_findings (touches all 21 active workflows)

**Live n8n GREEN changes (~23 workflows):**
- Rename + tag-as-archived for inactive supersessions and demos
- Hard delete remains YELLOW per §3.0 rails (7-day soak before delete)

---

## What Andrew owes CC before Phase 3 starts

1. **Answer Q1, Q3, Q6, Q7, Q8, Q-N1** (the actually-blocking decisions)
2. **Either** run the M22 Tasks `type='2'` probe yourself (one curl, instructions in reconciliation.md §M22) **or** approve CC to do it once you've confirmed the dropdown collision isn't a sanitization artifact
3. **Approve** the Phase 3 slate as scoped above, or push back on any item

CC is standing by. Will not start Phase 3 until greenlight.
