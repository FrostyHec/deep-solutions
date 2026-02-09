# Commit and PR Conventions

This document describes the commit message and pull request conventions for the `deep-solutions` project.

## Table of Contents
- [Commit Message Format](#commit-message-format)
- [Commit Types](#commit-types)
- [Examples](#examples)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Tools](#tools)
- [Merge Strategy](#merge-strategy)

---

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Structure

| Part | Required | Description |
|------|----------|-------------|
| `type` | ✅ Yes | Category of change (see below) |
| `scope` | ❌ Optional | Module/component affected (e.g., `core`, `api`, `docs`) |
| `subject` | ✅ Yes | Short description (≤50 chars, imperative mood, no period) |
| `body` | ❌ Optional | Detailed explanation (wrap at 72 chars) |
| `footer` | ❌ Optional | Issue references, breaking changes |

---

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(core): add data validation` |
| `fix` | Bug fix | `fix(utils): resolve parsing error` |
| `docs` | Documentation only | `docs(readme): update installation guide` |
| `style` | Code style (formatting, no logic change) | `style: format with ruff` |
| `refactor` | Code refactoring (no new feature, no bug fix) | `refactor(core): simplify data processing` |
| `perf` | Performance improvement | `perf: optimize data loading` |
| `test` | Adding or updating tests | `test(core): add unit tests` |
| `build` | Build system or dependencies | `build: update setuptools` |
| `ci` | CI/CD configuration | `ci: add Python 3.12 to matrix` |
| `chore` | Other changes (maintenance) | `chore: update gitignore` |
| `revert` | Revert a previous commit | `revert: revert "feat: add X"` |

---

## Examples

### Simple commit
```
feat(core): add dynamic batch sampler
```

### Commit with body
```
fix(cli): handle config path with tilde expansion

The CLI was not expanding ~ in file paths, causing
FileNotFoundError when users specified paths like
~/.config/app.yaml

Closes #55
```

### Breaking change
```
feat(api): change return type of process()

BREAKING CHANGE: process() now returns a dataclass instead of dict.
Users should update their code to access fields as attributes.

Migration:
- Before: result["value"]
- After: result.value
```

### Multiple scopes
```
feat(core,api): add streaming support
```

---

## Pull Request Guidelines

### PR Title Format

PR titles should follow the same format as commit messages:

```
<type>(<scope>): <description>
```

**Examples:**
- `feat(core): add data validation pipeline`
- `fix(utils): resolve edge case in parser`
- `docs: update API documentation`

### PR Description

Use the provided PR template which includes:
- Description of changes
- Type of change
- Related issues
- Checklist

### Requirements for Merge

1. **All CI checks must pass**
   - Lint check
   - Type check
   - All tests pass
   - Build check

2. **At least one approval (LGTM)**

3. **No merge conflicts**

---

## Tools

### Commitizen

We use [Commitizen](https://commitizen-tools.github.io/commitizen/) for:
- Interactive commit message creation
- Commit message validation
- Automatic CHANGELOG generation

#### Usage

```bash
# Interactive commit (recommended)
cz commit
# or
cz c

# Check if last commit message is valid
cz check --rev-range HEAD

# Generate/update CHANGELOG
cz changelog
```

### Pre-commit

Pre-commit hooks automatically validate commit messages:

```bash
# Install hooks (one-time setup)
pre-commit install --hook-type commit-msg

# Run all hooks manually
pre-commit run --all-files
```

### Git Commit Template

A commit message template is provided at `.gitmessage`. To use it:

```bash
# Set for this repository only
git config commit.template .gitmessage

# Or set globally
git config --global commit.template ~/.gitmessage
```

---

## Merge Strategy

We use **Squash and Merge** for most PRs:

- Keeps `main` branch history clean and linear
- Each PR becomes a single atomic commit
- PR title becomes the commit message

### When to use other strategies

| Strategy | Use Case |
|----------|----------|
| **Squash and Merge** | Most PRs (default) |
| **Merge Commit** | Large PRs where history matters |
| **Rebase and Merge** | Small PRs that should remain separate |

---

## CHANGELOG Generation

CHANGELOG is automatically generated from commit messages:

- `feat` → **Added** section
- `fix` → **Fixed** section
- `BREAKING CHANGE` → **Breaking Changes** section

To generate/update CHANGELOG:

```bash
cz changelog
```

---

## Related Documentation

- [Code Standards](./en-US_code_standards.md)
- [Developer Guide](./en-US_developers_guide.md)
- [Language Guidelines](./en-US_language_guidelines.md)
