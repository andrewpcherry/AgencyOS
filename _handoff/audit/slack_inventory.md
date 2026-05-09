# Slack Channel Inventory

**Generated:** 2026-05-09 via Slack MCP probe
**Source of truth:** Live Slack workspace search

## Active client channel pairs (verified)

| Client | Internal (private) | External (public/private) | Status |
|---|---|---|---|
| Quick Home Buyers | #team-quick-home-buyers (C0AS1BVFR1C) | #client-quick-home-buyers (C0ARWDN09AP, public) | ✅ Pair complete |
| Real Vantage | #team-real-vantage (C0AS3DU4RNW) | #client-real-vantage (C0ARMBQ3PB9, public) | ✅ Pair complete |
| Ritsel Notes | #team-ritsel-notes (C0ARN0FR6G7) | #client-ritsel-notes (C0ARMBQ4WUX, public) | ✅ Pair complete |
| First Integrity Home Buyers | #team-first-integrity-home-buyers (C0AS1BW865U) | #client-first-integrity-home-buyers (C0AS6CXPHFW, public) | ✅ Pair complete |
| Next Journey Homes | #team-next-journey-homes (C0AV52EGCHY) | #client-next-journey-homes (C0AV1PWCL05, **private**) | ⚠ Created Apr 25; client channel is private (others are public) |
| Bayrock Home Buyers | #team-bayrock-home-buyers (C0AVAJ5KM0U) | #client-bayrock-home-buyers (C0AV3KEEGUV, **private**) | ⚠ Created Apr 25; both private |

## Operational channels

| Channel | ID | Notes |
|---|---|---|
| #team-operations | C0AKWU4835E | Renamed from #team-tasks on Apr 22 (per memory). Live. |
| #new-clients | C0ARPNFGVDH | Onboarding handoff channel. Live. |

## Findings vs current docs

**1. Master state doc (Apr 20) lists 4 active clients.** Slack shows 6 client channel pairs — Real Vantage, Quick Home Buyers, Ritsel Notes, First Integrity, **Next Journey Homes (Apr 25)**, **Bayrock Home Buyers (Apr 25)**. Two clients onboarded after the state doc was written. Master state doc is stale.

**2. Channel naming convention is consistent across all 6 pairs.** Format: `#team-<slug>` private + `#client-<slug>` public-or-private. SOP_09 V2's pair pattern matches reality.

**3. Two newer clients (Next Journey, Bayrock) have PRIVATE client channels.** First four have public client channels. This is a quiet operational drift — either intentional (newer clients prefer private) or unintentional (Bot defaulted to private when Andrew wasn't watching). Worth confirming intent.

**4. SOP_09 V2's example client list is incomplete.** Lists only the first 4. Needs Next Journey and Bayrock added.

**5. Dead channel C0AKWU4H8C8 (per memory) — not visible in search.** Likely already archived/cleaned. No action needed.

**6. RequityAI Bot creator pattern verified.** Bot creates `#team-` channels (private). Andrew creates `#client-` channels manually. Bot also created Bayrock's `#client-` (Apr 25) — the one outlier from the Andrew-creates-client-channel pattern. That's the M5 Deal Won workflow auto-creating both halves of the pair, per memory project_m5_deal_won_live_apr24.md. The Andrew-as-creator pattern on the older 4 reflects pre-M5 manual creation.

## Anomalies / open questions

- Why are Next Journey + Bayrock client channels private when First Integrity / Quick Home Buyers / Real Vantage / Ritsel are public? Need to clarify whether M5 should default-create as public or private.
- No `#all-requityai` channel found in the "team" or "client" searches — may exist under different naming. Needs follow-up search.
