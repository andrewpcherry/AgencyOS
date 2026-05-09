# SmartSuite Inventory — Live Truth (2026-05-09)

**Source:** Raw schema dumps in `_handoff/audit/raw/ss_app_*.json`, pulled via SmartSuite API by Andrew on 2026-05-09. Sanitized of secrets; functional fields, slugs, and choice lists intact.

**Headline:** Live workspace contains **12 apps**, not 8 as `AgencyOS_SmartSuite_Structure_Spec.md` (Apr 17) and `AgencyOS_Architecture_AtoZ_Apr26.md` claim. Of the 4 extras, 2 are SmartSuite system defaults (Teams, Members — every SS workspace has these) and 2 are custom apps not referenced in any documentation (Financial Metrics Dashboard, SOPs).

---

## App roster (12)

| # | App | App ID | Slug | Fields | In docs? | Notes |
|---|---|---|---|---|---|---|
| 1 | Pipeline | `6908636826cfbf4238a34f31` | `tb_pipeline` | 29 | ✅ | Spec says 24 fields — drift of +5 |
| 2 | Conversation Tracker | `69d92c38b801d747e74629d1` | `sxdf8eny` | 14 | ✅ | Spec says 12 — drift of +2 |
| 3 | Clients | `69ce5f18cb8a07430bfee02d` | `shybuqst` | 33 | ✅ | Spec target was ~25; arch map says 31 |
| 4 | Onboarding | `69db909cd9114601cccb2b57` | `sdy1cx8c` | 36 | ✅ | Arch map says 34 — drift of +2 |
| 5 | Campaigns | `69ce678977bf866e34b46f68` | `sepyuwz4` | 54 | ✅ | Arch map says 53 — drift of +1 |
| 6 | Tasks | `69ce67b3fec5b91842ebaf03` | `snpdqupz` | 22 | ✅ | Arch map says 21 — drift of +1 |
| 7 | Optimization | `69ce67e01cc0855f89fee02e` | `sph5lmp9` | 31 | ✅ | Arch map says 30 — drift of +1 |
| 8 | Finance | `69cee1623a5dd7f2078e4d93` | `sma34ein` | 19 | ✅ | Arch map says 18 — drift of +1 |
| 9 | **Teams** | `68bf191d83283ba3ce027d1a` | `teams` | 11 | ❌ | **SmartSuite system app** — every workspace ships with this. Out of scope for VA. |
| 10 | **Members** | `68bf191d83283ba3ce027eff` | `members` | 38 | ❌ | **SmartSuite system app** — workspace member profiles. Out of scope for VA. |
| 11 | **Financial Metrics Dashboard** | `6908751876052786a92cba0b` | `tb_financial_metrics_dashboard` | 26 | ❌ | **Custom analytics app** — MRR/ARR/CAC/churn. Andrew-only. Not in any V2 SOP. Either intentional dormant analytics or scope-creep. **Andrew confirms.** |
| 12 | **SOPs** | `69e2ba10829d2fb61c75f286` | `sukxxo1q` | 13 | ❌ | **Custom SOP registry app** — title/description/status/sop_url/app_name. Not in any current doc. Possibly a future system for SOP versioning. **Andrew confirms.** |

**Action:** Treat Teams + Members as SS system defaults; document briefly but exclude from VA Manual scope. Surface Financial Metrics Dashboard + SOPs to Andrew for a keep/archive decision (see Phase 2 Q7).

---

## Critical dropdown vocabularies (live)

### Tasks — `type` field (15 choices, but ⚠️ DATA INTEGRITY ISSUE)

```
value='2'      label='Set Up Ad Account Access'   ⚠ value collision
value='2'      label='Set Up Lead Forms'          ⚠ value collision
value='2'      label='Request Videos'             ⚠ value collision
value='2'      label='Upload Creative'            ⚠ value collision
value='2'      label='Write Script'               ⚠ value collision
value='2'      label='Admin'                      ⚠ value collision
value='iQMVn'  label='Build Campaign (CSV Import)'
value='n6EvX'  label='Build Campaign (Manual)'
value='WvoJS'  label='QA Campaign'
value='3LeIB'  label='Launch Campaign'
value='pjZqe'  label='Campaign Review'
value='Kr9Qn'  label='Cut / Pause Campaign'
value='LaFdW'  label='Create Retargeting Audiences'   ⚠ retired May 5 — still live
value='gPtcw'  label='Update SmartSuite Records'
value='M2IdT'  label='Escalation Follow-Up'
```

