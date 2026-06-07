# Related Tools

## llm-wiki-compiler

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) is a Node.js CLI that compiles sources into a concept wiki with the same Karpathy inspiration. It is Obsidian-compatible.

| | Create Wiki Skill | llm-wiki-compiler |
|---|---|---|
| Page creation | Agent judgment, in the loop | Batch CLI compile |
| Best for | Ongoing curation, contradictions, confidence signals | Scheduled compile of a source directory |
| Corpus size | Scales with agent context | Tuned for smaller corpora |

Use this skill for agent-in-the-loop curation. Use llm-wiki-compiler for batch compile pipelines.

## Karpathy's Original Pattern

[Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the original inspiration.

## Hermes Agent

[Hermes Agent](https://github.com/NousResearch/hermes-agent) — agent framework with native skill support. Load with `skill_view(name="create_wiki_skill")` after installing to `~/.hermes/skills/research/create-wiki-skill/`.
