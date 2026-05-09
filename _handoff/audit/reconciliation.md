# Phase 2 Reconciliation — Doc Layer vs Live Truth (2026-05-09)

**Author:** Cowork
**Sources:** Live SmartSuite + n8n raw dumps in `_handoff/audit/raw/`. Doc-layer audit `_handoff/audit/doc_reconciliation.md` (390 lines, M1–M20). New finding inventories: `smartsuite_inventory.md`, `n8n_inventory.md`, `slack_inventory.md`, `drive_inventory.md`.

**Purpose:** Single canonical decision register for the Phase 3 patching pass. Per CLAUDE.md and the brief, Phase 2 STOPS HERE. No edits to live infra. No SOP rewrites. Andrew approves the slate, then Phase 3 ships.

---

## How to read this doc

Each issue has:
- **Status** — RESOLVED-LIVE (live truth provides the answer), DECISION-NEEDED (Andrew must call), or PROBE-PENDING (record-level data needed).
- **Severity** — RUNTIME (system is broken or about to break), MISLEADING (a VA would do the wrong thing), COSMETIC (drift only).
- **Decision** — what becomes canonical.
- **Patch target** — which doc(s) and which line(s).
- **Live system follow-up** — anything Andrew must execute outside the doc layer (SS schema cleanup, n8n workflow patch, Slack channel work). Flagged, not executed.

---

## Doc-set scope

The doc_reconciliation pass covered 14 docs. This Phase 2 pass extends the same lens to the additional inputs surfaced in pre-flight reading:

- `AgencyOS_Architecture.html` (companion to .docx)
- `AgencyOS_Automation_Chain_Map.md`
- `AgencyOS_Build_Status_April13_2026.md` ← stale, pre-Apr-22 events
- `AgencyOS_Fix_Thread_Prompt.md`
- `AgencyOS_Full_Automation_Stack.md`
- `AgencyOS_Master_SOP_v2.docx`
- `AgencyOS_Optimization_SOP.md`
- `AgencyOS_SmartSuite_Audit_April17.md`
- `Close_Dropdown_Handoff_Apr19.md`
- `RequityAI_Operator_Guide.docx` (Apr V1, predecessor to V2)
- `RequityAI_SmartSuite_Operating_Guide_v2.docx` and the VA variant
- `SmartSuite_Keep_Kill_List.md`
- `SS_Automation_M4_M5_Build.md`
- `SOPs_VA_v2_May2026/SOP_*.{docx,pdf}` (the latest VA-facing draft set)
- `_handoff/CC_Prompt_SOP_Alignment_May09.md` (this brief)

Net effect: M1–M20 carry over; new misalignments **M21–M28** added. Open questions extended from 6 to 9 (Q1–Q9). Stale-infra refs go S1–S10.

---

## RESOLUTIONS — issues now closed against live truth

### M11 — Onboarding step count: **18 named steps + 1 master flag = 19 step_* fields**

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

**Live truth:** Onboarding app `69db909cd9114601cccb2b57` has exactly 19 `step_*` `singleselectfield`s, all 3-state (1=Not Started, 2=In Progress, 3=Complete). Phases: Access (5) + Lead Setup (5) + Videos (4 — including `step_videos_edited` and `step_approved_videos_exist`) + Campaign Launch (4) + Master flag `step_onboarding_complete`.

**Sync Agent parser** (`OB_STEP_MAP`) lists exactly these 19 — parser ↔ live SS in lockstep.

**Canonical phrasing for docs:** "18 onboarding steps in 4 phases (5 + 5 + 4 + 4), plus the master `Onboarding Complete` flag (19 step_* dropdowns total)."

**Patch targets:**
- `SOP_04_Onboarding_V2.txt` lines 8, 28, 52 — change "19-step" to "18-step (plus master flag)"
- `SOP_04_Onboarding.md` lines 86, 112 — same
- `SOP_09_Slack_Communication_V2.txt` lines 68–73 — add `step_videos_edited` to Videos phase; add the 4th Phase-4 step that's currently missing
- `AgencyOS_Architecture_AtoZ_Apr26.md` line 58 + section E lines 151–179 — current text says "19 STEPS" but enumerates 18; align to "18 + master = 19 dropdowns"

