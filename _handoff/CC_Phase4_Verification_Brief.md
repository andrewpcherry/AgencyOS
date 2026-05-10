# Phase 4 — Functional Verification (added May 9 evening)

**Mission expanded from "doc cleanup + VA Manual" to "make sure AgencyOS actually works."**

The original brief (`CC_Prompt_SOP_Alignment_May09.md`) covered Phase 1 (audit), Phase 2 (reconciliation), Phase 3 (doc patches + n8n cleanup + VA Manual). That was scoped to documentation alignment. Andrew's actual goal is broader: every automation, every flow, working end-to-end. This phase fills that gap.

## What Phase 4 covers

For every one of the 21 active n8n workflows + every cross-system chain (M3 Calendly, M4 No-Show, M5 Deal Won, Windsor metrics, Slack /update parser, Onboarding step progression, Campaigns build → QA → launch), produce a verified-working state report.

## Method

For each workflow / chain:

1. **Read the workflow JSON** — confirm trigger, nodes, expected behavior
2. **Run a synthetic test** — fire a controlled input that exercises the workflow's path. Examples:
   - Sync Agent: post a known-good `/update` message to a test Slack channel; verify SmartSuite record updates within 60 seconds
   - M3 Calendly: send a synthetic `invitee.created` webhook; verify Pipeline record created with correct fields
   - M5 Deal Won: flip a test Pipeline deal to `Won`, `won_processed=false`; verify Client + Onboarding records created, Drive folder created, Slack channels created, niche-aware brief delivered
   - Windsor sync: trigger the cron manually; verify it returns clean (zero records is fine if no live campaigns)
   - Onboarding progression: flip a step status; verify next-step trigger fires
3. **Confirm output lands correctly** — record exists, values populated, downstream notification sent
4. **Document the result**: GREEN (works as advertised), YELLOW (works but with caveats), RED (broken)
5. **For RED**: surface to Andrew with proposed fix; do not patch live infra without escalation per CLAUDE.md

## Specific verifications required (from the audit)

- **YELLOW-N1 (RUNTIME)** — Slack Ops Supervisor + Onboarding Health Monitor have been silently failing 17 days writing to renamed `#team-tasks`. After Phase 3 patches that channel reference, verify both workflows resume sending to `#team-operations` with one synthetic trigger each.
- **M22 (RUNTIME)** — After SmartSuite Tasks `type` dropdown collapse + retirement, verify Sync Agent parser correctly maps every canonical task type when receiving `/update Tasks` Slack messages with each new value.
- **M5 chain** — End-to-end: Pipeline deal Won → Client record → Onboarding record → Drive folder → Slack channels (private/public per Q1) → niche-aware brief delivery → notification to #team-operations.
- **M3 + M3 Close hydration** — Calendly invitee.created webhook → Pipeline record + Close contact lookup → close_lead_id populated, company/phone/title hydrated.
- **M4 No-Show** — Pipeline deal_stage flipped to "No Show" → Calendly invitee_no_show API call → Calendly Workflow reschedule SMS+email fires.
- **Sales Brief** (`pa7I1FKd50TQRFrV`) — verify 8:05am ET cron next fire produces correct counts in #team-operations.
- **Windsor sync** — trigger manual run; verify HTTP auth, response shape, write path. Even with zero campaigns to pull, the workflow should complete green.
- **All cron triggers** — for each scheduled workflow, verify last execution timestamp matches expected cadence. Zombie staleData detector pass.

## What CC can/can't do here

**GREEN — can run autonomously:**
- Read-only verification (pull workflow execution logs, check status fields)
- Synthetic triggers that don't affect real client data (test channel posts, deactivated test workflows)
- Documenting findings

**YELLOW — surface and ask:**
- Any synthetic test that touches a real client record (a real Pipeline deal, a real Client onboarding) — escalate before running
- Any fix that modifies an active workflow's logic (not just renaming or tagging) — escalate before patching
- Triggering M5 against a real won deal — never. Use a synthetic test deal only.

**RED — never:**
- Modifying production credential storage
- Sending real client-facing communications during testing (no real Slack messages to real client channels, no real Calendly bookings)
- Anything that bills against Andrew's accounts (Anthropic, Windsor, paid services) beyond minimal verification calls

## Deliverable

`_handoff/audit/verification_results.md` — one row per workflow / chain, with:
- Name + ID
- Test method used
- Result: GREEN / YELLOW / RED
- Evidence (execution log timestamp, response body, side-effect check)
- For YELLOW/RED: proposed fix + escalation status

This becomes the proof that AgencyOS actually works before any VA touches it. It's also Andrew's ground-truth for what's safe to demo and what's not.

## When Phase 4 happens

After Phase 3 doc patches + n8n cleanup land, before the VA Operator Manual write begins. The Manual gets written against a verified-working system, not against an audited but untested one. That's what makes the Manual real instead of aspirational.

## Model + effort for Phase 4

Sonnet 4.6 + Medium effort throughout. This is structured verification work — well-defined methods per workflow, clear pass/fail criteria. Opus is overkill; Haiku is too shallow for the cross-system chains. Sonnet+Medium is the right balance.

End of Phase 4 brief.
