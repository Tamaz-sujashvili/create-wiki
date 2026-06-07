#!/usr/bin/env python3
"""Lint an LLM Wiki directory. Exit 0 if no errors, 1 if issues found."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

WIKI_DIRS = ("entities", "concepts", "comparisons", "queries")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
REQUIRED_FIELDS = ("title", "created", "updated", "type", "tags", "sources")


@dataclass
class Issue:
    severity: str  # error, warn, info
    category: str
    message: str


@dataclass
class LintReport:
    issues: list[Issue] = field(default_factory=list)

    def add(self, severity: str, category: str, message: str) -> None:
        self.issues.append(Issue(severity, category, message))


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    block = match.group(1)
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def slug_from_path(path: Path, wiki: Path) -> str:
    rel = path.relative_to(wiki)
    return str(rel.with_suffix("")).replace(os.sep, "/")


def wiki_page_exists(target: str, wiki: Path, pages: set[str]) -> bool:
    target = target.strip()
    if target in pages:
        return True
    # Allow linking by filename without directory
    basename = Path(target).stem
    return any(p.endswith(f"/{basename}") or p == basename for p in pages)


def load_taxonomy(schema_path: Path) -> set[str]:
    if not schema_path.exists():
        return set()
    text = schema_path.read_text(encoding="utf-8")
    tags: set[str] = set()
    in_taxonomy = False
    for line in text.splitlines():
        if line.strip().startswith("## Tag Taxonomy"):
            in_taxonomy = True
            continue
        if in_taxonomy and line.startswith("## "):
            break
        if in_taxonomy and line.strip().startswith("- "):
            # e.g. "- Models: model, architecture, benchmark"
            parts = line.split(":", 1)
            if len(parts) == 2:
                for tag in parts[1].split(","):
                    tags.add(tag.strip())
    return tags


def collect_wiki_pages(wiki: Path) -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for dirname in WIKI_DIRS:
        base = wiki / dirname
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            pages[slug_from_path(path, wiki)] = path
    return pages


def extract_index_slugs(index_text: str) -> set[str]:
    slugs: set[str] = set()
    for match in WIKILINK_RE.finditer(index_text):
        slugs.add(match.group(1).strip())
    return slugs


def sha256_body(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    body = text[match.end() :] if match else text
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def lint_wiki(wiki: Path) -> LintReport:
    report = LintReport()
    wiki = wiki.resolve()

    if not wiki.is_dir():
        report.add("error", "structure", f"Wiki path does not exist: {wiki}")
        return report

    for required in ("SCHEMA.md", "index.md", "log.md"):
        if not (wiki / required).exists():
            report.add("error", "structure", f"Missing required file: {required}")

    pages = collect_wiki_pages(wiki)
    page_slugs = set(pages.keys())
    taxonomy = load_taxonomy(wiki / "SCHEMA.md")

    inbound: dict[str, int] = {slug: 0 for slug in page_slugs}
    outbound: dict[str, list[str]] = {slug: [] for slug in page_slugs}

    for slug, path in pages.items():
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        missing = [f for f in REQUIRED_FIELDS if f not in fm]
        if missing:
            report.add("error", "frontmatter", f"{slug}: missing fields {missing}")

        if fm.get("type") and fm["type"] not in {
            "entity",
            "concept",
            "comparison",
            "query",
            "summary",
        }:
            report.add("warn", "frontmatter", f"{slug}: unknown type '{fm['type']}'")

        if taxonomy and "tags" in fm:
            for tag in re.findall(r"[\w-]+", fm["tags"]):
                if tag not in taxonomy and tag not in {"tags"}:
                    report.add("warn", "tags", f"{slug}: tag '{tag}' not in SCHEMA taxonomy")

        line_count = len(text.splitlines())
        if line_count > 200:
            report.add("info", "size", f"{slug}: {line_count} lines (consider splitting)")

        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).strip()
            outbound[slug].append(target)
            if wiki_page_exists(target, wiki, page_slugs):
                for existing in page_slugs:
                    if existing == target or existing.endswith(f"/{Path(target).stem}"):
                        inbound[existing] = inbound.get(existing, 0) + 1
            else:
                report.add("error", "broken-link", f"{slug}: broken wikilink [[{target}]]")

        if len(outbound[slug]) < 2:
            report.add("warn", "cross-ref", f"{slug}: fewer than 2 outbound wikilinks")

    for slug, count in inbound.items():
        if count == 0:
            report.add("warn", "orphan", f"{slug}: no inbound wikilinks")

    index_path = wiki / "index.md"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        indexed = extract_index_slugs(index_text)
        for slug in page_slugs:
            basename = Path(slug).name
            if slug not in indexed and basename not in indexed:
                report.add("warn", "index", f"{slug}: not listed in index.md")

    raw_base = wiki / "raw"
    if raw_base.exists():
        for path in raw_base.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if "sha256" in fm:
                actual = sha256_body(text)
                if actual and actual != fm["sha256"].strip():
                    rel = path.relative_to(wiki)
                    report.add(
                        "warn",
                        "source-drift",
                        f"{rel}: sha256 mismatch (source may have changed)",
                    )

    log_path = wiki / "log.md"
    if log_path.exists():
        entries = len(re.findall(r"^## \[", log_path.read_text(encoding="utf-8"), re.MULTILINE))
        if entries > 500:
            report.add("info", "log", f"log.md has {entries} entries (rotate recommended)")

    return report


def print_report(report: LintReport) -> int:
    order = {"error": 0, "warn": 1, "info": 2}
    issues = sorted(report.issues, key=lambda i: (order.get(i.severity, 9), i.category, i.message))

    if not issues:
        print("OK — no issues found")
        return 0

    counts = {"error": 0, "warn": 0, "info": 0}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
        print(f"[{issue.severity.upper():5}] {issue.category}: {issue.message}")

    print(
        f"\nSummary: {counts.get('error', 0)} errors, "
        f"{counts.get('warn', 0)} warnings, {counts.get('info', 0)} info"
    )
    return 1 if counts.get("error", 0) or counts.get("warn", 0) else 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint an LLM Wiki directory")
    parser.add_argument(
        "wiki_path",
        nargs="?",
        default=os.environ.get("WIKI_PATH", os.path.expanduser("~/wiki")),
        help="Path to wiki root (default: $WIKI_PATH or ~/wiki)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = lint_wiki(Path(args.wiki_path))
    return print_report(report)


if __name__ == "__main__":
    sys.exit(main())
