# Code Standards

This document defines the code standards, commit conventions, and Pull Request workflow for the `deep-solutions` project.

## Table of Contents
- [Code Style](#code-style)
- [Language Requirements](#language-requirements)
- [Commit Conventions](#commit-conventions)
- [Pull Request Workflow](#pull-request-workflow)
- [Code Review Requirements](#code-review-requirements)
- [Merge Requirements](#merge-requirements)

---

## Code Style

### Tool Chain

This project uses the following tools to ensure code quality:

| Tool | Purpose | Configuration File |
|------|---------|-------------------|
| **Ruff** | Code formatting + Lint (replaces black/isort/flake8) | `pyproject.toml` |
| **MyPy** | Static type checking | `pyproject.toml` |
| **pytest** | Unit testing | `pyproject.toml` |

### Ruff Configuration

```toml
[tool.ruff]
target-version = "py38"
line-length = 88

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort (import sorting)
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
]
```

### Code Formatting Commands

```bash
# Format code
ruff format src/ tests/

# Check format (no modification)
ruff format --check src/ tests/

# Lint check
ruff check src/ tests/

# Auto-fix lint issues
ruff check --fix src/ tests/
```

### Type Annotation Requirements

All public APIs must have type annotations:

```python
from typing import Optional, List, Dict

def process_data(
    data: List[int],
    options: Optional[Dict[str, str]] = None
) -> List[int]:
    """Process the data.

    Args:
        data: Input data list
        options: Optional configuration options

    Returns:
        Processed data list
    """
    if options is None:
        options = {}
    return data
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of the function.

    More detailed description (if necessary).

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When this exception is raised
    """
    pass
```

---

## Language Requirements

### Source Code

- **All comments and docstrings must be in English**
- No Chinese characters allowed in source code
- See [Language Guidelines](./language_guidelines.md) for details

### Documentation

- English documentation is required
- Chinese translations are recommended but optional
- English is always the source of truth

---

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(core): add data validation` |
| `fix` | Bug fix | `fix(utils): resolve parsing error` |
| `docs` | Documentation only | `docs(readme): update installation guide` |
| `style` | Code style (formatting, no logic change) | `style: format with ruff` |
| `refactor` | Code refactoring | `refactor(core): simplify data processing` |
| `perf` | Performance improvement | `perf: optimize data loading` |
| `test` | Adding or updating tests | `test(core): add unit tests` |
| `build` | Build system or dependencies | `build: update setuptools` |
| `ci` | CI/CD configuration | `ci: add Python 3.12 to matrix` |
| `chore` | Other changes | `chore: update gitignore` |
| `revert` | Revert a commit | `revert: revert "feat: add X"` |

### Tools

```bash
# Interactive commit (recommended)
cz commit

# Or standard git commit
git commit -m "feat: add new feature"
```

For full details, see [Commit Conventions](./commit_conventions.md).

---

## Pull Request Workflow

### 1. Pre-PR Checklist

Before creating a PR, ensure:

- [ ] Code is formatted (`ruff format`)
- [ ] Lint check passes (`ruff check`)
- [ ] Type check passes (`mypy`)
- [ ] Necessary tests added
- [ ] All tests pass (`pytest`)
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No Chinese in source code

**Quick check command**:

```bash
./scripts/check.sh
```

### 2. PR Title Format

Same as commit message format:

```
<type>(<scope>): <description>
```

**Examples**:
- `feat(core): add data validation`
- `fix(utils): resolve parsing issue`
- `docs: update API documentation`

### 3. PR Description

Use the provided PR template which includes:
- Description of changes
- Type of change
- Related issues
- Checklist

### 4. After Creating PR

1. Ensure CI checks automatically start
2. Wait for all checks to complete
3. Address any CI failures
4. Request code review

---

## Code Review Requirements

### Review Focus Areas

Reviewers should focus on:

1. **Functional correctness**: Does code correctly implement expected functionality
2. **Code quality**: Is code clear and maintainable
3. **Test coverage**: Is there sufficient test coverage
4. **Performance**: Are there obvious performance issues
5. **Security**: Are there security concerns
6. **Documentation**: Are APIs properly documented
7. **Language**: Is all code in English

### Review Response Labels

| Label | Meaning |
|-------|---------|
| `LGTM` | Looks Good To Me - Approve merge |
| `nit:` | Small suggestion, non-blocking |
| `question:` | Needs explanation |
| `suggestion:` | Improvement suggestion |
| `blocking:` | Must be fixed before merge |

---

## Merge Requirements

### Required Conditions

PR must meet all conditions before merge:

1. **CI passes** ✅
   - Lint check passes
   - Type check passes
   - All tests pass
   - Build check passes
   - Language check passes

2. **Code review** ✅
   - At least **1 LGTM** approval
   - All blocking issues resolved

3. **Branch updated** ✅
   - No conflicts with target branch

### Merge Strategy

- **Feature branch → main**: Squash and merge (recommended)
- **Hotfix → main**: Merge commit

### CI Testing Strategy

| Scenario | Test Scope | Expected Duration |
|----------|------------|-------------------|
| PR / Regular Push | Python 3.8 only | < 3 minutes |
| Push to main | Python 3.8-3.12 full matrix | ~5-7 minutes |

> This differentiated strategy ensures code quality while significantly improving PR feedback speed.

---

## Quick Reference Commands

```bash
# Code formatting
ruff format src/ tests/

# Lint check
ruff check src/ tests/

# Type check
mypy src/

# Run tests
pytest

# One-click check (recommended)
./scripts/check.sh

# Full CI simulation
./scripts/ci-local.sh

# Language check
python scripts/check_language.py

# Interactive commit
cz commit
```

---

## Related Documentation

- [Developer Guide](./developers_guide.md)
- [Local Testing Guide](./local_testing.md)
- [CI Workflow](./ci_workflow.md)
- [Commit Conventions](./commit_conventions.md)
- [Language Guidelines](./language_guidelines.md)