**Live-system follow-up:** The two slug-vs-label drifts in SS UI (`step_approved_videos_exist` labeled "Ad Creative Ready"; `step_launch_notification_sent` labeled "Client Notified") aren't bugs, but if cleaning, rename labels to match slugs OR rename slugs (slug changes break automations — DON'T). Recommend: leave slugs, document the label/slug pair in the VA Manual.

---

### M15 — Pipeline `deal_stage`: **10 stages, no NDM, no "Engaged/Qualified" vocab**

**Status:** RESOLVED-LIVE. Severity: MISLEADING (high).

**Live truth:** 10 stages: Conversation - Positive / Follow Up - Reschedule / Booked / No Show / Cancelled / Proposal - Decision - Pending / Ghosted / Signed - Invoice Sent / Won / Lost.

**Confirms:**
- `SOPs/SOP_01_Pipeline.md` (10 stages exact match) ✅
- `AgencyOS_SmartSuite_Structure_Spec.md` ✅
- Sync Agent parser `STATUS_MAPS.pipeline` ✅

**Refutes:**
- `SOP_09_Slack_Communication_V2.txt:75` — fabricated 11-stage list ("Lead, Contacted, Discovery Call, NDM, Proposal Sent, Negotiation, Verbal Commit, Onboarding, Active Client, Churned, Lost"). **None of those strings exist in live SS.** This list looks copy-pasted from a generic CRM template.
- `AgencyOS_Architecture_AtoZ_Apr26.md` lines 55, 114 — "7 stages (Booked → Engaged → Qualified → Proposal → Won/Lost/No Show)". Also fabricated.
- Memory note `project_m2_replaced_by_polling_apr22` — "NDM choice added (11 total)" was wrong. NDM was added to **ConvTracker `last_call_outcome`** (verified live), not to Pipeline.

**Canonical:** Use the 10-stage live list verbatim everywhere, including SOP_09 V2, the architecture map, and the VA Manual's Pipeline section.

**Patch targets:**
- `SOP_09_Slack_Communication_V2.txt:75` — replace 11-stage fabrication with 10-stage live list
- `AgencyOS_Architecture_AtoZ_Apr26.md` lines 55, 114 — replace 7-stage fabrication with 10-stage live list
- `AgencyOS_Current_State.md` — pipeline section
- (No memory note edits in scope here; flag for parent.)

**Live-system follow-up:** None. SS dropdown is correct.

---

### M4 / Q5 — ConvTracker `last_call_outcome`: **15 values, NDM lives here**

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

**Live truth:** 15 values exactly: Owner-Booked / Owner-Talked / Owner-Maybe / Owner-Callback Requested / Owner-Not Interested / Non-Decision Maker (NDM) Interested / Gatekeeper / Voicemail / No Answer / Wrong Number / Do Not Call / Hung Up - Owner / Left Voicemail / Voice Agent / Invalid.

**Patch targets:**
- `SOPs/SOP_02_Conversation_Tracker.md` after line 51 — add new section enumerating the 15 `last_call_outcome` values, populated by M2b polling, VAs do not edit.
- `AgencyOS_Architecture_AtoZ_Apr26.md` — confirm wording in section E doesn't conflict.

Adjacent finding: separate `outcome` field has 6 values (Interested / Maybe / Not Interested / No Contact / Gatekeeper / LVM). The "LVM" choice has SS-generated value `bjQuK` instead of the literal — cosmetic SS housekeeping item if Andrew wants to clean. **Phase 2 #P3.**

---

### M1 / M3 / M10 / vocab — Tasks `type` field: **15 entries, but ⚠️ data integrity flag**

**Status:** RESOLVED-LIVE plus open data-integrity question. Severity: RUNTIME (potential).

