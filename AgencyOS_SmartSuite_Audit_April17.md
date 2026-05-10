# AgencyOS — SmartSuite Audit (April 17, 2026)

**Purpose:** Verify SmartSuite is 100% correct before touching n8n workflows.
**Method:** API audit of every app's actual fields vs spec.

---

## Summary

| App | Spec Fields | Actual Fields | Status |
|-----|------------|---------------|--------|
| Pipeline | 24 | 24 | ✅ Clean |
| Conversation Tracker | 12 | 12 | ✅ Clean |
| Clients | ~25 target | 30 | ⚠️ Issues found |
| Onboarding | 19 steps + 5 core | 19 steps + 15 (incl system) | ⚠️ Minor issues |
| Campaigns | ~40-45 target | 51 | ⚠️ Issues found |
| Tasks | 24 | 21 | ✅ Functional |
| Optimization | 30 | 30 | ✅ Clean |
| Finance | 18 | 18 | ✅ Clean |

**Deleted apps confirmed:** Scripts ✅, Creative Assets ✅

---

## Issues Found

### CRITICAL (affects workflow correctness)

**1. Clients app — Missing: Ad Account ID**
- Spec says: `Ad Account ID | Text | Meta ad account ID`
- Reality: Field does not exist
- Impact: Any workflow that needs to reference a client's ad account has nowhere to read it from
- Fix: Add `ad_account_id` text field to Clients app

**2. Campaigns app — Missing: Funnel Stage**
- Spec says: `Funnel Stage | Dropdown | TOF / MOF / BOF`
- Reality: Field does not exist
- Impact: Campaign naming convention uses TOF/MOF/BOF prefixes. Without this field, no way to filter or sort by funnel position. The SOP naming convention ("TOF | EDU VIDEO | [MARKET]") depends on this.
- Fix: Add `funnel_stage` dropdown with TOF / MOF / BOF choices

**3. Campaigns app — Missing: Market**
- Spec says: `Market | Text | Geographic market`
- Reality: Field does not exist
- Impact: Campaign naming convention includes market. No way to group campaigns by market.
- Fix: Add `market` text field to Campaigns app

### MODERATE (system-slug fields — ugly but functional)

**4. Campaigns app — System-generated slugs on key fields**
These fields exist but have auto-generated slugs instead of readable ones:
| Label | Actual Slug | Should Be |
|-------|------------|-----------|
| Link to Tasks | s1o4gai1 | link_to_tasks |
| Link to Reviews | sbnlxsxl | link_to_reviews |
| Campaign Name | s121aee092 | campaign_name |
| Ad Set Name | sa3ea1a428 | ad_set_name |
| Ad Name | s0822bef9f | ad_name |

- Impact: Any n8n workflow referencing these must use the ugly slugs. Not a blocker but error-prone.
- Fix: Cannot rename slugs via API (SmartSuite limitation). Workflows must use actual slugs.

**5. Clients app — System-generated slugs on linked records**
| Label | Actual Slug | Should Be |
|-------|------------|-----------|
| Link to Campaigns | sxk0tn88 | link_to_campaigns |
| Link to Tasks | s0jlr1ps | link_to_tasks |

**6. Optimization app — System-generated slug**
| Label | Actual Slug | Should Be |
|-------|------------|-----------|
| Link to Tasks | s71eb0cb | link_to_tasks |

### LOW (cosmetic / cleanup)

**7. Onboarding app — Default system fields still visible**
- description, assigned_to, status, due_date, priority still present
- These duplicate onboarding_stage and add clutter
- Fix: Hide in views (UI only, not API)

**8. Spec is outdated**
- Spec still lists 8 Audience Build step fields that were intentionally deleted on Apr 13
- Spec doesn't include step_videos_edited (added Apr 16)
- Fix: Update spec to match reality

---

## Verified Field Map — What n8n Workflows MUST Use

### Onboarding App (69db909cd9114601cccb2b57)

**Core fields:**
- `title` — Client name
- `client` — Linked record to Clients
- `onboarding_stage` — Dropdown: 1=Access Setup, 2=Video Briefing, 3=Awaiting Videos, 4=Videos Received, 5=Campaign Build, 6=QA, 7=Live
- `onboarding_notes` — Rich text
- `blocker_notes` — Rich text

**Step fields (19 total, all singleselectfield with "1"=Not Started, "2"=In Progress, "3"=Complete):**

Phase 1 — Account Access:
- `step_business_portfolio_access`
- `step_ad_account_visible`
- `step_facebook_page_confirmed`
- `step_instagram_connected`
- `step_meta_ads_app_installed`

Phase 2 — Lead Setup:
- `step_leads_access_confirmed`
- `step_lead_notifications_set`
- `step_lead_centre_to_crm`
- `step_lead_destination_confirmed`
- `step_fb_lead_centre_connected`

Phase 3 — Videos:
- `step_video_brief_sent`
- `step_videos_received`
- `step_videos_edited`
- `step_approved_videos_exist`

Phase 4 — Campaign Launch:
- `step_campaign_built`
- `step_qa_passed`
- `step_campaign_launched`
- `step_launch_notification_sent`

Master:
- `step_onboarding_complete`

