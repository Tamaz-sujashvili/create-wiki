# Manual Lint Checks

The bundled `scripts/lint-wiki.py` handles structural checks. The agent should also perform these manual reviews during a full lint:

## Stale Content

Pages whose `updated` date is >90 days older than the most recent source mentioning the same entities.

## Contradictions

Pages on the same topic with conflicting claims. Surface all pages with:
- `contested: true` in frontmatter
- `contradictions: [page-slug]` in frontmatter

Look for pages sharing tags/entities but stating different facts.

## Quality Signals

List pages with `confidence: low`. Flag pages citing only one source with no confidence field — candidates for corroboration or demotion to `confidence: medium`.

## Severity Order

Report grouped by severity:

1. Broken wikilinks (error)
2. Orphan pages (warning)
3. Source drift (warning)
4. Contested pages (warning)
5. Stale content (info)
6. Tag drift, oversized pages, style issues (info)