**Live truth:** 15 dropdown choices in Tasks `type` field:
1. Set Up Ad Account Access (value=`'2'`)
2. Set Up Lead Forms (value=`'2'`) ⚠ collision
3. Request Videos (value=`'2'`) ⚠ collision
4. Upload Creative (value=`'2'`) ⚠ collision
5. Write Script (value=`'2'`) ⚠ collision
6. Admin (value=`'2'`) ⚠ collision
7. Build Campaign (CSV Import) (value=`'iQMVn'`)
8. Build Campaign (Manual) (value=`'n6EvX'`)
9. QA Campaign (value=`'WvoJS'`)
10. Launch Campaign (value=`'3LeIB'`)
11. Campaign Review (value=`'pjZqe'`)
12. Cut / Pause Campaign (value=`'Kr9Qn'`)
13. Create Retargeting Audiences (value=`'LaFdW'`) ⚠ retired May 5
14. Update SmartSuite Records (value=`'gPtcw'`)
15. Escalation Follow-Up (value=`'M2IdT'`)

**Six choices share `value='2'`**. Either (a) data corruption — records storing `type='2'` cannot uniquely resolve which label (this is a SHOW-STOPPER if so), or (b) sanitization quirk in the dump-time scanner that overzealously rewrote stable choice IDs. Phase 2 cannot tell which without a record-level probe. **#P1 below.**

**Sync Agent parser handles `type` field:** It does NOT. The parser writes `tasks.status` and `description`, never `type`. SOP_06 V2 and SOP_09 V2 both reference "the parser's hardcoded valid task-type list" — that list does not exist in the parser code. Doc-layer fabrication.

**SOP_09 V2's task list is fabricated:**
- Build Video Views Campaign / Build Retarget Campaign / Build Lead Ad Campaign — **none in live SS**
- Process Raw Video / Configure Lead Notifications / Send Video Brief / Organic Page Post / Optimization Review / General Task / CSV Import Build / Upload Ad Creatives — **none in live SS** (live has "Upload Creative" not "Upload Ad Creatives")