**Findings:**
- **Six choices share `value='2'`** — Set Up Ad Account Access / Set Up Lead Forms / Request Videos / Upload Creative / Write Script / Admin. That's not a sanitization artifact (the other 9 choices have unique 5-character SS-generated IDs). Either (a) actual data corruption — records storing `type='2'` cannot be uniquely interpreted; reads will surface whichever label SS resolves first, or (b) a quirk of how the SS API returns legacy choice values (the 6 collisions are exactly the choices listed in the structure-spec doc dated Apr 17, before the later additions got proper IDs). **Andrew probes a sample Task record to confirm which it is — see Phase 2 #P1.**
- "Create Retargeting Audiences" is still in the live dropdown despite being retired May 5 (per memory `project_audience_creation_collapsed_may05`). No automation creates it (verified across all 55 n8n workflows — zero matches in workflow JSON). It's a stranded option. Removing it is YELLOW per Phase 3 §3.0 (touches live SS schema).
- "Build Campaign (CSV Import)" and "Build Campaign (Manual)" both still present. Per Andrew's decision (M10), these should collapse to a single "Build Campaign" type. The active workflow `uDdwyIl7VDFEWJ8N` Prerequisites Met still writes "CSV Import" — needs updating in lockstep.

### Onboarding — step fields (19 dropdowns, all 3-state Not Started/In Progress/Complete)

Resolves M11. Live count is **19 step_* dropdown fields**: 18 named work steps in 4 phases + 1 master flag.

| Phase | Slug | UI Label |
|---|---|---|
| 1 — Access | `step_business_portfolio_access` | 🔑 Business Portfolio Access |
| 1 — Access | `step_ad_account_visible` | 🔑 Ad Account Visible |
| 1 — Access | `step_facebook_page_confirmed` | 🔑 Facebook Page Confirmed |
| 1 — Access | `step_instagram_connected` | 🔑 Instagram Connected |
| 1 — Access | `step_meta_ads_app_installed` | 🔑 Meta Ads App Installed |
| 2 — Lead Setup | `step_leads_access_confirmed` | 📋 Leads Access Confirmed |
| 2 — Lead Setup | `step_lead_notifications_set` | 📋 Lead Notifications Set |
| 2 — Lead Setup | `step_lead_centre_to_crm` | 📋 Lead Centre to CRM |
| 2 — Lead Setup | `step_lead_destination_confirmed` | 📋 Lead Destination Confirmed |
| 2 — Lead Setup | `step_fb_lead_centre_connected` | 📋 FB Lead Centre Connected |
| 3 — Videos | `step_video_brief_sent` | 🎬 Video Brief Sent |
| 3 — Videos | `step_videos_received` | 🎬 Videos Received |
| 3 — Videos | `step_videos_edited` | Videos Edited *(added Apr 16)* |
| 3 — Videos | `step_approved_videos_exist` | **Ad Creative Ready** *(label drift — slug says approved_videos_exist)* |
| 4 — Campaign Launch | `step_campaign_built` | 🚀 Campaign Built |
| 4 — Campaign Launch | `step_qa_passed` | 🚀 QA Passed |
| 4 — Campaign Launch | `step_campaign_launched` | 🚀 Campaign Launched |
| 4 — Campaign Launch | `step_launch_notification_sent` | 🚀 Client Notified *(label drift — slug says launch_notification_sent)* |
| Master | `step_onboarding_complete` | ✅ Onboarding Complete |

**Canonical phrasing for docs:** "18 onboarding steps in 4 phases (5 + 5 + 4 + 4), plus the master `Onboarding Complete` flag (19 step_* dropdowns total). All 3-state: 1=Not Started, 2=In Progress, 3=Complete."

**Notes:**
- The Sync Agent parser (`8tdPtQWO4qDKEjgq`) `OB_STEP_MAP` lists exactly these 19 entries. Parser ↔ live SS match.
- Two slug-vs-label drifts: `step_approved_videos_exist` is labelled "Ad Creative Ready" in the UI; `step_launch_notification_sent` is labelled "Client Notified". Docs may want to use the slug-derived names for unambiguous reference and add the UI label in parens.
- SOP_09 V2's enumeration of 17 named steps was wrong on two counts: missing `step_videos_edited` AND missing one of the launch-phase steps. Patch in Phase 3.

### Pipeline — `deal_stage` field (10 choices)

Resolves M15. Live values:

```
Conversation - Positive
Follow Up / Reschedule
Booked
No Show
Cancelled
Proposal - Decision - Pending
Ghosted
Signed - Invoice Sent
Won
Lost
```

**Decision:** This 10-stage list is the canonical Pipeline vocabulary. Matches:
- `SOPs/SOP_01_Pipeline.md` exactly ✅
- `AgencyOS_SmartSuite_Structure_Spec.md` exactly ✅
- The Sync Agent parser's `STATUS_MAPS.pipeline` exactly ✅

