# Contributing to Create Wiki Skill

Thanks for helping improve the skill. This repo ships a portable agent skill (`SKILL.md`) plus optional scripts and templates.

## Repository naming

- **GitHub repo slug:** `create-wiki` — https://github.com/Tamaz-sujashvili/create-wiki
- **Skill directory name:** `create-wiki-skill` (installed under your agent's skills folder)

## Development setup

```bash
git clone https://github.com/Tamaz-sujashvili/create-wiki.git
cd create-wiki
./scripts/install.sh local /tmp/create-wiki-skill-test
```

Or install to your agent without cloning:

```bash
curl -fsSL https://raw.githubusercontent.com/Tamaz-sujashvili/create-wiki/main/scripts/install.sh | bash -s -- local /tmp/create-wiki-skill-test
```

## Testing the lint script

Requires Python 3.8+.

```bash
# Human-readable output
python3 scripts/lint-wiki.py /path/to/wiki

# JSON output for agents
python3 scripts/lint-wiki.py /path/to/wiki --json

# Version check
python3 scripts/lint-wiki.py --version
```

Point it at an existing wiki (or a fresh one created by the skill) and verify checks run without errors.

## Testing the installer

```bash
bash -n scripts/install.sh
./scripts/install.sh --version
./scripts/install.sh local /tmp/create-wiki-skill-test

# Verify .git was not copied
test ! -d /tmp/create-wiki-skill-test/.git && echo "OK: no .git"
```

## Submitting changes

1. Fork the repo and create a feature branch.
2. Keep changes focused — bug fixes, docs, and small improvements are welcome.
3. Run `bash -n scripts/install.sh` and `python3 scripts/lint-wiki.py --version` before opening a PR.
4. Open a pull request against `main` with a short description of what changed and why.

## What to contribute

- Bug fixes in `scripts/lint-wiki.py` or `scripts/install.sh`
- Clearer skill instructions in `SKILL.md`
- Additional examples in `examples/`
- Reference docs in `reference/`

Avoid drive-by refactors unrelated to your change.
