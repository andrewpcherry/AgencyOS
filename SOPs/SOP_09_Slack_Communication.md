# 💬 Slack Communication — How VAs Talk to the System

**App:** Slack workspace (RequityAI)
**Last updated:** 2026-05-10
**Purpose:** How to use Slack to drive SmartSuite — without breaking the automation.
**Who uses this:** VAs (every Slack message you send), Andrew (cross-client + escalation), 3 agents (Sync Agent, Operations Supervisor, Campaign Intelligence Agent).
**Source of truth:** Live Slack workspace + Sync Agent parser (`8tdPtQWO4qDKEjgq`). The parser is the runtime contract — it accepts the apps and field names listed in §6 and rejects everything else.

---

## TL;DR — In 30 Seconds

Slack is wired into SmartSuite. When you post a `/update` message, the Sync Agent reads it within ~60 seconds and writes the change to SmartSuite. No copy-paste, no manual data entry.

**Section 6** is the most important part of this SOP. Get the format right and the system does the work for you.

**Channel rename note:** `#team-tasks` was renamed to `#team-operations` on 2026-04-22. The channel ID `C0AKWU4835E` is unchanged. Use `#team-operations` everywhere.

---

## 1. Channel Map

RequityAI Slack has 4 types of channels. Each has one job.

| Channel | What it's for | Who posts |
|---|---|---|
| `#all-requityai` | Company-wide announcements + recognition | Andrew only — VAs read |
| `#team-operations` (`C0AKWU4835E`) | Cross-client agency rollup. Daily ops briefing 8am ET, sales brief 8:05am ET M-F, system health, stale-record alerts | Agents + Andrew. You post `/update Pipeline` and `/update Finance` here |
| `#team-<client>` | Internal channel per client. Build notes, blockers, questions, day-to-day VA work | You + agents + Andrew. Post `/update Tasks`, `/update Campaigns`, `/update Onboarding` here |
| `#client-<client>` | External, client-facing. Campaign launch notifications, deliverables. Professional tone only | Andrew (mostly) and you with explicit approval. **Never post structured `/update` here** |

### Two channels per client — never mix them up

- `#team-<client>` = INTERNAL. Anything goes (within reason). Build notes, blockers, questions.
- `#client-<client>` = EXTERNAL. Client may be reading. Professional only. Never structured `/update` messages, never internal opinions, never pricing.

### Current client channel pairs (6 as of 2026-05-10)

| Client | Internal | Client-facing |
|---|---|---|
| Real-Vantage | `#team-real-vantage` | `#client-real-vantage` (public) |
| Quick Home Buyers | `#team-quick-home-buyers` | `#client-quick-home-buyers` (public) |
| Ritsel Notes | `#team-ritsel-notes` | `#client-ritsel-notes` (public) |
| First Integrity Home Buyers | `#team-first-integrity-home-buyers` | `#client-first-integrity-home-buyers` (public) |
| Next Journey Homes | `#team-next-journey-homes` | `#client-next-journey-homes` (**private**) |
| Bayrock Home Buyers | `#team-bayrock-home-buyers` | `#client-bayrock-home-buyers` (**private**) |

The two newer clients (Apr 25 onboards) have private `#client-` channels. M5 now defaults `#client-{slug}` to private at creation; Andrew flips public after the client is invited as a guest.

---

## 2. Communication Rules

- Respond to task notifications within 1 hour during working hours.
- Use threads for replies. Never reply in the main channel body.
- Use emoji reactions to acknowledge: ✅ = Done / Acknowledged · 👀 = Seen, working on it · ❓ = Need clarification.
- Don't DM Andrew unless it's urgent and private. Use the appropriate channel.
- Don't use `@channel` or `@here`. Andrew only.
- Keep messages short and actionable. State the issue, what you tried, what you need.
- No personal conversations in work channels.

---

## 3. Quiet Hours