### Clients App (69ce5f18cb8a07430bfee02d)

**Key fields for workflows:**
- `title` — Business Name
- `status` — Dropdown: Onboarding / Active / Paused / Churned
- `contact_name`, `contact_email`, `contact_phone`
- `owner_name`
- `market_region`
- `business_portfolio_id`
- `facebook_page_url`
- `instagram_handle`
- `monthly_ad_budget`
- `drive_folder_url`
- `assigned_va_select`
- `slack_channel_id`
- `link_to_onboarding` — Linked to Onboarding app
- `sxk0tn88` — Link to Campaigns (system slug)
- `s0jlr1ps` — Link to Tasks (system slug)
- `link_to_optimization`
- `finance_records`
- `live_campaigns` — Count
- `open_tasks` — Count
- `total_revenue` — Rollup
- ❌ `ad_account_id` — MISSING, needs adding

### Campaigns App (69ce678977bf866e34b46f68)

**Key fields for workflows:**
- `title` — Campaign Record Name
- `client` — Linked to Clients
- `status` — Dropdown: Draft / QA Ready / Live / Paused / Cut / Completed
- `campaign_type` — Dropdown: Video Views / Retarget / Lead Ad
- `owner_select`
- `week`
- `daily_budget`
- `launch_date`
- `platform_campaign_id`
- `script_link`, `asset_link` — Google Drive URLs
- `script_id` — Script identifier
- `posted_to_page` — Organic posting tracker
- `s121aee092` — Campaign Name (system slug)
- `sa3ea1a428` — Ad Set Name (system slug)
- `s0822bef9f` — Ad Name (system slug)
- `s1o4gai1` — Link to Tasks (system slug)
- `sbnlxsxl` — Link to Reviews/Optimization (system slug)
- `client_launch_notified`
- `build_sop_reference`
- QA fields: `qa_correct_video_uploaded`, `qa_correct_page_ig_identity`, `qa_correct_geo_market`, `qa_correct_budget_set`, `qa_naming_convention_matches`, `qa_special_ad_category_housing`, `qa_placements_correct`, `qa_cbo_off`, `qa_cta_correct`
- Metrics: `spend`, `thruplays`, `cost_thruplay`, `views_50`, `views_75`, `views_95`, `saves`, `shares`, `comments`, `dms`, `leads`, `cost_lead`, `last_pull_date`
- ❌ `funnel_stage` — MISSING, needs adding (TOF / MOF / BOF)
- ❌ `market` — MISSING, needs adding

### Tasks App (69ce67b3fec5b91842ebaf03)

**Key fields for workflows:**
- `title` — Task name
- `status` — Dropdown
- `type` — Dropdown (15 task types)
- `priority` — Dropdown: Urgent / High / Normal / Low
- `assigned_to_select`
- `due_date`
- `blocker_reason` — Rich text
- `evidence` — File upload
- `client` — Linked to Clients
- `campaign` — Linked to Campaigns
- `blocker_dm_sent`
- `task_category`
- `completed_date`
- `slack_thread` — Link
- `opt_review` — Linked to Optimization

### Optimization App (69ce67e0...)

**Key fields for workflows:**
- `title`
- `review_date`, `next_review_date`, `re_review_date`
- `campaign` — Linked to Campaigns
- `client` — Lookup from Campaign
- `funnel_stage` — Lookup from Campaign
- `decision` — Dropdown: Keep Running / Cut / Retarget Test / Lead Ad Candidate / Swap Creative / Needs Review
- `why` — Text area (AI reasoning)
- `decision_notification_sent` — Yes/No
- `next_action`
- Metrics: `spend`, `thruplay_count`, `cost_per_thruplay`, `thruplay_rate`, `views_50pct`, `views_75pct`, `views_95pct`, `saves`, `shares`, `ad_comments`, `dms`
- `watch_depth_signal`, `engagement_signal`
- `script_id`
- `s71eb0cb` — Link to Tasks (system slug)

### Pipeline App (6908636826cfbf4238a34f31)

✅ Clean — 24 fields, matches spec exactly.

### Conversation Tracker App (69d92c38...)

✅ Clean — 12 fields, matches spec exactly.

### Finance App (69cee162...)

✅ Clean — 18 fields, matches spec.

---

## Extra Apps (not in spec)

10 additional apps exist beyond the core 8:
- Teams (11f), Members (38f) — likely system/workspace apps
- Contracts (27f), Invoices (24f), Payments (19f), Revenue Recognition (15f), Expenses/COGS (17f), Profitability by Client (24f), Client ROI Tracking (26f), Financial Metrics Dashboard (26f) — Finance sub-apps

**Decision needed:** Are these in use? If not, they add clutter. If yes, the spec should document them.

---

## Action Plan

### Must Fix Before Workflows:
1. ✅ Add `ad_account_id` text field to Clients app
2. ✅ Add `funnel_stage` dropdown (TOF/MOF/BOF) to Campaigns app
3. ✅ Add `market` text field to Campaigns app
4. ✅ Update spec to match reality (remove audience steps, add step_videos_edited)

### Nice to Have (cosmetic):
5. Hide default system fields in Onboarding app views
6. Document system-slug fields so future workflow builders know the mappings