Contradicts:
- `SOP_09_V2:75` — claims 11 stages including "NDM (No Decision Maker)" and uses entirely different vocabulary ("Lead, Contacted, Discovery Call, Proposal Sent, Negotiation, Verbal Commit, Onboarding, Active Client, Churned"). **None of those 11 strings exist in live SS.** The SOP_09 list is fabricated — likely copy-pasted from a generic CRM template.
- `AgencyOS_Architecture_AtoZ_Apr26.md:55,114` — claims "7 stages (Booked → Engaged → Qualified → Proposal → Won/Lost/No Show)". None of "Engaged" or "Qualified" or "Proposal" exist in live SS. Architecture map fabricated this too.
- Memory `project_m2_replaced_by_polling_apr22` saying "NDM choice added (11 total)" — wrong target. NDM was added to **ConvTracker `last_call_outcome`**, NOT Pipeline `deal_stage`. The memory note conflated the two apps.

### ConvTracker — `last_call_outcome` field (15 choices)

Resolves M4 / Q5. Live values:

```
Owner - Booked
Owner - Talked
Owner - Maybe
Owner - Callback Requested
Owner - Not Interested
Non-Decision Maker (NDM) Interested      ← this is where NDM lives
Gatekeeper
Voicemail
No Answer
Wrong Number
Do Not Call
Hung Up - Owner
Left Voicemail
Voice Agent
Invalid
```

Confirms 15-value expansion (per memory `project_convtracker_outcome_expansion_may06`). NDM lives here, not Pipeline.

### ConvTracker — `outcome` field (separate, 6 choices, ⚠️ broken value)

```
Interested
Maybe
Not Interested
No Contact
Gatekeeper
LVM                                       ⚠ value='bjQuK' (others use label as value)
```

The "LVM" choice has a SS-generated value `bjQuK` instead of the label string. Cosmetic but inconsistent — clean up if doing SS housekeeping.

### Pipeline — `health_status` field

Values: On Track / At Risk / Stalled. Matches spec.

### Clients — duplicate status fields ⚠️

```
status         (singleselect, label="Status (OLD)")  values: Onboarding/Active/Paused/Churned
client_status  (statusfield,  label="Client Status") values: onboarding/active/paused/churned (lowercase, slugified)
priority       (singleselect, label="Niche")         values: REI/Notes/Health/Construction/Other  (slug "priority" misnamed)
```

**Findings:**
- Two parallel status fields. Sync Agent parser writes to `status` (the OLD one). M5 likely also writes to `status`. The newer `client_status` field appears to be a SS UI status type — unclear which is canonical.
- `priority` is the slug for the Niche dropdown — confirms architecture map line 303. Docs that talk about Niche should reference slug `priority`.
- Andrew confirms (Phase 2 #P2): which Client status field is the source of truth? Pick one, deprecate the other.

### Campaigns — clean

```
status:        Draft / QA Ready / Live / Paused / Cut / Completed       ✅ matches spec & docs
campaign_type: Video Views / Retarget / Lead Ad                         ✅
funnel_stage:  TOF / MOF / BOF                                          ✅
owner_select:  VA / Operator                                            ✅
```

### Optimization — `decision` field (5 choices) — ⚠️ NEW MISALIGNMENT

```
Keep Running
Cut
Retarget Test                ← architecture map says "Retarget"
Lead Ad Candidate            ← architecture map doesn't list this
Swap Creative
                             ← architecture map says "Needs Review" (NOT in live)
```

Architecture map lines 233, 240–244, and 423–428 enumerate Cut / Keep Running / Retarget / Swap Creative / **Needs Review** — three of the five mismatch live SS. The Decision Router workflow is INACTIVE (see n8n_inventory.md), so the live divergence has no current consumer, but docs and the Sync Agent parser should match live. Sync Agent parser already matches live exactly (Keep Running / Cut / Retarget Test / Lead Ad Candidate / Swap Creative). **Architecture map needs the patch.** New misalignment **M21**.

### Finance — clean

All 4 dropdowns (record_type, month, payment_status, payment_method) match spec.

---

## Field-count drift summary

| App | Spec / Arch says | Live | Drift |
|---|---|---|---|
| Pipeline | 24 / 24 | 29 | +5 |
| ConvTracker | 12 / 12 | 14 | +2 |
| Clients | 31 (arch) | 33 | +2 (incl. duplicate `client_status`) |
| Onboarding | 34 (arch) | 36 | +2 |
| Campaigns | 53 (arch) | 54 | +1 |
| Tasks | 21 (arch) | 22 | +1 |
| Optimization | 30 (arch) | 31 | +1 |
| Finance | 18 (arch) | 19 | +1 |

Drift is small but consistent — fields have been added since the Apr 17 spec / Apr 26 architecture map without doc updates. Phase 3 should re-emit Structure Spec to match live.

---

## Record counts

Not in scope for the schema dump (would require record-list calls). For the patching pass, record-level checks are needed to:
- Verify P1 (Tasks `type='2'` collision is doc artifact vs real data corruption)
- Verify cross-system referential integrity (every Client has resolvable `slack_channel_id`, `drive_folder_url`)
- Confirm 6 active clients per slack_inventory.md vs SS Clients

Andrew can run a record-list dump per app for the Phase 3 patch verification — out of scope for this audit.

---

*End of SmartSuite inventory.*