Automated client-facing notifications fire **8am–6pm ET only.** If you see a system message arrive in `#client-<client>` outside that window, it's a system issue — flag to Andrew. Internal channels (`#team-operations`, `#team-<client>`, DMs) can fire any time.

---

## 4. The 3 Agents

| Agent | What it does | Your job |
|---|---|---|
| **Campaign Intelligence Agent** (`6TuDo3mqBZSBF667`) | Currently dormant — auto-reactivates on first live campaign. Reads campaign metrics every 12h, writes a decision (Keep Running / Cut / Retarget / Swap Creative / Needs Review) to the Optimization record, DMs Andrew | When it sends a task spec — execute exactly as given. Don't modify thresholds or lookback windows |
| **Operations Supervisor** (`5cdMtOByeZVRFS6H`) | 8am + 8pm ET. Posts daily ops briefing in `#team-operations`. Flags stuck records and slow movement | Read the briefing. If it flags something assigned to you, act + post a `/update` |
| **SmartSuite Sync Agent** (`8tdPtQWO4qDKEjgq`) | Reads your `/update` messages within ~60s. Parses, finds the matching record, writes the change. Reacts ✅ or ⚠️ | Post correctly formatted messages. If ⚠️, fix and repost. Don't let ⚠️ sit |

---

## 5. When to Use a Structured `/update` Message

Use a `/update` message any time something should be recorded in SmartSuite:

- Completing a task
- Flagging a task as blocked
- Reporting a campaign build is ready for QA
- Confirming an onboarding step is done
- Logging a Pipeline deal stage change
- Responding to a Campaign Intelligence Agent directive

If your message is a question or discussion, you do NOT need the structured format. Only use it when the result should update a SmartSuite record.

---

## 6. The Format

Every structured message starts with `/update [App]` on the first line, then `field: value` pairs on each subsequent line.

```
/update [App]
Client: [exact client name from SmartSuite]
[field]: [value]
[field]: [value]
Notes: [optional context]
```

### Rules that bite

- `/update [App]` MUST be on the first line. App = `Tasks`, `Campaigns`, `Onboarding`, `Pipeline`, `Optimization`, `Finance`, or `Clients`.
- `Client:` MUST exactly match SmartSuite (case-sensitive). "Quick Home Buyers" — not "QHB" or "quick home".
- Each field on its own line. Don't combine.
- Status / stage / step values MUST match SmartSuite dropdown labels exactly.
- Notes is optional but encouraged.
- Don't add fields not listed for that app.

### Bot reactions

- ✅ = parsed and written successfully.
- ⚠️ = parse error. Re-read this section, fix your message, repost.

### App-specific formats

#### Tasks

Valid `Status`: `To Do`, `In Progress`, `Blocked`, `Done`.

Valid `type` values (13 canonical, post-2026-05-10 cleanup):

`Set Up Ad Account Access` · `Set Up Lead Forms` · `Send Video Brief` · `Upload Creative` · `Write Script` · `Build Campaign` · `QA Campaign` · `Launch Campaign` · `Cut / Pause Campaign` · `Swap Creative` · `Adjust Targeting` · `Update SmartSuite Records` · `Escalation Follow-Up`

```
/update Tasks
Client: First Integrity Home Buyers
Task: Build Campaign — TOF EDU VIDEO — First Integrity Home Buyers
Status: Done
Notes: 3 ad sets live, all videos from batch 2, Special Ad Category = Housing confirmed.
```

Blocked example:

```
/update Tasks
Client: Real-Vantage
Task: Set Up Ad Account Access
Status: Blocked
Notes: Client hasn't approved Business Portfolio access — DM'd them in #client-real-vantage on May 10.
```

#### Campaigns

Valid `Action`: `Build Complete`, `QA Ready`, `Launched`, `Paused`, `Issue`.

```
/update Campaigns
Client: Quick Home Buyers
Campaign: Probate Video Views — Dallas
Action: QA Ready
Notes: 3 ad sets, Dallas DMA, $20/set/day, all creatives approved.
```

