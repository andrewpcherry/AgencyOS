# Google Drive Inventory

**Generated:** 2026-05-09 via Drive MCP probe
**Source of truth:** Live Google Drive search

## RequityAI parent folder

- **Folder ID:** `1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R` ✅ matches state doc
- **Owner:** andrew@requityai.com
- **Created:** 2026-04-09
- **Last modified:** 2026-04-28
- **URL:** https://drive.google.com/drive/folders/1DB_qI24c3DtWd_fSabtiUNYH27NV-C2R

## Status

Parent folder confirmed live and accessible. Per-client subfolder enumeration requires deeper probe (need to list contents). Initial finding: parent exists where state doc claims it does, with the same ID.

## Per-client subfolder check — TBD

A follow-up probe will list the immediate children of the RequityAI folder to confirm:
- All 6 active clients have subfolders (Real Vantage, Quick Home Buyers, Ritsel Notes, First Integrity, Next Journey Homes, Bayrock Home Buyers)
- Each subfolder contains both `Raw Video/` and `Ad Creative/` directories per SOP_05 standard
- The script library + niche-specific video brief docs referenced by M5 (`SCRIPT_DOC_BY_NICHE` map per memory) exist and are accessible

## Findings vs current docs

**1. Folder ID matches state doc — parent layer is good.** No drift.
**2. Need full subfolder audit** to verify the 6 active clients each have correctly-structured subfolders. The 2 newer clients (Next Journey, Bayrock — created Apr 25) need verification; M5 Deal Won workflow is supposed to auto-create them.