**Canonical task-type list** (per Andrew's M3+M10 decisions, applied to live):

After retiring "Create Retargeting Audiences" (M3) and collapsing "Build Campaign (CSV Import)" + "Build Campaign (Manual)" → "Build Campaign" (M10):

| # | Canonical | Source |
|---|---|---|
| 1 | Set Up Ad Account Access | live |
| 2 | Set Up Lead Forms | live |
| 3 | Request Videos | live |
| 4 | Upload Creative | live |
| 5 | Write Script | live |
| 6 | Build Campaign | collapsed from CSV Import + Manual |
| 7 | QA Campaign | live |
| 8 | Launch Campaign | live |
| 9 | Campaign Review | live |
| 10 | Cut / Pause Campaign | live |
| 11 | Update SmartSuite Records | live |
| 12 | Escalation Follow-Up | live |
| 13 | Admin | live (kept as catch-all bucket — alternative is Update SmartSuite Records / Escalation Follow-Up) |

**13 types** if Admin is kept as a bucket. **Drop to 12** if Andrew wants Admin folded — see Q9 below.

doc_reconciliation §5 proposed adding "Swap Creative" and "Adjust Targeting" task types based on Decision Router output (architecture map lines 240–244). Live SS does NOT have these as task types, AND the Decision Router workflow is INACTIVE. Recommend: do NOT add to canonical list now. If/when Decision Router reactivates, add then. Otherwise the docs claim a vocabulary the system can't write.

**Patch targets:**
- `SOPs/SOP_06_Tasks.md` — replace 15-types table with canonical 13 (or 12 if Admin folded).
- `SOP_06_Tasks_V2.txt` — same.
- `SOP_09_Slack_Communication_V2.txt:64` — replace fabricated 15 with canonical 13.

**Live-system follow-up — YELLOW (escalation needed):**
- **YELLOW-T1:** Resolve P1 data-integrity question. If real, escalate immediately.
- **YELLOW-T2:** Remove "Create Retargeting Audiences" from SS Tasks `type` dropdown (no automation creates it; safe to remove). YELLOW per Phase 3 §3.0 (live SS schema edit).
- **YELLOW-T3:** Collapse "Build Campaign (CSV Import)" + "Build Campaign (Manual)" → single "Build Campaign". Requires updating active workflow `uDdwyIl7VDFEWJ8N` Prerequisites Met to write the new value (currently writes "Build Campaign (CSV Import)" — 6 matches). Sequence: deactivate workflow → patch JS → save → reactivate → SS dropdown change → verify next run produces the new label.

---

### M21 (NEW) — Optimization `decision` field: **5 values, architecture map fabricated 3 of them**

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

**Live truth:** 5 choices: Keep Running / Cut / **Retarget Test** / **Lead Ad Candidate** / Swap Creative.

**Architecture map** lines 233, 240–244, 423–428 say: Cut / Keep Running / Retarget / Swap Creative / **Needs Review**. Three mismatches:
- "Retarget" vs "Retarget Test"
- "Lead Ad Candidate" missing entirely
- "Needs Review" doesn't exist

**Sync Agent parser** matches live exactly (Keep Running / Cut / Retarget Test / Lead Ad Candidate / Swap Creative).

**Patch targets:**
- `AgencyOS_Architecture_AtoZ_Apr26.md` — section J (lines 401–435) and section E (lines 233, 240–244). Replace fabricated decision list with live 5.
- `SOPs/SOP_07_Optimization.md` — verify against live; patch if needed.

**Live-system follow-up:** None — Decision Router workflow is INACTIVE anyway. When/if it's reactivated, the doc claims a "Needs Review" branch that the SS dropdown won't accept; the patched docs will protect against this.

---

### M1 — `#team-tasks` rename to `#team-operations`

**Status:** RESOLVED-LIVE. Severity: **RUNTIME** (active workflows broken).

**Live truth:** Channel was renamed Apr 22; ID `C0AKWU4835E` unchanged. Confirmed in slack_inventory.md.

**doc_reconciliation §M1** found `#team-tasks` in 4 markdown SOPs + master state doc. Phase 2 extends the search:

**Active n8n workflows still reference `#team-tasks`:**
- `5cdMtOByeZVRFS6H` Slack Ops Supervisor — 8 matches in node parameters. Posts daily ops health to a channel that no longer exists under that name. Slack API will return `channel_not_found` → Global Error Handler → DM Andrew. Effectively the daily ops health post has been silently failing since Apr 22.
- `CqesBe55FnP6oaxA` Onboarding Health Monitor — 2 matches. Same problem.

**Inactive workflows (lower priority):**
- `HZ18Xb98Szin8OTQ` Deal Won (Manual) — 2 matches
- `PpfpYaSQRcGrJqLe` Weekly Skeleton Tasks — 2 matches

**Patch targets — docs:**
- 4 markdown SOPs (per doc_reconciliation §M1)
- `AgencyOS_Current_State.md` lines 14, 84, 87

**Patch targets — runtime (YELLOW, n8n cleanup §3.0):**
- **YELLOW-N1:** Patch active workflows `5cdMtOByeZVRFS6H` and `CqesBe55FnP6oaxA` — replace `#team-tasks` with `#team-operations` in all node parameters. Sequence: deactivate → edit → save → reactivate → verify next scheduled run posts successfully.

This is the highest-priority runtime fix surfaced by the audit. Two pieces of automation that exist to alert Andrew on issues have been silently failing for ~17 days.

---

### M2 — Dead channel `C0AKWU4H8C8`

**Status:** RESOLVED-LIVE. Severity: COSMETIC.

**Live truth:** No references in any of 55 n8n workflows or 14 docs. Already clean. **No-op.**

---

### M3 — "Create Retargeting Audiences" task

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

**Live truth:**
- Still in SS Tasks `type` dropdown (value `LaFdW`).
- Zero references in any of 55 n8n workflows. No automation creates it.
- 7 doc references per doc_reconciliation §M3.

**Decision:** Retire per Andrew May 5. Remove from docs (already-decided patches in §M3). YELLOW for SS dropdown removal (YELLOW-T2 above).

**Patch targets:** Per doc_reconciliation §M3 — already enumerated.

---

### M5 — Operator Guide implies prospects self-book

**Status:** DOC-ONLY (no live signal needed). Severity: MISLEADING.

**Decision and patch targets:** Per doc_reconciliation §M5 — apply as-is.

---

### M6 — Campaign Intelligence Agent presented as actively running

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

**Live truth:** Campaign Intelligence Agent `6TuDo3mqBZSBF667` is **INACTIVE** in live n8n. SOP_09 V2 line 139 says correctly "currently dormant". Operator Guide V2 lines 71–73 imply active. Architecture map §I says active — also wrong.

**Patch targets:**
- `Operator_Guide_V2:73` — append "currently dormant" qualifier per doc_reconciliation §M6
- `AgencyOS_Architecture_AtoZ_Apr26.md` line 379 — move from active to inactive list

---

### M7 — Active client count: 6, not 4

**Status:** RESOLVED-LIVE (Slack-side). Severity: MISLEADING.

Per slack_inventory.md — 6 active client channel pairs. Per doc_reconciliation §M7 — patch state doc and SOP_09 V2 client list.

**SmartSuite-side verification PROBE-PENDING** — record-list dump of Clients app needed to confirm 6 active records. Architecture map §K line 441 already states 6.

---

### M8 — n8n workflow count: 21 active, NOT 24

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

**Live truth:** 21 active, 34 inactive (= 55 total).

**Patch targets:** Per doc_reconciliation §M8 — replace state doc workflow list with pointer to architecture map. Architecture map itself needs updating (see N1 below) to reflect that Campaign Intelligence Agent + Decision Router + Windsor AI are now inactive (the doc says they're active).

---

### M9 — V1 SOPs predate Calendly + M-series

**Status:** DOC-ONLY. Severity: MISLEADING.

**Decision and patch targets:** Per doc_reconciliation §M9 — apply as-is.

---

### M10 — CSV Import as primary build method

**Status:** RESOLVED-LIVE. Severity: RUNTIME (workflow misalignment).

**Live truth:** Both "Build Campaign (CSV Import)" and "Build Campaign (Manual)" are in SS Tasks `type` dropdown. Active workflow `uDdwyIl7VDFEWJ8N` Prerequisites Met still creates "Build Campaign (CSV Import)" tasks (6 matches in JSON). State doc line 144 still says CSV Import is primary.

**Decision:** Per Andrew, collapse to single "Build Campaign" + manual is the only build method.

**Patch targets — docs:** Per doc_reconciliation §M10.

**Live-system follow-up — YELLOW-T3 above.** Workflow + SS dropdown must move in lockstep with the docs.

---

### M12 — New client channels are PRIVATE; existing 4 are PUBLIC

**Status:** RESOLVED-OBSERVED, DECISION-NEEDED on policy. Severity: MISLEADING.

Per slack_inventory.md — 4 original `#client-{slug}` are public, 2 newer (Next Journey + Bayrock, Apr 25) are private.

**Decision needed (Q1):** Should M5 default new `#client-` to public or private? Or keep as Andrew-decides-per-client?

---

### M13, M14, M16, M17, M18, M19 — Per doc_reconciliation, no new live findings

These remain as the existing audit document describes. M19 was a no-op. Apply doc_reconciliation patches as written.

---

### M20 — Old `signal` n8n API key expiry

**Status:** RESOLVED. Severity: COSMETIC.

Per `_handoff/audit/security_findings.md:35-41`, the previous JWT (expired 2026-04-29) is dead; the new `signal-new-never-expires` is current. No action.

---

## NEW MISALIGNMENTS — surfaced this pass

### M22 — Tasks `type` dropdown value collision

**Status:** PROBE-PENDING. Severity: **POTENTIAL RUNTIME** (data integrity).

**Issue:** Six choices in Tasks `type` share `value='2'`. See M1/M3/M10 section above. Andrew probes a sample Task record to confirm whether (a) actual data corruption or (b) sanitization artifact.

**Probe instructions for Andrew (or me, once allowlist permits):**
```bash
# Pull 10 sample Task records and inspect the type field value
curl -X POST "https://app.smartsuite.com/api/v1/applications/69ce67b3fec5b91842ebaf03/records/list/" \
  -H "Authorization: Token $SMARTSUITE_API_TOKEN" \
  -H "ACCOUNT-ID: sl181chl" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "fields": ["title", "type"]}'
```

If multiple records have `type: "2"` and the labels resolved by SS are all the same, it's a sanitization artifact. If labels are different across records all storing `"2"`, it's data corruption — the schema dump's choice list is correct, the records are ambiguous, and SS is silently picking the first-defined label.

---

### M23 — Clients app has duplicate status fields

**Status:** RESOLVED-LIVE on existence; DECISION-NEEDED on canonical. Severity: MISLEADING (high — silent data divergence risk).

**Live truth:** Clients has both `status` (singleselectfield, label "Status (OLD)") AND `client_status` (statusfield, label "Client Status"). Sync Agent parser writes only to `status`. M5 likely also writes to `status`.

**Decision needed (Q8):** Pick one as canonical; deprecate the other. Without this, any UI/automation that reads `client_status` will diverge from records updated by Sync Agent or M5.

---

### M24 — `step_approved_videos_exist` slug-vs-label drift

**Status:** RESOLVED-LIVE. Severity: COSMETIC.

UI labels "Ad Creative Ready", slug is `step_approved_videos_exist`. Same for `step_launch_notification_sent` (UI: "Client Notified"). Docs should pick one canonical name and stick to it. Recommend: use slug-derived name everywhere (avoids ambiguity if Andrew renames UI labels later).

**Patch:** All onboarding step references in SOPs.

---

### M25 — Architecture map's active/inactive workflow split is stale

**Status:** RESOLVED-LIVE. Severity: MISLEADING.

Per n8n_inventory.md: arch map says Campaign Intelligence Agent + Decision Router + Windsor AI Metrics are active; live shows inactive. Arch map says Campaign QA Ready Checklist is inactive; live shows active.

**Decision needed (Q-N1):** Did Andrew deactivate Campaign Intelligence Agent + Decision Router intentionally (e.g., to preserve costs until first campaign launches)? If yes, document the rationale in the architecture map.

**Patch:** Architecture map §I needs full alignment with live.

---

### M26 — VA-facing SOPs in `SOPs_VA_v2_May2026/` (8 docx + pdf, dated May 2026) duplicate the V2 set in `_handoff/`

**Status:** DOC-ONLY. Severity: MISLEADING.

There are TWO parallel V2 SOP sets: `_handoff/*.txt` and `SOPs_VA_v2_May2026/*.{docx,pdf}`. Probably the same content in two formats, but a VA opening the repo will not know which is canonical.

**Decision needed (Q9 → renamed Q-D1):** Are these the same source or do they diverge? If same, delete one (recommend keep the .docx in `SOPs_VA_v2_May2026/` and treat `_handoff/*.txt` as derived/working copy). If they diverge, reconcile.

---

### M27 — Workflow names in n8n contain UTF-8 corruption (`â` instead of `→`)

**Status:** RESOLVED-LIVE. Severity: COSMETIC.

`NFU4jyVpaRSKv4Mj` Onboarding Progression and `uDdwyIl7VDFEWJ8N` Prerequisites Met both have `â` in their names where `→` should be. Other workflows render `→` correctly. Either an early double-encoding or a copy-paste from a tool that mangled the arrow.

**Patch (YELLOW-N2):** Rename in n8n UI. Low risk — name change doesn't touch logic.

---

### M28 — Daily Sales Brief workflow name drift

**Status:** RESOLVED-LIVE. Severity: COSMETIC.

Architecture map §I line 368 names `pa7I1FKd50TQRFrV` "Daily Sales Brief". Live name: "Daily Sales Metrics Brief". Pick one and align.

**Patch:** Architecture map.

---

## OPEN QUESTIONS — Andrew decides BEFORE Phase 3

(Q1–Q6 carried forward from doc_reconciliation; Q7–Q9 new.)

### Q1 — `#client-` channel privacy default

Original 4 are public; the 2 newest (Apr 25) are private. Should M5 default new `#client-` to public, private, or remain as-is (whatever Andrew sets manually)? Recommendation: default private; Andrew flips to public once the client guest invite is in.

### Q2 — SOP_07 SmartSuite UI rename of "Launch Date" → "Review Date"

Per doc_reconciliation §Q2. Now live-verified: Optimization app field `review_date` already labeled "Review Date" (no UI rename pending). The SOP_07 callout about a mislabel can be DROPPED. **This is now actionable — close the SOP comment, no UI work needed.**

### Q3 — Video editor role

Per doc_reconciliation §Q3. No new live signal. Andrew picks: VA does video editing OR there's a separate role. Once decided, language unifies across Operator Guide / SOP_04 / SOP_06 / architecture map.

### Q4 — Pipeline canonical list

**RESOLVED.** See M15 above. 10 stages. No more decision needed.

### Q5 — `last_call_outcome` 15-value list

**RESOLVED.** See M4 above. 15 values enumerated.

### Q6 — Master state doc — replace or backfill

Per doc_reconciliation §Q6. Recommendation: delete `AgencyOS_Current_State.md` entirely. Architecture map already supersedes per its own §line 481. The state doc is too stale to backfill cleanly (24 vs 21 workflows, 4 vs 6 clients, broken channel name, stale build method, missing M-series). Andrew confirms.

### Q7 (NEW) — Financial Metrics Dashboard + SOPs apps

Two custom SS apps not referenced anywhere. Are they intentional dormant analytics/registry apps (keep + document briefly), or scope-creep to clean up? Recommendation: keep. Both have plausible long-term roles. Document each in 1 paragraph in the architecture map; exclude from VA scope.

### Q8 (NEW) — Clients duplicate status fields

`status` (OLD) vs `client_status` (newer). Pick canonical. Recommendation: keep `status`. Sync Agent and likely M5 already write to it. Deprecate `client_status` — hide the field in SS UI; remove from any view. Out-of-scope to do now (YELLOW-S1) but flag.

### Q9 (NEW) — Two parallel V2 SOP sets

`_handoff/*V2*.txt` and `SOPs_VA_v2_May2026/*.{docx,pdf}` — same source or different? Recommendation: I'll diff in Phase 3 prep and decide; if identical, kill the .txt set; if different, reconcile to one canonical.

### Q-N1 (NEW) — Were Campaign Intelligence Agent + Decision Router + Windsor AI deactivated intentionally?

Architecture map says active. Live says inactive. If intentional (cost preservation until first campaign), document in arch map; if not (zombie deactivation), reactivate. Andrew confirms.

### Q-D1 (NEW) — Same as Q9 — reconcile parallel SOP sets.

---

## LIVE-SYSTEM FOLLOW-UP REGISTER (flagged, not executed)

These are the items Phase 3 §3.0 governs. Recapped here so Andrew sees the slate before approving.

### YELLOW (escalate before acting)

| ID | Action | Why YELLOW |
|---|---|---|
| YELLOW-N1 | Patch active workflows `5cdMtOByeZVRFS6H` Slack Ops Supervisor + `CqesBe55FnP6oaxA` Onboarding Health Monitor — replace `#team-tasks` → `#team-operations` | Touches active workflow writing live data |
| YELLOW-T1 | Resolve M22 — record-level probe to confirm Tasks `type='2'` collision is artifact vs corruption | Could reveal data corruption blocking Phase 3 |
| YELLOW-T2 | Remove "Create Retargeting Audiences" from SS Tasks `type` dropdown | Live SS schema edit |
| YELLOW-T3 | Collapse "Build Campaign (CSV Import)" + "Build Campaign (Manual)" → "Build Campaign" in SS Tasks dropdown AND patch active workflow `uDdwyIl7VDFEWJ8N` to write the new value | Live SS + active workflow, lockstep |
| YELLOW-S1 | Resolve M23 — Clients duplicate status fields. Hide one, document the other as canonical | Live SS schema (hide is reversible) |
| YELLOW-N2 | Rename workflows with `â` UTF-8 corruption in n8n UI | Cosmetic but touches active workflow metadata |
| YELLOW-N3 | Reconcile architecture map's active/inactive split with live (M25). Per Q-N1 — confirm intent on Campaign Intelligence Agent / Decision Router / Windsor AI / Campaign QA Ready Checklist | Could uncover unintended deactivations |
| YELLOW-N4 | Migrate hardcoded secrets in all 21 active workflows to n8n Credentials per security_findings.md | Touches every active workflow; sequence and verification per security note |

### GREEN (Phase 3 cleanup autonomy per §3.0)

Pre-approved scope: deactivate clearly-retired workflows that meet (a) inactive logic, (b) no execution in 14d, (c) no downstream dependency. Candidates from inactive list:

| ID | Workflow | Why retire |
|---|---|---|
| `dInuMwYxjwcftjSp` | M2 — Close CRM Webhook (push) | Replaced by M2b polling Apr 22 |
| `Ikil2vx4jQNR7yxa` | M4 — SS No-Show (predecessor) | Same name as active M4, pre-shipped version |
| `Gly17Kkp8oUTEyGp` | Close CRM → SmartSuite ConvTracker | Superseded by M2b |
| `R4mXec6XM032MMyB` | Close CRM → SmartSuite Pipeline Sync | Close-as-source pattern retired Apr 19 |
| `HZ18Xb98Szin8OTQ` | Deal Won → Create Client + Onboarding (Manual) | Superseded by M5 |
| `9pAsoQqBhRT4HHS6` | Client Onboarding — Create Slack Channels | Superseded by M5 |
| `W2GRDMN8xwlQhlqg` | Client Onboarding — Slack Trigger | Superseded by M5 |
| `I599mjvYW4ZdkNRf` | Won Deal — Auto-Create Onboarding Task Chain | Superseded by M5 |
| `QX0VicX53AzQmHPY` | M1_ClientOnboarding_Orchestrator | Predecessor to M5 |
| `7gKYzCvV0zibOWq9` | Task Blocked - DM Andrew v2 | Replaced by `ra2F0R9zrKMmGEvE` |
| `SDIWZGNRgXFwg81W` | Task Notifications v2 | Superseded |
| `DH5Yx9S2RS6OO6qG` | Task Completed → Auto-Set Completed Date | Superseded |
| `KEcx3yQ7kephk0cM` | Daily Data Hygiene Check | Replaced by Stale Record Detector |
| `apbdh284pFlCy2hZ` | QA Ready → Create QA Task for Andrew | Superseded |
| `XGVbY2c8ijPoz54w` | Recurring Maintenance Tasks | Demo |
| `PpfpYaSQRcGrJqLe` | Weekly Skeleton Tasks | Demo |
| `G0ITjfkhRZqKIWX4` | Windsor Metrics Sync v2 | Superseded |
| `GQwRPVA9iaiZwCQ5` | AI Maintenance Agent | Demo |
| `PJaJYLuesPU2oxc7` | RequityAI Enterprise Demo | Demo |
| `9fPbvP6pytQslBD1` | Telnyx Listener Webhook | Experiment |
| `TX7laFirjpUrxDoa` | Optimization Decision → Notify #operations | Superseded by Decision Router |
| `QGtGJydvWkR6vSCj` | Client Communication — Onboarding Updates | Superseded |
| `rtjwykL2X3VwKZxM` | Client Report Auto-Generator | Demo |

That's 23 candidates. Per §3.0 GREEN, removal is scoped to: rename for clarity, tag/group as `archived`, remove zombie scheduleTrigger nodes. Hard delete is YELLOW. Phase 3 §3.0 mandates: deactivate first → 7-day soak → then delete. These are already deactivated, so the soak clock has presumably already started. Andrew confirms soak status and approves bulk archive tagging.

### RED (never)

- Edit trigger nodes on any active workflow without deactivating first
- Touch credentials
- Anything that would break M3 / M4 / M5 chains

---

## STALE-INFRA REFERENCES — added findings

Carrying forward S1–S8 from doc_reconciliation. Adds:

### S9 (NEW) — Architecture map's claim of 4 ConvTracker outcome values

`AgencyOS_Architecture_AtoZ_Apr26.md` doesn't explicitly enumerate `last_call_outcome` values, but spec doc lists only 3 outcome values and SOP_02 lists 3 outcome values — both refer to the *separate* `outcome` field (6 live values, 1 has artifact slug `bjQuK`). Both sets need updating. Already covered by M4 patch.

### S10 (NEW) — Spec's "CSV Import is the primary build method" line

`AgencyOS_SmartSuite_Structure_Spec.md:451` still says "CSV Import is the primary campaign build method". Stale — same as M10. Add to S register and spec patch list.

---

## SUMMARY FOR ANDREW

(See chat summary that follows.)

---

*End of reconciliation.*
