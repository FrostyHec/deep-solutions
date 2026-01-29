# Publishing Guide

This document describes how to publish the `deep-solutions` package to PyPI.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Versioning](#versioning)
- [Manual Publishing](#manual-publishing)
- [Automated Publishing (CI/CD)](#automated-publishing-cicd)
- [TestPyPI Testing](#testpypi-testing)
- [Post-Publish Verification](#post-publish-verification)
- [Troubleshooting](#troubleshooting)

---

## Overview

The publishing workflow follows these steps:

```
Version Bump → Build → Test → Upload to PyPI → Verify
```

We use:
- **setuptools-scm** for version management (based on git tags)
- **build** for creating distribution packages
- **twine** for uploading to PyPI

---

## Prerequisites

### Required Tools

```bash
pip install build twine
```

### PyPI Account

1. Create account at https://pypi.org/account/register/
2. Enable 2FA (recommended)
3. Create API token at https://pypi.org/manage/account/token/

### Configure API Token

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

Or use environment variables:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE
```

---

## Versioning

### Version Scheme

We use [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Source

Version is automatically determined from git tags using `setuptools-scm`:

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=64", "setuptools-scm[toml]>=8"]

[tool.setuptools_scm]
```

### Creating a Version Tag

```bash
# Check current version
python -c "import deep_solutions; print(deep_solutions.__version__)"

# Create new version tag
git tag v1.0.0
git push origin v1.0.0

# Or with annotation (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Pre-release Versions

```bash
# Alpha
git tag v1.0.0a1

# Beta
git tag v1.0.0b1

# Release candidate
git tag v1.0.0rc1
```

---

## Manual Publishing

### Step 1: Ensure Clean State

```bash
# Check for uncommitted changes
git status

# Ensure on main branch
git checkout main
git pull origin main
```

### Step 2: Run All Checks

```bash
# Run full test suite
pytest

# Run lint and type checks
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/
```

### Step 3: Create Version Tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Step 4: Build Distribution

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates:
- `dist/deep_solutions-1.0.0.tar.gz` (source)
- `dist/deep_solutions-1.0.0-py3-none-any.whl` (wheel)

### Step 5: Check Distribution

```bash
# Check package metadata
twine check dist/*
```

### Step 6: Upload to PyPI

```bash
twine upload dist/*
```

---

## Automated Publishing (CI/CD)

### GitHub Actions Workflow

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for trusted publishing

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### Trusted Publishing (Recommended)

Configure trusted publishing on PyPI:

1. Go to https://pypi.org/manage/project/deep-solutions/settings/publishing/
2. Add a new publisher:
   - Owner: `your-github-username`
   - Repository: `deep-solutions`
   - Workflow: `publish.yml`
   - Environment: (leave blank or use `release`)

### Creating a Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Choose or create tag (e.g., `v1.0.0`)
4. Fill in release notes
5. Click "Publish release"
6. CI will automatically publish to PyPI

---

## TestPyPI Testing

### Upload to TestPyPI

Always test with TestPyPI first:

```bash
# Build
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

### Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    deep-solutions
```

Note: `--extra-index-url` is needed for dependencies that aren't on TestPyPI.

---

## Post-Publish Verification

### 1. Check PyPI Page

Visit: https://pypi.org/project/deep-solutions/

Verify:
- Version is correct
- Description renders correctly
- Links work

### 2. Test Installation

```bash
# Create fresh virtual environment
python -m venv test-install
source test-install/bin/activate

# Install from PyPI
pip install deep-solutions

# Verify
python -c "import deep_solutions; print(deep_solutions.__version__)"

# Clean up
deactivate
rm -rf test-install
```

### 3. Test Basic Functionality

```python
import deep_solutions
# Run basic functionality tests
```

---

## Troubleshooting

### 1. "File already exists" Error

PyPI does not allow overwriting existing versions.

**Solution**: Bump version number and re-release.

### 2. "Invalid distribution" Error

**Solution**: Ensure valid package metadata:
```bash
twine check dist/*
```

Fix any reported issues in `pyproject.toml`.

### 3. Authentication Failed

**Solution**: Check your API token:
- Ensure token starts with `pypi-`
- Check token scope (project-specific vs account-wide)
- Regenerate token if needed

### 4. Version Not Detected

**Solution**: Ensure git tag exists:
```bash
git tag -l
git describe --tags
```

### 5. Build Fails

**Solution**: Check build dependencies:
```bash
pip install --upgrade build setuptools wheel
```

### 6. Missing Files in Distribution

**Solution**: Check `MANIFEST.in` if you have non-Python files:
```
include README.md
include LICENSE
recursive-include src *.py
```

Or use `pyproject.toml`:
```toml
[tool.setuptools.package-data]
"deep_solutions" = ["py.typed", "*.json"]
```

---

## Release Checklist

Before publishing:

- [ ] All tests pass
- [ ] Code formatted and linted
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version tag created
- [ ] Tested on TestPyPI
- [ ] GitHub release created (for automated publishing)

---

## Quick Reference

| Task | Command |
|------|---------|
| Check version | `python -c "import deep_solutions; print(deep_solutions.__version__)"` |
| Create tag | `git tag -a v1.0.0 -m "Release v1.0.0"` |
| Push tag | `git push origin v1.0.0` |
| Build | `python -m build` |
| Check dist | `twine check dist/*` |
| Upload to TestPyPI | `twine upload --repository testpypi dist/*` |
| Upload to PyPI | `twine upload dist/*` |

---

## Related Documentation

- [Developer Guide](./developers_guide.md)
- [CI Workflow](./ci_workflow.md)
- [Code Standards](./code_standards.md)
