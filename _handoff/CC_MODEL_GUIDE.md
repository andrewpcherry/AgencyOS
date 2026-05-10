# Claude Code — Which Model for What (AgencyOS Project)

**Last updated:** 2026-05-09
**Purpose:** A pinned reference so you don't have to think about model selection mid-task.
**Switch model in CC:** type `/model` in chat → pick from the menu.

---

## The single rule

**Default to Sonnet.** Switch up to **Opus** only when output quality is the headline deliverable. Switch down to **Haiku** only when speed and volume matter more than quality.

If you only remember one thing: **Sonnet is right 80% of the time.**

---

## The three current Claude tiers

| Tier | Strength | Weakness | Cost vs Sonnet | When to use |
|---|---|---|---|---|
| **Haiku 4.5** | Fast, cheap, great at structured tasks | Shallow on hard reasoning, can miss nuance | ~0.2x | Bulk operations, classification, quick lookups |
| **Sonnet 4.6** | Balanced, smart, excellent default | Not quite Opus on truly novel reasoning | 1x | Almost everything |
| **Opus 4.6** (or 4.7+ if newer) | Best reasoning, deepest synthesis | Slow, expensive, eats quota fast | ~5x | Headline deliverables, ambiguous problems |

Note: model names update over time. Anthropic ships newer versions periodically. Whatever's labeled top-tier in `/model` is what was Opus.

---

## AgencyOS project — phase-by-phase

This is your specific roadmap. Open it when you start a CC session.

| Phase / Task | Model | Why |
|---|---|---|
| **Phase 1** — Live API probes (raw data dumps) | Sonnet | Mechanical fetching + JSON parsing. Sonnet is fine. |
| **Phase 2** — Reconciliation (compare docs vs live truth) | Sonnet | Pattern-matching across structured data. Already proven — CC ran Phase 2 on Sonnet and produced the M1-M28 register cleanly. |
| **Phase 3a** — SOP markdown patches (M1-M28 fixes) | Sonnet | Targeted edits with clear instructions. |
| **Phase 3b** — Master state doc rewrite | Sonnet | Editing a doc against an audit register. |
| **Phase 3c** — n8n workflow cleanup (rename, deactivate, tag) | Sonnet | Mechanical, well-bounded by the green/yellow/red rails. |
| **Phase 3d** — Architecture map rewrite (~5 sections) | Sonnet | If reasoning gets ambiguous, switch up. Otherwise Sonnet. |
| **Phase 3e** — Sync Agent parser update (vocabulary swap) | Sonnet | Deterministic JSON edit. Sonnet handles it. |
| **🟢 VA Plug-and-Play Operator Manual write** | **OPUS** | **The only place Opus genuinely earns its keep on this project.** Synthesizing 14+ docs + live audit findings + your operator memory into a single ~3,000-word manual that VAs will read every day. Quality bar is high. Pay the premium. |

---

## Adjacent / non-CC tasks (using me, Cowork, or other Claude tools)

| Task | Model | Why |
|---|---|---|
| Daily ops briefing (read Slack + Calendly + Close) | Sonnet | Standard summarization with context. |
| Lead enrichment — bulk classification of inbound leads | Haiku | High volume, clear criteria, speed > nuance. |
| Drafting a single client follow-up email | Sonnet | Quality matters but not headline-quality. |
| Strategic discussion ("Path A vs B for new feature") | Opus | Real ambiguity, want best reasoning. |
| Slack message drafts ("write a quick reply to X") | Sonnet (or Haiku for speed) | Simple work. |
| Reading + summarizing a long document | Sonnet | Default. |
| Account research (deep dive on a target client) | Sonnet → Opus if surface-level isn't enough | Start cheap. |
| Debugging a tough bug Sonnet keeps missing | Bump to Opus after 2-3 Sonnet fails | Cost makes sense once Sonnet has demonstrated it can't crack it. |

---

## Practical signals to switch UP (Sonnet → Opus)

- Sonnet's output is shallow, generic, or just wrong, on a question that has a real answer
- The reasoning is genuinely ambiguous (multiple valid paths, no clear right one)
- The output is going to be read 100+ times by other people (manual, public doc, customer-facing copy)
- You've tried Sonnet 2-3 times and it's not getting closer

## Practical signals to switch DOWN (Sonnet → Haiku)

- You're processing high volume (50+ items) and per-item quality doesn't need to be deep
- It's a quick fact lookup or classification
- You're hitting your Pro / Max plan quota and need to stretch the runway
- The task is genuinely simple (extract these 3 fields, format as a list)

## Practical signals to switch DOWN further (Sonnet → cheaper Sonnet model)

- Anthropic ships smaller-Sonnet variants periodically — check `/model` for what's available
- Use them when Sonnet is overkill but Haiku is too shallow

---

## Cost / quota awareness

- Pro plan: monthly message quota; Opus messages count more than Sonnet messages
- Max plan: higher quota but same dynamic — Opus burns it ~5x faster
- A 4-hour CC session entirely on Opus can exhaust your daily quota in some plans
- Defaulting to Sonnet keeps your runway long; saving Opus for the headline deliverable means you actually have quota when you need it

---

## How to switch in Claude Code

In the CC chat, type:

```
/model
```

A picker shows current available models. Select with arrow keys + Enter.

You can switch mid-session — the change applies to the next message you send.

---

## TL;DR cheat-sheet (the only thing you really need)

```
Default                   → Sonnet
Bulk / fast / cheap       → Haiku
VA Operator Manual write  → Opus
Strategic decision        → Opus
Sonnet keeps failing      → Opus
```

That's the entire decision tree.

---

## Layered view (added 2026-05-09 after CC pushed back)

CC argued — correctly — that this isn't "use one model" but "use the right model for each LAYER" of the system. Three layers:

**Layer 1 — CC itself (the audit operator)**
- Phase 2 reconciliation = **Opus** (1M context holds the full doc set + raw JSON dumps + parser + register without compaction)
- Phase 3a–c (SOP patches, master state rewrite, n8n cleanup) = **Sonnet** (mechanical edits, bounded per item, save the Opus quota)
- Phase 3d (architecture map rewrite) = **Sonnet** first, **Opus** if reasoning gets ambiguous
- Phase 3e (VA Operator Manual) = **Opus** (headline deliverable, full synthesis)

**Layer 2 — n8n agent workflows on cron**
- Campaign Intelligence Agent = **Haiku** (sized correctly; upgrade to Sonnet only if Cut/Keep/Retarget decisions show quality issues post-launch)
- Slack Ops Supervisor = **Haiku** (extraction/decision on health checks)
- SmartSuite Sync Agent = **Haiku** (parser is mostly deterministic JS; LLM step is small)

**Layer 3 — Routine workflow Anthropic calls**
- Default = **Haiku** (extraction tasks, classifications, simple decisions)
- Upgrade only with concrete signal that Haiku is missing things

**Quota discipline:** sustaining Opus across all of Phase 3 mechanical work will exhaust your daily quota on Pro plan, faster on shorter Max windows. Switching to Sonnet for 3a-c keeps you operational through the whole mission.
