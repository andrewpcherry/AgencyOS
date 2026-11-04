# Gulf Coast Contractors — website preview

Preview build of the new Gulf Coast Contractors website, on the same foundation as the
Texas Roof Guardians build (layout, engine, conversation-preview chat, review marquee,
AI receptionist demo). The funnel lives in the companion repo `gc-funnel`.

Content, photos, reviews, licenses and contact details come from gccontractors.net
(pulled 2026-11-04). Google rating (4.9 / 65 reviews) is from RequityAI's prospect
research sheet.

## Before launch
- Confirm the Google rating/review count against the live Google Business Profile.
- Confirm hours (their site lists "MWF 8–6") and whether FORTIFIED Roof is a current certification.
- Replace the hero still with their drone video (`DJI_0397.mp4` on gccontractors.net) if wanted.
- Create GC's own GoHighLevel sub-account, then wire the contact form and funnel to it and set
  `GHL_CHAT_WIDGET_ID` in `assets/site.js`. Until then all forms are preview-only and send nothing.
- Legal pages (privacy, terms, SMS terms) are drafts adapted from a template: GC must review them.
- Remove `<meta name="robots" content="noindex">` and update `robots.txt` when going live.
