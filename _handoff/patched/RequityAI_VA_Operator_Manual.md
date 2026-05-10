# RequityAI — VA Plug-and-Play Operator Manual

**Version:** 2026-05-10 · canonical
**Who this is for:** the VA who runs RequityAI's client delivery day-to-day.
**How to read this:** front to back, once. Then keep it open as a reference for your first two weeks. Every section earns its place — nothing is filler.

---

## 1. Welcome + the 60-second mental model

RequityAI is a Facebook ads agency for real-estate investors and off-market property buyers. We run a 3-stage funnel for each client:

| Stage | Campaign | What it does |
|---|---|---|
| **TOF** | Video Views | Educational client-recorded video. The audience that watches the most is your retargeting pool. The CTA is "comment OPTIONS" — no link, no form. |
| **MOF** | Retarget | A different talking-head video shown to TOF watchers (50/75/95%). Pushes them to the deepest watch tier. |
| **BOF** | Lead Ad | Facebook Lead Form shown to the warmest watchers. **The only campaign that captures leads.** |

You sit in the middle of that funnel — your work is the deterministic operational steps that move a client from Won deal to live campaign to optimized loop. The agents do the cognition, the automations carry every state change, and you do the precision work that needs human eyes and hands. Andrew runs sales and approves strategy.

Two phrases to lock in:
- **The system holds the state — you don't.** SmartSuite is the source of truth. If a task isn't in SmartSuite, it doesn't exist.
- **Andrew is not the bottleneck.** That's the whole point of this stack. Don't ping him for what an SOP, a task, or a `/update` message can answer.

## 2. The plug-and-play promise

This is the contract between you and the system:

**The system gives you:**
- A queue of tasks in SmartSuite (My Queue view), prioritized.
- Each task is linked to a client record, a campaign record (if relevant), and the SOP you should follow.
- Slack notifications when something needs your attention.
- The 3 agents (see §10) who flag what to look at and recommend what to do next.

**You give the system:**
- Open My Queue. Work top to bottom.
- Follow the SOP linked on each task.
- Post a structured `/update` message in Slack when work is done or blocked.
- Don't invent work. If it's not in the queue, it's not a priority.

That's the entire contract. If you keep it, the system runs itself and Andrew never has to chase you for status.

## 3. Day 1 setup checklist

Andrew owns the access; you confirm each item works.

- [ ] **SmartSuite login** at `app.smartsuite.com` (workspace `sl181chl`). You should see the 8 business apps: Pipeline, Conversation Tracker, Clients, Onboarding, Campaigns, Tasks, Optimization, Finance.
- [ ] **Slack workspace** (RequityAI). You should be in: `#all-requityai`, `#team-operations`, every `#team-<client>` for the active 6 clients, and `#client-<client>` channels you're invited to.
- [ ] **Google Drive access** to the `RequityAI` parent folder (`1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R`). You should see one subfolder per active client.
- [ ] **Meta Business Manager** invitation accepted. You should be able to see RequityAI's Business Portfolio.
- [ ] **Meta Ads Manager** access via the client's Business Portfolio (per-client; will arrive as you complete Phase 1 onboarding for each client).
- [ ] **Password manager** entry for the above so you're not asking Andrew for credentials twice.
- [ ] **You can post in `#team-operations`** and the bot reacts (try a hello message).

If any item is blocked, post a blocker in `#team-operations` (not a DM) so it's visible to the system and to Andrew.

## 4. The tools