#### Onboarding

Valid `Status`: `Not Started`, `In Progress`, `Complete`. Valid `Step`: any of the 18 named steps (see SOP_04).

```
/update Onboarding
Client: Quick Home Buyers
Step: Ad Account Visible
Status: Complete
Notes: Ad account ID 1234567890 confirmed in Business Manager.
```

#### Pipeline

Valid `Stage` (10 values):

`Conversation - Positive` · `Follow Up / Reschedule` · `Booked` · `No Show` · `Cancelled` · `Proposal - Decision - Pending` · `Ghosted` · `Signed - Invoice Sent` · `Won` · `Lost`

> NDM lives in Conversation Tracker `last_call_outcome`, NOT Pipeline. Don't try to write `Stage: NDM` — it'll bounce ⚠️.

Pipeline updates go in `#team-operations`, not a client channel.

```
/update Pipeline
Client: Marcus Johnson
Deal: Marcus Johnson — May 2026
Stage: Booked
Notes: Discovery call scheduled Mon 2pm ET via Calendly.
```

#### Optimization

Valid `Action`: `Review Complete`, `Budget Change`, `Creative Swap`, `Audience Update`, `Paused`, `Restarted`. VAs rarely write here — Andrew owns optimization decisions.

#### Finance

Valid `Action`: `Payment Received`, `Invoice Sent`, `Payment Overdue`, `Refund Issued`. Andrew only.

#### Clients

Valid `Action`: `Info Update`, `Issue`, `Escalation`, `Note`. For `Info Update`, also include `Field:` and `Value:`.

```
/update Clients
Client: Quick Home Buyers
Action: Info Update
Field: Ad Account ID
Value: 1234567890
Notes: Confirmed in Business Manager today.
```

---

## 7. Common Mistakes — Don't Do This

- ❌ Free-form: "Hey I finished the campaign for QHB, it's the probate one in Dallas, 3 ad sets" — won't parse, no record updated.
- ❌ Abbreviated client name: `Client: QHB` — won't match SmartSuite. Use the exact full name.
- ❌ Made-up status value: `Status: Finished` — must be an exact SmartSuite dropdown label.
- ❌ Multiple updates in one message — post each as a separate `/update`.
- ❌ Ignoring agent specs — if Campaign Intelligence says 25% / 30-day lookback, don't use 75% / 14-day.
- ❌ Posting structured `/update` in `#client-<client>` — never. Those are client-facing.
- ❌ Letting a ⚠️ reaction sit — fix and repost immediately.

---

## 8. Escalation — When to DM Andrew

- A live campaign is broken or about to be (account ban, payment failure, ad rejection).
- A `#team-<client>` blocker has gone >30 minutes unanswered AND it's blocking a live campaign.
- A system alert affects a live campaign.
- A client looks upset or confused in a `#client-<client>` thread.
- You're about to publish and something doesn't look right.

For everything else, post in `#team-<client>` (or `#team-operations` for cross-client) and let it work asynchronously.

---

## 9. The 5 Things You Need to Remember

1. `#team-operations` for cross-client. `#team-<client>` for one-client work. **Never post `/update` in `#client-<client>`.**
2. Every status update goes through a `/update` message — never free-form.
3. Client names = exact match to SmartSuite. Status values = exact dropdown label.
4. ✅ from the bot = processed. ⚠️ = fix and repost.
5. When in doubt, ask in `#team-<client>` as a question (no `/update` prefix). Threads, not main channel.

---

## What NOT to Do

- ❌ Don't create new channels without Andrew's approval.
- ❌ Don't invite external people to any channel without Andrew's approval.
- ❌ Don't discuss client information in `#all-requityai`.
- ❌ Don't post free-form task updates — always use the structured format.
- ❌ Don't use Slack for file storage. All files go to Google Drive.
- ❌ Don't ever post structured `/update` messages in `#client-<client>` channels.
