# Example: AI/ML Research Wiki

This example shows how to create a wiki for tracking AI/ML research papers, models, labs, and people.

## 1. Initialize

```bash
export WIKI_PATH="$HOME/ai-research-wiki"
```

Then tell your agent: *"Create a wiki for AI/ML research"*

The agent will:
- Ask about your specific domain focus
- Write a customized `SCHEMA.md` with AI/ML tag taxonomy
- Create the directory structure
- Initialize `index.md` and `log.md`

## 2. Ingest a Paper

Share an arxiv link: *"Add this paper: https://arxiv.org/abs/2303.08774"*

The agent will:
- Save the paper to `raw/papers/`
- Extract key findings, methods, results
- Create/update entity pages for authors and organizations
- Create/update concept pages for techniques
- Cross-link everything with `[[wikilinks]]`
- Update `index.md` and `log.md`

## 3. Query Your Wiki

*"What do I know about Mixture of Experts models?"*

The agent will:
- Scan the index and search content
- Read relevant pages (models, papers, comparisons)
- Synthesize a response citing specific wiki pages
- Optionally file the answer as a `queries/` page

## 4. Run a Health Check

*"Lint my wiki"*

Or run the script directly:

```bash
SKILL_DIR="$HOME/.cursor/skills/create-wiki-skill"  # directory containing SKILL.md
python3 "$SKILL_DIR/scripts/lint-wiki.py" "$WIKI_PATH"
```

The agent reports:
- Broken wikilinks
- Orphan pages (no inbound links)
- Stale content (outdated >90 days)
- Contradictions between sources
- Tag drift (tags not in taxonomy)
