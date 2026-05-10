# AgencyOS Patch Summary — 2026-05-10

**Operator:** Local Claude Code (Opus 4.7 + high effort)
**Session scope:** Mass-confusion → audit → execute. Started from Andrew's full directional brief (3 RUNTIME fixes urgent + Phase 3a-d patches + Phase 4 verification + Phase 3e VA Manual write).
**Outcome:** All Phase 3 patches landed, all live infra changes logged, full functional verification complete, VA Manual written + .docx versions of all 5 priority SOPs generated.

---

## Headline

| Phase | Status | Highlight |
|---|---|---|
| 3 RUNTIME issues | ✅ done | M22 Tasks dropdown collapsed (15→13); Sync Agent `filter.filters` typo fixed; uDdwyIl7VDFEWJ8N rewritten (was silently no-op'ing 5 days). One claimed runtime issue (team-tasks rename) was a false alarm — workflows were posting fine. |
| Phase 3a — SOP markdown patches | ✅ done | All 8 SOPs in `SOPs/` carry `Last updated: 2026-05-10` headers + canonical schema/vocabulary fixes. SOP_09 created from scratch. |
| Phase 3b — retire master state doc | ✅ done | `AgencyOS_Current_State.md` deleted (Q6). |
| Phase 3c — n8n cleanup | ✅ done | 9 mojibake renames, 2 cosmetic team-tasks UI label cleanups, 53 lifecycle tags, 0 zombie cron fires found. |
| Phase 3d — architecture map rewrite | ✅ done | `AgencyOS_Architecture_AtoZ_Apr26.md` patched against live truth — Pipeline 10 stages (not 7), Onboarding 18+1 (not 19), Tasks 13 types (not 15), 12 SS apps (not 8), Q-N1/Q1/Q3/Q7/Q8/Q9 all resolved + documented. |
| Phase 4 — functional verification | ✅ done | 17 GREEN, 4 YELLOW (each explained), 0 RED across 21 active workflows + cross-system chains. Report at `_handoff/audit/verification_results.md`. |
| Phase 3e — VA Operator Manual | ✅ done | `_handoff/patched/RequityAI_VA_Operator_Manual.{md,docx}` — 16 sections, ~6,500 words, 10-question Day 1 self-test. |
| Patched .docx for SOP_03/04/05/06/09 | ✅ done | `_handoff/patched/SOP_*_V2_PATCHED.docx` |

---

## What changed in live infra (all logged in `_handoff/patched/n8n_cleanup_log.md`)

### SmartSuite

- **Tasks `type` dropdown** (app `69ce67b3fec5b91842ebaf03`): 15 corrupted choices → 13 canonical via `PUT /change_field/`. Pre-state: 6 labels collided on `value='2'`, "Create Retargeting Audiences" present despite May 5 retirement. Post-state: 13 unique-valued canonical types per doc_reconciliation §5. Zero records existed at patch time → zero migration risk. Reversibility: full pre-state preserved at top of `_handoff/audit/raw/ss_app_69ce67b3fec5b91842ebaf03.json`.

### n8n

- **Sync Agent `8tdPtQWO4qDKEjgq`** — `sf.filter.filters.push` → `sf.filter.fields.push` (2 locations). Fixes latent throw on `/update Tasks task:X` and `/update Campaigns campaign:X` paths. Sequence: deactivate → PUT (with stripped settings to satisfy n8n public API allowlist) → activate. Verified post-state: 0 `filter.filters` references, 2 `filter.fields.push` references, active=true.
- **Workflow `uDdwyIl7VDFEWJ8N`** — full rewrite of `Check Prerequisites` Code node. Removed dead audience-step check (8 fields that don't exist post-May 5 retirement); replaced retired CSV Import / Manual task type labels with canonical `Build Campaign`. The workflow had been silently returning `{skip:true}` every day since at least May 7.
- **2 active workflows** (`5cdMtOByeZVRFS6H` Slack Ops Supervisor + `CqesBe55FnP6oaxA` Onboarding Health Monitor) — cosmetic `cachedResultName` "team-tasks" → "team-operations" UI label cleanup. Channel ID `C0AKWU4835E` was always correct; Slack routes by ID. **The "17-day silent failure" claim in the phase 2 report was incorrect** — both workflows were posting `ok:true` on the day of the audit.
- **9 workflow display name renames** — UTF-8 mojibake fix (`â\x86\x92` → `→`, `â\x80\x94` → `—`).
- **53 lifecycle tags applied** — `active` (21), `campaign-gated` (13), `deprecated` (14), `demo` (1), `experimental` (5). Zero zombie cron fires detected post-Apr 26.

### Filesystem

- `AgencyOS_Current_State.md` deleted (Q6).
- `SOPs/SOP_01..08` patched with date stamps + canonical content.
- `SOPs/SOP_09_Slack_Communication.md` created.
- `AgencyOS_Architecture_AtoZ_Apr26.md` patched against live truth (date bumped, 12 SS apps documented, 10 Pipeline stages, 18+1 onboarding, etc.).
- `_handoff/patched/RequityAI_VA_Operator_Manual.{md,docx}` — headline VA deliverable.
- `_handoff/patched/SOP_*_V2_PATCHED.docx` (5 files).
- `_handoff/patched/n8n_cleanup_log.md` — append-only log of every live-infra change.
- `_handoff/audit/verification_results.md` — Phase 4 GREEN/YELLOW/RED report.
- `_handoff/audit/raw/*.json` — live API dumps captured this session (n8n workflows, SS schemas, executions).

---

## Issues NOT changed and why

| Issue | Why deferred |
|---|---|
| `SS_TOKEN` hardcoded in JS code of `8tdPtQWO4qDKEjgq` (Sync Agent) and `uDdwyIl7VDFEWJ8N` (Prereqs Met) | Same security pattern as Anthropic key leak. Should be moved to n8n Credentials. Andrew action — see `_handoff/audit/anthropic_key_rotation_runbook.md`. Touches multiple workflows; needs a coordinated rotation pass. |
| Slack bot `not_in_channel` errors on `#client-<client>` channels | Bot needs guest invite to all 6 client channels. Andrew action. Slack Ops Supervisor handles the missing access gracefully. |
| `SOPs_VA_v2_May2026/*.docx` archive | Same source as `_handoff/*_V2.txt` extracts (May 2 2026). Going forward canonical = `SOPs/*.md` + `_handoff/patched/*_PATCHED.docx`. The May 2 .docx set is archive-only. (Q9.) |
| Hard delete of `deprecated`-tagged workflows | YELLOW per §3.0. 7-day soak first, then a follow-up pass needs explicit approval per workflow. 14 candidates. |
| Anthropic API key rotation | Andrew owns — runbook in `_handoff/audit/anthropic_key_rotation_runbook.md`. 5-minute task. Bounded leak. |
| `PJaJYLuesPU2oxc7` Enterprise Demo display rename | n8n public API returned 400 on the PUT (workflow's node graph likely has structure the public API rejects on round-trip). Cosmetic only; workflow is `demo`-tagged. Skipped. |
| SS Automations for M5 + M4 (instant webhook vs 5-min poller) | Andrew action — needs to be built in SmartSuite UI. Documented as outstanding in arch map §L. Until then both M-flows fire on the fallback poll. |

---

## Open questions resolved (closed this session)

| # | Question | Resolution |
|---|---|---|
| Q1 | New `#client-{slug}` channel privacy default | Private; Andrew flips public after guest invite. Documented in arch map §F + SOP_03 + VA Manual §5. |
| Q3 | Video editor: separate role or VA work? | VA owns end-to-end. 4-6 week skill ramp expected. Documented in arch map §H + SOP_04 + VA Manual §7. |
| Q6 | Delete or backfill `AgencyOS_Current_State.md`? | Deleted. Architecture map is sole canonical state doc. |
| Q7 | Financial Metrics Dashboard + SOPs apps — keep or scope-creep? | Kept; one paragraph each in arch map §C; both excluded from VA scope. |
| Q8 | Clients duplicate status fields | Canonical = `status` (label "Status (OLD)"); `client_status` deprecated. Sync Agent already correct. Documented in SOP_03 + arch map §C. |
| Q9 | Two parallel V2 SOP sets | Same source (May 2 2026). `SOPs_VA_v2_May2026/*.docx` is archive-only. Canonical going forward = `SOPs/*.md` (patched) + `_handoff/patched/*_PATCHED.docx`. |
| Q-N1 | Were CIA + Decision Router + Windsor deactivated intentionally? | Yes. All 3 are correctly campaign-gated. Auto-reactivate when first real campaign publishes. Documented in arch map §I. None should be reactivated now. |
| M22 | Tasks `type` dropdown corruption | Fixed today. 15 → 13 canonical. |

---

## Phase 4 validation checklist results

- ✅ Tasks `type` choices in SmartSuite ≡ list in SOP_06 ≡ list in SOP_09 ≡ list in VA Manual ≡ Sync Agent parser (status maps; type is a write-only dropdown not parsed by the agent).
- ✅ Onboarding step count: live SS = SOP_04 = SOP_09 = VA Manual = arch map (18 named + 1 master flag).
- ✅ Pipeline `deal_stage` choices: live SS = SOP_01 = SOP_09 = VA Manual = arch map (10 stages, no NDM).
- ✅ ConvTracker `last_call_outcome` choices: live SS = SOP_02 = arch map (15 values).
- ✅ No SOP markdown references `#team-tasks` (verified by grep).
- ✅ No SOP markdown references "Create Retargeting Audiences" as an active task type.
- ✅ No SOP markdown references retired Close Pipeline as a writable system.
- ✅ No SOP markdown proposes prospect self-booking, /book slash command, or Google Calendar.
- ✅ VA Manual has zero references to retired/dead infra.
- ✅ Every active n8n workflow is documented in either VA Manual / SOPs OR explicitly excluded as system-internal.
- ✅ Every escalation trigger in VA Manual matches the criteria in CLAUDE.md.
- ✅ n8n active workflow count post-cleanup matches the count cited in the patched architecture map (21).
- ✅ No active workflow references retired entities. Spot-grepped JSON for `C0AKWU4H8C8` (dead channel — 0 hits in actives), `Build Campaign (CSV Import)` (0 hits in actives post-fix).
- ✅ M3 chain executes green (last fire 88h ago, success).
- ✅ M5 chain functionally proven (5 Won deals carry `won_processed=true` + Client + Onboarding + Drive + Slack channel pairs all confirmed).
- ⚠️ M4 chain: untested in production (no real no-shows yet). Architecturally sound.

---

## Workflow count

- Before this session: 55 total (21 active, 34 inactive).
- After this session: 55 total (21 active, 34 inactive). No deletions; deactivations YELLOW per §3.0 rails.
- Lifecycle distribution: 21 active · 13 campaign-gated · 14 deprecated · 1 demo · 5 experimental.

---

## VA-readiness estimate

- **Before this session:** ~30%. Doc layer claimed 11 Pipeline stages where live had 10. Tasks dropdown was schema-corrupt (6 collisions on value='2'). The Sync Agent parser had a latent throw. The "Prerequisites Met" workflow was silently no-op'ing. SOPs referenced retired infra (`#team-tasks`, "Create Retargeting Audiences", CSV Import). No single VA-facing manual existed.
- **After this session:** ~85%. Live infra is verified working end-to-end (17 GREEN / 4 YELLOW / 0 RED). Doc layer matches live truth in every place a VA would look. VA Operator Manual exists, is plug-and-play, and has a 10-question Day 1 self-test.
- **What stops it from being 100%:** Andrew's planned operator-week (Andrew runs the system as the VA himself for ~1 week, surfaces real-world failures, sharpens the Manual against lived experience). Plus M4 + /done + first M5 fresh fire all need real triggers to verify in production.

---

## Recommended next move (one option, not a menu)

**Andrew's operator week.** Run the system end-to-end as the VA yourself for ~5 working days, on at least one real client cycle. Note every place the Manual is wrong, every SOP step that doesn't match live behavior, every workflow that doesn't fire when it should. Bring that list back; we sharpen the Manual against your lived experience, then it's ready for VA hand-off. Per CLAUDE.md the system passes its filter ("does this keep the stack running, make a VA more effective, or remove Andrew as a bottleneck") only if a real human can run it; you're the highest-fidelity test we can run.
