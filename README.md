# Create Wiki Skill

> Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
> No database. No special tooling. Just markdown + an AI agent.

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — an LLM agent acts as a **librarian**, not just a chatbot. Compile knowledge once, cross-reference it, and keep it current.

## Why not RAG?

| Traditional RAG | LLM Wiki |
|---|---|
| Re-embeds every query | Knowledge compiled once |
| No cross-references | `[[wikilinks]]` between pages |
| No history awareness | Tracks what's known vs. unknown |
| Contradictions invisible | Frontmatter flags `contested: true` |
| Stateless per query | Stateful, growing knowledge base |

## Quick Start

```bash
# One-line install (Cursor)
curl -fsSL https://raw.githubusercontent.com/Tamaz-sujashvili/create-wiki/main/scripts/install.sh | bash

# Or clone and install locally
git clone https://github.com/Tamaz-sujashvili/create-wiki.git
cd create-wiki
./scripts/install.sh cursor   # or: claude | codex | hermes | all
```

Set your wiki path:

```bash
export WIKI_PATH="$HOME/wiki"
```

Then ask your agent:

> "Create a wiki about AI/ML research"

The agent scaffolds the structure, writes `SCHEMA.md`, and asks what to ingest first.

## Installation

### Cursor

```bash
./scripts/install.sh cursor
# Installs to ~/.cursor/skills/create-wiki-skill/
```

### Claude Code

```bash
./scripts/install.sh claude
# Installs to ~/.claude/skills/create-wiki-skill/
```

### Codex

```bash
./scripts/install.sh codex
# Installs to ~/.codex/skills/create-wiki-skill/
```

### Hermes Agent

```bash
./scripts/install.sh hermes
# Installs to ~/.hermes/skills/research/create-wiki-skill/
```

### Manual

Copy the entire `create-wiki-skill/` folder into your agent's skills directory. The only required file is `SKILL.md`; bundled scripts and templates are optional but recommended.

## Architecture

```
wiki/
├── SCHEMA.md           # Conventions, structure, tag taxonomy
├── index.md            # Sectioned content catalog
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

## Core Operations

### Ingest

Give the agent a URL, PDF, or text. It captures the raw source (with SHA256 drift detection), cross-references existing pages, creates/updates entity and concept pages with `[[wikilinks]]`, and updates index and log.

### Query

Ask a question about your wiki's domain. The agent reads the index, finds relevant pages, and synthesizes an answer citing its sources.

### Lint

Ask the agent to audit the wiki, or run the bundled linter:

```bash
python3 scripts/lint-wiki.py "$WIKI_PATH"
```

Checks: orphan pages, broken wikilinks, stale content, contradictions, tag drift, source integrity, and more.

## Skill Package Contents

```
create-wiki-skill/
├── SKILL.md              # Main skill instructions
├── README.md             # This file
├── templates/            # SCHEMA, index, log templates for new wikis
├── examples/             # Example workflows
├── reference/            # Obsidian sync, lint checks, related tools
└── scripts/
    ├── install.sh        # Multi-platform installer
    └── lint-wiki.py      # Wiki health checker
```

## Requirements

- Any LLM agent that can follow procedural skills (Cursor, Claude Code, Codex, Hermes Agent, etc.)
- `WIKI_PATH` environment variable (defaults to `~/wiki`)
- Python 3.8+ for the lint script (optional)

## Use Cases

- **AI/ML research** — papers, models, benchmarks, relationships
- **Competitive intelligence** — companies, products, people
- **Personal knowledge management** — Obsidian vault curated by your agent
- **Technical documentation** — living docs that grow with your project
- **Market intelligence** — financial data, sector analysis, macro trends

## Related

- [llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) — Node.js CLI for batch compiles
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — agent framework with native skill support
- [Karpathy's original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## License

MIT — see [LICENSE](LICENSE)
