# Example: Competitive Intelligence Wiki

This example shows how to build a startup dossier wiki for tracking competitors, products, funding, and market positioning.

## 1. Initialize

```bash
export WIKI_PATH="$HOME/competitive-intel-wiki"
```

Then tell your agent: *"Create a wiki for competitive intelligence on B2B SaaS project management tools"*

The agent will:
- Ask which competitors and market segment to focus on
- Write a customized `SCHEMA.md` with tags like `competitor`, `product`, `pricing`, `funding`, `gtm`
- Scaffold `raw/`, `entities/`, `concepts/`, `comparisons/`, `queries/`, and `_archive/`
- Initialize `index.md` and `log.md`

## 2. Ingest a Competitor Profile

Share a source: *"Add this Crunchbase profile and their latest pricing page for Acme Corp"*

The agent will:
- Save fetched content to `raw/articles/` (web pages) or `raw/papers/` (PDF reports)
- Create or update `entities/acme-corp.md` (company dossier)
- Create or update `concepts/project-management-market.md` if relevant
- Add a `comparisons/acme-vs-incumbent.md` page when you have multiple players
- Cross-link products, founders, investors, and pricing tiers with `[[wikilinks]]`
- Update `index.md` and append to `log.md`

## 3. Query Your Wiki

*"How does Acme Corp's pricing compare to what we know about IncumbentCo?"*

The agent will:
- Read `index.md` and search entity/comparison pages
- Synthesize pricing tiers, packaging, and positioning
- Cite wiki pages: "Based on [[entities/acme-corp]] and [[comparisons/acme-vs-incumbent]]..."
- Optionally file the answer under `queries/pricing-comparison-2026.md`

## 4. Run a Health Check

*"Lint my competitive intel wiki"*

Resolve the lint script relative to this skill's install directory (the folder containing `SKILL.md`):

```bash
SKILL_DIR="$(dirname "$(find ~/.cursor/skills -name SKILL.md -path '*/create-wiki-skill/*' | head -1)")"
python3 "$SKILL_DIR/scripts/lint-wiki.py" "$WIKI_PATH"
python3 "$SKILL_DIR/scripts/lint-wiki.py" "$WIKI_PATH" --json
```

The agent reports:
- Broken wikilinks between competitor pages
- Orphan dossiers with no inbound references
- Pages missing from `index.md`
- Tag drift (e.g. `competitor` not in SCHEMA taxonomy)
- Source SHA256 drift if a pricing page was re-ingested

## 5. Typical entity pages

| Page type | Example slug | What it tracks |
|-----------|--------------|----------------|
| Company | `entities/acme-corp` | HQ, funding, team, strategy |
| Product | `entities/acme-workspace` | Features, integrations, roadmap signals |
| Person | `entities/jane-founder` | Role, background, public statements |
| Concept | `concepts/usage-based-pricing` | Market pattern across competitors |
| Comparison | `comparisons/acme-vs-incumbent` | Side-by-side feature and pricing matrix |

Keep raw sources immutable; put analysis and synthesis in L2 wiki pages.