| Tool | What it's for | What you touch | What you don't |
|---|---|---|---|
| **SmartSuite** | Source of truth — every record, every status, every SOP link | Task statuses · `/update`-driven field changes · reading client + campaign records | Creating Client/Onboarding/Campaign records (automations do that) · Finance · Optimization decision fields · Onboarding step dropdowns directly |
| **Slack** | Communication + the wire that carries `/update` messages back to SmartSuite | Posting `/update` in `#team-<client>` or `#team-operations` · responding to agent posts · notifying client launches in `#client-<client>` (with Andrew's approval) | Posting structured `/update` in `#client-<client>` · @channel/@here · DMing Andrew unless urgent |
| **Google Drive** | Content store — videos, scripts, ad creative, onboarding docs | Reading raw videos, editing, dropping finished cuts into `Ad Creative/` · reading the niche-specific script library | Renaming or moving files outside the folder structure · uploading raw files into `Ad Creative/` |
| **Meta Business Manager** | Where client business assets are managed | Requesting access · confirming asset visibility · reporting what's missing | Approving access from the client side (the client does that in their own Meta) |
| **Meta Ads Manager** | Where you build, QA, and launch | Building campaigns per SOP_05 · running the 9-point QA checklist · publishing | Changing budgets without an explicit task · running ads outside Special Ad Category = Housing |
| **Lead destinations** | Where leads land — Lead Centre, the client's CRM (often GoHighLevel), a Google Sheet | Confirming lead flow · running test leads when SOP requires | Picking the destination — the client picks; you confirm it works |

## 5. Channel map

| Channel | Purpose | Who posts |
|---|---|---|
| `#all-requityai` | Company-wide announcements + recognition | Andrew only — VAs read |
| `#team-operations` (`C0AKWU4835E`) | Cross-client ops rollup. Daily ops briefing 8am ET, sales brief 8:05am ET M-F, system health, stale-record alerts | Agents + Andrew. You post `/update Pipeline` and `/update Finance` here. |
| `#team-<client>` | Internal channel per client. Build notes, blockers, questions, day-to-day VA work. | You + agents + Andrew. Post `/update Tasks`, `/update Campaigns`, `/update Onboarding` here. |
| `#client-<client>` | External channel per client. Campaign launch notifications, deliverables. | Andrew (mostly) and you with explicit approval. **Never post structured `/update` here.** |

Active client channel pairs (6 as of 2026-05-10):

| Client | Internal (`#team-`) | External (`#client-`) |
|---|---|---|
| Real-Vantage | `C0AS3DU4RNW` | `C0ARMBQ3PB9` (public) |
| Quick Home Buyers | `C0AS1BVFR1C` | `C0ARWDN09AP` (public) |
| Ritsel Notes | `C0ARN0FR6G7` | `C0ARMBQ4WUX` (public) |
| First Integrity Home Buyers | `C0AS1BW865U` | `C0AS6CXPHFW` (public) |
| Next Journey Homes | `C0AV52EGCHY` | `C0AV1PWCL05` (private) |
| Bayrock Home Buyers | `C0AVAJ5KM0U` | `C0AV3KEEGUV` (private) |

The two newer clients have **private** `#client-` channels by design (M5 default since Apr 25). Older 4 are public from pre-M5 manual creation. New clients going forward will start private; Andrew flips public after the client is invited as a guest.

## 6. The structured `/update` format

This is the most important section in this manual. When you post a `/update` message in Slack, the SmartSuite Sync Agent reads it within ~60 seconds and writes the change to SmartSuite. Get the format right and you never touch SmartSuite directly.

**Skeleton:**

```
/update [App]
Client: [exact name from SmartSuite]
[field]: [value]
[field]: [value]
Notes: [optional context]
```

Rules that bite:
- `/update [App]` MUST be the first line. App = `Tasks`, `Campaigns`, `Onboarding`, `Pipeline`, `Optimization`, `Finance`, or `Clients`.
- `Client: <name>` MUST exactly match SmartSuite (case-sensitive). "Quick Home Buyers" — not "QHB" or "quick home".
- Each field on its own line. Don't combine.
- Status / stage / step values MUST match SmartSuite dropdown labels exactly.
- Bot reactions: ✅ = parsed and written. ⚠️ = parse error — fix your message and repost.

### Per-app templates and worked examples

**Tasks** — valid status: `To Do`, `In Progress`, `Blocked`, `Done`. Valid `type` values: the 13 canonical types in §9.

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
Notes: Client hasn't approved Business Portfolio access request — DM'd them in #client-real-vantage on May 10.
```

**Campaigns** — valid `Action`: `Build Complete`, `QA Ready`, `Launched`, `Paused`, `Issue`.

```
/update Campaigns
Client: Quick Home Buyers
Campaign: Probate Video Views — Dallas
Action: QA Ready
Notes: 3 ad sets, Dallas DMA, $20/set/day, all creatives approved.
```

**Onboarding** — valid `Status`: `Not Started`, `In Progress`, `Complete`. Valid `Step`: any of the 18 named steps (see §7).

```
/update Onboarding
Client: Quick Home Buyers
Step: Ad Account Visible
Status: Complete
Notes: Ad account ID 1234567890 confirmed in Business Manager.
```

**Pipeline** — valid `Stage` (10 values): `Conversation - Positive`, `Follow Up / Reschedule`, `Booked`, `No Show`, `Cancelled`, `Proposal - Decision - Pending`, `Ghosted`, `Signed - Invoice Sent`, `Won`, `Lost`. Pipeline updates go in `#team-operations`, not a client channel.

**Optimization, Finance, Clients** — formats listed in SOP_09. You'll rarely touch these as a VA — Andrew owns them.

### The 5 things you must remember

1. `#team-operations` for cross-client. `#team-<client>` for one client. Never post `/update` in `#client-<client>`.
2. Every status change goes through a `/update` message — never free-form text like "I finished the campaign for QHB."
3. Client names = exact match. Status / step / stage values = exact dropdown label.
4. ✅ from the bot = processed. ⚠️ = fix and repost. Don't let ⚠️ messages sit unfixed.
5. When in doubt, ask in `#team-<client>` as a regular question (no `/update` prefix). Threads, not main channel.

## 7. The 4 phases of onboarding

Tracked in the Onboarding app. **18 named steps + 1 master flag (`Onboarding Complete`).** Audience phase was removed 2026-05-05 — retargeting audiences auto-build from Video Views activity, not as an onboarding step.

You don't manually flip step dropdowns — n8n does. Your job is to do the underlying work and post a `/update Onboarding` when done.

### Phase 1 — Account Access (5 steps)
| # | Step | What you do |
|---|---|---|
| 1 | Business Portfolio Access | Request access in Meta Business Manager. Client approves in their own Meta. |
| 2 | Ad Account Visible | Confirm the client's ad account appears in your Business Manager. |
| 3 | Facebook Page Confirmed | Confirm the correct FB page is identified and accessible. |
| 4 | Instagram Connected | Confirm the client's IG is linked to their FB page. |
| 5 | Meta Ads App Installed | Confirm the client has the Meta Ads app on their phone (for lead notifications). |

### Phase 2 — Lead Setup (5 steps)
| # | Step | What you do |
|---|---|---|
| 6 | Leads Access Confirmed | Confirm you can see Lead Centre. |
| 7 | Lead Notifications Set | Confirm client gets email/push on new leads. |
| 8 | Lead Centre to CRM | Confirm leads flow to the client's CRM (GoHighLevel, sheet, etc.). |
| 9 | Lead Destination Confirmed | Client has confirmed where leads should go. |
| 10 | FB Lead Centre Connected | Full Lead Centre setup verified. |

### Phase 3 — Videos (4 steps) · You own this end-to-end
| # | Step | What you do |
|---|---|---|
| 11 | Video Brief Sent | Send the niche-specific video recording brief to the client. |
| 12 | Videos Received | Client uploads raw videos to `Raw Video/`. |
| 13 | Videos Edited | **You edit the raw videos** and drop finished cuts into `Ad Creative/`. Editing is part of the VA's role as of May 9 2026. Assume a 4–6 week skill ramp before quality is consistent. |
| 14 | Approved Videos Exist | Andrew reviews and approves cuts for ad use. |

### Phase 4 — Campaign Launch (4 steps)
| # | Step | What you do |
|---|---|---|
| 15 | Campaign Built | You build per SOP_05. |
| 16 | QA Passed | You run the 9-point QA checklist (§8). |
| 17 | Campaign Launched | You publish in Ads Manager. Status flips to Live. |
| 18 | Launch Notification Sent | The system posts to `#client-<client>`. You confirm the client got it. |

When Step 18 fires, the master `Onboarding Complete` flag goes 🟢 and Client.status flips to `Active`.

**Blockers** go in the Onboarding record's `Blocker Notes` field — and post a `/update Tasks` with `Status: Blocked` for the related task.

## 8. The campaigns workflow

The 3-stage funnel from §1, expanded into the build-and-launch sequence.

### Naming convention (non-negotiable)
- **Campaign:** `[CAMPAIGN TYPE] | [MARKET]` → e.g., `VIDEO VIEWS | PHOENIX AZ`
- **Ad Set:** `[CLIENT CODE] | [AUDIENCE] | [DATE]` → e.g., `APEX | 25PCT-VIEWERS | APR2026`
- **Ad:** `[SCRIPT ID] | [SITUATION] | [VERSION]` → e.g., `FC-B2-14 | FORECLOSURE | V1`

### Build sequence (per SOP_05 — read it before every build)
1. Open the Campaign record (Status = Draft) in Build Queue view.
2. Confirm: client, market, type, daily budget, script link, asset link, week.
3. Pull the video file from `Ad Creative/`.
4. Build in Ads Manager. Naming convention exact. Audiences: broad for Video Views; 25%/50% for Retarget; 75%/95% for Lead Ad.
5. **Set Special Ad Category = Housing.** Required by law. Skipping risks an account ban.
6. **No zip-code targeting.** City/state level only.
7. **CBO off.**
8. Set the CTA: Video Views + Retarget = no CTA button (copy says "comment OPTIONS"). Lead Ad = Facebook Lead Form attached.
9. Save as draft.
10. Mirror the Campaign Name, Ad Set Name, Ad Name, Platform Campaign ID, Owner into the SmartSuite Campaign record. Flip Status to **QA Ready**.

### QA checklist (9 items — all must be ✅ before publish)
1. Correct video uploaded (matches Asset Link).
2. Correct Page + IG identity.
3. Correct geo / market.
4. Correct daily budget.
5. Naming convention matches exactly.
6. **Special Ad Category = Housing.**
7. Placements (FB + IG feeds + Reels typically).
8. CBO off.
9. CTA correct (no button on Video Views/Retarget; Lead Form on Lead Ad).

### Publish sequence
1. All 9 QA ticks ✅.
2. Andrew DM'd for go/no-go (the QA Ready Slack workflow handles this).
3. On approval, hit **Publish** in Ads Manager.
4. In SmartSuite: Campaign Status → **Live**, Launch Date → today, Client Launch Notified → ✅.
5. Post `/update Campaigns Action: Launched` in `#team-<client>`.
6. Mark the linked Task as **Done**.

### How retargeting audiences are handled
You do **not** create retargeting audiences as a task — that task type was retired May 5. Audiences auto-build from Video Views campaign activity. When a Build Campaign task arrives for Retarget or Lead Ad, you confirm the 25%/50%/75%/95% video-viewer audiences exist in Ads Manager before assembling. If they don't exist, the Video Views campaign hasn't run long enough — flag it in the Task as Blocked.

## 9. The Tasks app and the daily loop

**Default view:** My Queue. **This is your home screen.**

Sorted by Priority (Urgent → High → Normal → Low) then Due Date. Open the top task. Read it. Open the linked SOP. Open the linked client + campaign records. Do the work. Update Status.

**13 canonical task types** (live SmartSuite dropdown after the 2026-05-10 cleanup):

| # | Type | What it means |
|---|---|---|
| 1 | Set Up Ad Account Access | Phase 1 — Meta access flow |
| 2 | Set Up Lead Forms | Phase 2 — Lead Centre + CRM wiring |
| 3 | Send Video Brief | Phase 3 — niche-specific brief to client |
| 4 | Upload Creative | Phase 3 — edit raw videos, place in `Ad Creative/` |
| 5 | Write Script | Edit AI-generated script for client voice |
| 6 | Build Campaign | Phase 4 — single canonical build task per SOP_05 |
| 7 | QA Campaign | Phase 4 — 9-point QA checklist |
| 8 | Launch Campaign | Phase 4 — publish + status flip |
| 9 | Cut / Pause Campaign | Optimization output — kill or pause underperformer |
| 10 | Swap Creative | Optimization output — replace creative with approved alternate |
| 11 | Adjust Targeting | Optimization output — modify audience targeting |
| 12 | Update SmartSuite Records | One-off SS update — read Notes for which app/record/field |
| 13 | Escalation Follow-Up | Follow up on a flagged blocker per Notes |

**Status semantics:**
- **To Do** — in your queue, not started.
- **In Progress** — actively working it. Don't sit on this for >24h without an update.
- **Blocked** — fill `Blocker Notes`, post `/update Tasks Status: Blocked`, ping `#team-<client>`.
- **Done** — actually complete. Be honest.

**Priority response times:**
| Priority | When |
|---|---|
| Urgent | Within 1–2 hours |
| High | Same day |
| Normal | 1–2 days |
| Low | 3–5 days |

## 10. The 3 agents

Three intelligence agents support the system. They watch data and recommend; you execute.

| Agent | What it does | Your job |
|---|---|---|
| **Campaign Intelligence Agent** (currently dormant — activates on first live campaign) | Reads live campaign metrics every 12h. Writes a decision (Keep Running / Cut / Retarget / Swap Creative / Needs Review) to the Optimization record. DMs Andrew the summary. | Read its decisions when they arrive as task assignments. Execute the operational tasks (Cut/Pause, Swap Creative, Adjust Targeting). Don't argue with the spec — if it says 25% / 30-day lookback, use exactly that. |
| **Operations Supervisor** | 8am + 8pm ET. Posts daily ops briefing in `#team-operations`. Flags stuck records and slow movement. | Read the briefing. If it flags something assigned to you, act and post a `/update`. |
| **SmartSuite Sync Agent** | Reads your `/update` messages within ~60s. Parses, finds the matching record, writes the change. Reacts ✅ or ⚠️. | Post correctly formatted messages. If ⚠️, fix and repost. Don't let ⚠️ sit. |

## 11. Escalation paths

**DM Andrew** (only when):
- Live campaign is broken or about to be (account ban, payment failure, ad rejection).
- Client looks upset or confused in a `#client-<client>` thread.
- You're about to publish and something feels wrong.
- A blocker has gone >30 minutes unanswered in `#team-<client>` and is blocking a live campaign.

**Post in `#team-<client>`** (default for anything client-specific):
- Build questions, blocker reports, missing access, conflicting instructions.

**Post in `#team-operations`** (cross-client):
- System-wide issues, agent errors, vocabulary confusion across clients.

**Use `/update Tasks Status: Blocked`** (always when you can't complete a task):
- Fill `Blocker Notes`. Be specific. "Ad account access not yet confirmed" beats "access not working."

### Decisions that are NOT yours
Pricing · contracts · refunds · scope · strategic ad changes · creative concept choices · client business questions · anything risky. These are Andrew's. If a client asks: "Thanks, I'm checking that and will confirm shortly," then ping Andrew internally.

## 12. Common mistakes — explicit, named

- ❌ Inviting clients into internal `#team-<client>` channels.
- ❌ Posting structured `/update` in `#client-<client>`.
- ❌ Building campaigns in the wrong ad account.
- ❌ Forgetting Special Ad Category = Housing.
- ❌ Using a raw file from `Raw Video/` instead of the approved cut from `Ad Creative/`.
- ❌ Assuming the newest Drive file is the correct one — read the task to confirm the file ID.
- ❌ Publishing without all 9 QA checks ✅.
- ❌ Marking a task **Done** before the work is actually done.
- ❌ Free-form Slack updates that won't parse ("Hey I finished the QHB campaign...").
- ❌ Abbreviating client names ("QHB", "real vantage" — must match SmartSuite exactly).
- ❌ Using made-up status values ("Finished" instead of "Done").
- ❌ Modifying agent specs ("the agent said 25% but I used 30%" — never).
- ❌ Sitting on a `⚠️` reaction without fixing the message.
- ❌ DMing Andrew for things an SOP, the agent, or `/update` can answer.
- ❌ Touching Finance, Optimization decision fields, or directly flipping Onboarding step dropdowns.

## 13. Troubleshooting matrix

| If this happens… | Do this |
|---|---|
| ⚠️ reaction on your `/update` | Re-read §6. Most common: client name doesn't match exactly, or status value isn't a dropdown label. Fix and repost. |
| Asset Link in Campaign record is broken | Stop the build. Post `/update Tasks Status: Blocked`. Ping Andrew. Wrong video in wrong ad is a real problem. |
| Special Ad Category warning in Ads Manager | Housing isn't selected. Fix in campaign settings before publishing. |
| Ad rejected by Facebook | Flag immediately to Andrew with the rejection reason. Don't republish. |
| `Last Pull Date` on a campaign record is >48h ago | Windsor sync may have failed. Flag to Andrew. (As of 2026-05-10 the Windsor workflow is intentionally inactive — auto-reactivates on first live campaign.) |
| Client record didn't appear after a Won deal | M5 normally fires within 30s and falls back to a 5-min poll. If it's been >10 min, ping Andrew with the deal name. |
| New client `#client-<slug>` channel is private | That's the default since Apr 25. Andrew flips to public after the client is invited as a guest. Don't try to flip it yourself. |
| Retarget/Lead Ad audiences don't exist in Ads Manager | Video Views campaign hasn't accumulated enough viewers yet. Flag the Build task as Blocked — don't proceed without audiences. |
| Bot says `not_in_channel` for a client channel | Bot needs a guest invite to that channel. Ping Andrew (he handles it). |
| The Apr 26 architecture map and an SOP disagree | The SOP wins for VA-facing workflows. The architecture map is the source for system architecture. If they conflict on operational steps, ping `#team-operations` and Andrew will reconcile. |
| Two tasks tell you to do the same thing | Don't act on both. Post in `#team-<client>` and ping Andrew. Duplicate task creation is a workflow bug — don't paper over it. |
| You can't find an SOP linked from a task | Stop. Don't improvise. Post in `#team-<client>`: missing SOP for task `<task-id>`, what should I do? |

## 14. Quiet hours rule

**All automated client-facing notifications fire 8am–6pm ET only.** If you see a system message arrive outside that window — especially anything posted in a `#client-<client>` channel — it's a system issue. Don't act on it. Flag it in `#team-operations` and ping Andrew.

Internal notifications (`#team-operations`, `#team-<client>`, DMs to Andrew) can fire any time — those aren't client-facing. The 8am–6pm rule applies specifically to anything the client could see.

## 15. What to do on Day 1 — concrete

Open these tabs:
1. SmartSuite → Tasks → My Queue.
2. SmartSuite → Onboarding → Onboarding Board.
3. SmartSuite → Clients → Dashboard.
4. Slack → `#team-operations`.
5. Slack → every `#team-<client>` for the 6 active clients.
6. Google Drive → `RequityAI` parent folder.
7. Meta Business Manager → Business settings.

Then:
1. Read the last 24h of `#team-operations` — that's the daily ops briefing + sales brief + any system alerts.
2. Read the last 24h of every `#team-<client>` you're in.
3. In SmartSuite Tasks → My Queue, identify the top task. Read it, open its linked SOP, walk through the work mentally.
4. Open the linked Onboarding record for that task. Find which step it's gated by.
5. **Take the first task on a kickoff call with Andrew.** Don't execute it solo on Day 1 — walk through it with him so you both know the live state matches the SOP.
6. After that call, work the queue normally.

## 16. Glossary

- **AgencyOS** — the operational layer behind RequityAI: SmartSuite + n8n + Slack + Drive + Meta + Windsor, plus the agents.
- **App** — a SmartSuite app (Pipeline, Onboarding, etc.). Each holds one type of record.
- **BOF** — Bottom of Funnel. Lead Ad campaigns. Captures contact details via FB Lead Form.
- **CIA** — Campaign Intelligence Agent. Currently dormant.
- **Close** — Close CRM. Andrew's calling tool. NOT the source of truth for deal stage — Pipeline is.
- **CTA** — Call to Action. For us: "comment OPTIONS" on TOF/MOF, FB Lead Form on BOF.
- **Decision Router** — the n8n workflow that turns CIA decisions into VA tasks. Currently dormant.
- **Lead Ad** — BOF campaign type. Only campaign that captures leads.
- **Lead Centre** — Meta's lead inbox in Business Manager.
- **M2b** — the every-30-min Close → ConvTracker polling workflow. M-F 8am–3:30pm ET.
- **M3** — the Calendly `invitee.created` → Pipeline workflow.
- **M4** — the No-Show → Calendly reschedule workflow.
- **M5** — the Won → Full Client Setup atomic chain (Client + Onboarding + Drive + Slack channels + welcome doc).
- **MOF** — Middle of Funnel. Retarget campaigns.
- **My Queue** — your home view in SmartSuite Tasks. Sorted by priority + due date.
- **n8n** — the automation runtime (`requityai.app.n8n.cloud`). 21 active workflows.
- **NDM** — Non-Decision Maker. A `last_call_outcome` value in ConvTracker, NOT a Pipeline stage.
- **Niche** — REI / Notes / Health / Construction / Other. Drives which video script library M5 delivers.
- **Onboarding** — the SmartSuite app. 18 named steps + 1 master flag. 4 phases.
- **`/update`** — the structured Slack message format that the Sync Agent parses into SmartSuite writes.
- **Pipeline** — the SmartSuite app. 10 `deal_stage` values. Mirror of Close call outcomes.
- **REI** — Real Estate Investor. The default niche.
- **Sync Agent** — the n8n workflow (`8tdPtQWO4qDKEjgq`) that parses `/update` into SmartSuite writes.
- **TOF** — Top of Funnel. Video Views campaigns.
- **VA** — you.
- **Windsor** — Windsor.ai. Pulls FB Ads metrics into SmartSuite Campaigns. Currently inactive (campaign-gated).
- **Won** — Pipeline `deal_stage` value that triggers M5.
- **Quiet hours** — 8am–6pm ET. Client-facing notifications fire only in this window.

---

## Self-test (Day 1 comprehension check)

Answer yes/no. If you can't answer all 10 confidently after reading this manual, re-read the section listed and ask in `#team-<client>` before working a real task.

| # | Question | Section |
|---|---|---|
| 1 | The system holds the state, not me. (Y/N) | §1 |
| 2 | If a task isn't in SmartSuite Tasks → My Queue, it's not a priority. (Y/N) | §2 |
| 3 | I should never post structured `/update` messages in `#client-<client>`. (Y/N) | §5, §6 |
| 4 | Special Ad Category = Housing is non-negotiable on every campaign. (Y/N) | §8 |
| 5 | If the Sync Agent reacts ⚠️, my message had a parse error and I should fix and repost. (Y/N) | §6 |
| 6 | I create retargeting audiences as a separate task. (Y/N — answer should be NO) | §8 |
| 7 | I edit raw videos in Phase 3 as part of my role. (Y/N) | §7 |
| 8 | I should DM Andrew for any question that an SOP could answer. (Y/N — answer should be NO) | §11 |
| 9 | Pipeline has 10 stage values, not 11 (no NDM in Pipeline). (Y/N) | §6, glossary |
| 10 | I post `/update Pipeline` in `#team-operations`, not in a client channel. (Y/N) | §5, §6 |

When you can answer all 10 correctly, you're ready to work the queue.

---

*This manual supersedes the prior `RequityAI_Operator_Guide_V2.docx` for VA use. Andrew keeps the per-app SOPs (`SOPs/SOP_01_Pipeline.md` … `SOP_09_Slack_Communication.md`) for system maintenance — VAs read this manual; Andrew reads both.*
