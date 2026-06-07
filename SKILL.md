---
name: create-wiki-skill
description: >-
  Build and maintain a persistent, compounding knowledge base as interlinked
  markdown files (Karpathy's LLM Wiki pattern). Use when the user asks to
  create, start, ingest into, query, lint, or audit a wiki or knowledge base;
  when adding sources (URLs, PDFs, notes) to a research vault; or when working
  with WIKI_PATH, SCHEMA.md, index.md, or Obsidian wikilinks in a research context.
---

# Create Wiki Skill

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike traditional RAG, the wiki compiles knowledge once and keeps it current.
Cross-references exist. Contradictions are flagged. Synthesis reflects everything ingested.

**Division of labor:** The human curates sources and directs analysis. The agent
summarizes, cross-references, files, and maintains consistency.

## Wiki Location

Resolve the wiki root at session start:

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

Set `WIKI_PATH` in the environment, project `.env`, or agent config. Default: `~/wiki`.

The wiki is a directory of markdown files — open in Obsidian, VS Code, or any editor.

## Architecture

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, tag taxonomy
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Chronological action log (append-only)
├── raw/                # L1: Immutable source material
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   └── assets/
├── entities/           # L2: People, orgs, products, models
├── concepts/           # L2: Topics and ideas
├── comparisons/        # L2: Side-by-side analyses
└── queries/            # L2: Filed query results
```

- **L1 — Raw Sources:** Immutable after ingestion. Read only.
- **L2 — The Wiki:** Agent-owned markdown with frontmatter and `[[wikilinks]]`.
- **L3 — The Schema:** `SCHEMA.md` defines structure and tag taxonomy.

## Agent Tools (platform-agnostic)

Map these operations to whatever tools the host agent provides:

| Operation | Use |
|-----------|-----|
| Read wiki files | Read tool / `cat` |
| Write wiki files | Write / StrReplace tools |
| Search content | Grep, Glob, SemanticSearch, or `rg` |
| Fetch URLs | WebFetch, curl, or browser tools |
| Fetch PDFs | PDF skill or download + extract |
| Compute SHA256 | Shell: `python3 -c "import hashlib; ..."` |
| Lint wiki | Run `scripts/lint-wiki.py "$WIKI"` |

## Resuming an Existing Wiki (CRITICAL)

Before ingest, query, or lint in any session:

1. Read `SCHEMA.md` — domain, conventions, tag taxonomy
2. Read `index.md` — what pages exist
3. Read the last 20–30 entries of `log.md` — recent activity

Only then proceed. This prevents duplicate pages, missed cross-references, and repeated work.

For wikis with 100+ pages, also search for the topic before creating new pages.

## Initializing a New Wiki

When the user asks to create or start a wiki:

1. Resolve wiki path (`$WIKI_PATH`, ask user, or default `~/wiki`)
2. Create the directory structure (all `raw/` subdirs, `entities/`, `concepts/`, `comparisons/`, `queries/`, `_archive/`)
3. Ask what domain the wiki covers — be specific
4. Write `SCHEMA.md` from [templates/SCHEMA.md](templates/SCHEMA.md), customized to the domain
5. Write `index.md` from [templates/index.md](templates/index.md)
6. Write `log.md` from [templates/log.md](templates/log.md) with a creation entry
7. Confirm ready and suggest first sources to ingest

## Core Operations

### 1. Ingest

When the user provides a source (URL, file, paste):

**① Capture the raw source**
- URL → fetch content, save to `raw/articles/`
- PDF → extract text, save to `raw/papers/`
- Pasted text → save to the appropriate `raw/` subdirectory
- Name descriptively: `raw/articles/karpathy-llm-wiki-2026.md`
- Add raw frontmatter (`source_url`, `ingested`, `sha256` of body below frontmatter)
- On re-ingest of the same URL: recompute sha256 — skip if identical, flag drift if changed

**② Discuss takeaways** with the user (skip in automated/cron contexts)

**③ Check what exists** — read `index.md` and search for mentioned entities/concepts

**④ Write or update wiki pages**
- New pages only if they meet Page Thresholds in `SCHEMA.md`
- Update existing pages; bump `updated` date; follow Update Policy for conflicts
- Every page links to ≥2 other pages via `[[wikilinks]]`; ensure backlinks
- Tags only from `SCHEMA.md` taxonomy
- Provenance markers on multi-source pages: `^[raw/articles/source.md]`
- Set `confidence: medium|low` for weak or single-source claims

**⑤ Update navigation**
- Add new pages to `index.md` (correct section, alphabetical)
- Update header counts and dates in `index.md`
- Append to `log.md` with every file created or updated

**⑥ Report what changed** — list all files touched

A single source often updates 5–15 pages. That compounding is intentional.

### 2. Query

When the user asks a question about the wiki's domain:

1. Read `index.md` to find relevant pages
2. For 100+ page wikis, also search `.md` files for key terms
3. Read relevant pages
4. Synthesize an answer citing wiki pages: "Based on [[page-a]] and [[page-b]]..."
5. File substantial answers to `queries/` or `comparisons/` if worth keeping
6. Log the query and whether it was filed

### 3. Lint

When the user asks to lint, audit, or health-check the wiki:

Run the bundled linter first:

```bash
python3 scripts/lint-wiki.py "$WIKI"
```

Then manually verify anything the script cannot judge (contradictions, stale content).
The script checks:

1. Orphan pages (no inbound wikilinks)
2. Broken wikilinks
3. Index completeness
4. Frontmatter validation and tag taxonomy compliance
5. Source SHA256 drift in `raw/`
6. Oversized pages (>200 lines)
7. Log rotation need (>500 entries)

Report findings by severity: broken links > orphans > source drift > contested pages > stale content > style issues.

Append to `log.md`: `## [YYYY-MM-DD] lint | N issues found`

See [reference/lint-checks.md](reference/lint-checks.md) for manual checks the script does not cover.

## Working with the Wiki

### Searching

```bash
# By content
rg "transformer" "$WIKI" --glob "*.md"

# By tag in frontmatter
rg "tags:.*alignment" "$WIKI/entities" "$WIKI/concepts" --glob "*.md"

# Recent activity
tail -30 "$WIKI/log.md"
```

### Bulk Ingest

1. Read all sources first
2. Identify all entities and concepts across sources
3. One search pass for existing pages
4. Create/update pages in one pass
5. Update `index.md` once
6. Single log entry for the batch

### Archiving

1. Move page to `_archive/` preserving path (e.g. `_archive/entities/old-page.md`)
2. Remove from `index.md`
3. Replace inbound wikilinks with plain text + "(archived)"
4. Log the archive action

### Obsidian Integration

The wiki works as an Obsidian vault: `[[wikilinks]]`, Graph View, YAML frontmatter, Dataview.

Set attachment folder to `raw/assets/`. For headless server sync, see [reference/obsidian-sync.md](reference/obsidian-sync.md).

## Pitfalls

- **Never modify `raw/` after ingestion** — corrections go in wiki pages
- **Always orient first** — SCHEMA + index + recent log every session
- **Always update index.md and log.md** — they are the navigational backbone
- **Don't create pages for passing mentions** — follow Page Thresholds
- **Don't create isolated pages** — minimum 2 outbound wikilinks each
- **Frontmatter is required** on every wiki page
- **Tags must come from taxonomy** — add to SCHEMA.md first
- **Keep pages scannable** — split pages over 200 lines
- **Ask before mass-updating** — confirm if ingest touches 10+ existing pages
- **Handle contradictions explicitly** — note both claims, mark in frontmatter, flag for review

## Additional Resources

- Schema template: [templates/SCHEMA.md](templates/SCHEMA.md)
- Index template: [templates/index.md](templates/index.md)
- Log template: [templates/log.md](templates/log.md)
- Example workflow: [examples/ai-research-wiki.md](examples/ai-research-wiki.md)
- Manual lint checks: [reference/lint-checks.md](reference/lint-checks.md)
- Obsidian headless sync: [reference/obsidian-sync.md](reference/obsidian-sync.md)
- Related tools: [reference/related-tools.md](reference/related-tools.md)
