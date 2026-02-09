# CI/CD Workflow

This document details the GitHub Actions CI/CD workflow configuration for the `deep-solutions` project.

## Table of Contents
- [Overview](#overview)
- [Workflow Triggers](#workflow-triggers)
- [Job Structure](#job-structure)
- [Python Version Matrix](#python-version-matrix)
- [Coverage Reporting](#coverage-reporting)
- [Branch Protection](#branch-protection)
- [Troubleshooting](#troubleshooting)

---

## Overview

Our CI/CD system uses GitHub Actions with a **differentiated testing strategy**:

| Scenario | Python Versions | Purpose |
|----------|-----------------|---------|
| Pull Request | 3.8 only | Fast feedback (< 3 min) |
| Push to main | 3.8, 3.9, 3.10, 3.11, 3.12 | Full compatibility check |

This approach balances development speed with thorough compatibility testing.

---

## Workflow Triggers

### Trigger Events

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

| Event | Branches | Matrix |
|-------|----------|--------|
| `push` | main | Full (3.8-3.12) |
| `pull_request` | main | Minimal (3.8 only) |

### Path Filters (Optional)

To skip CI for non-code changes:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'pyproject.toml'
      - '.github/workflows/**'
```

---

## Job Structure

### Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        CI Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────────┐ │
│  │  Lint   │   │  Type   │   │  Test   │   │    Coverage     │ │
│  │  Check  │   │  Check  │   │  Matrix │   │    Upload       │ │
│  └─────────┘   └─────────┘   └─────────┘   └─────────────────┘ │
│       │             │             │                  │          │
│       └─────────────┼─────────────┼──────────────────┘          │
│                     │             │                              │
│                     ▼             ▼                              │
│              ┌─────────────────────────┐                        │
│              │    Final Status Check   │                        │
│              └─────────────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Job Details

#### 1. Lint Check

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.8'
    - run: pip install ruff
    - run: ruff check src/ tests/
    - run: ruff format --check src/ tests/
```

#### 2. Type Check

```yaml
type-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.8'
    - run: pip install mypy
    - run: mypy src/
```

#### 3. Test Matrix

```yaml
test:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      python-version: ${{ github.event_name == 'push' && fromJSON('["3.8", "3.9", "3.10", "3.11", "3.12"]') || fromJSON('["3.8"]') }}
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -e ".[dev]"
    - run: pytest --cov=src --cov-report=xml
```

---

## Python Version Matrix

### Version Support

| Python | Status | Notes |
|--------|--------|-------|
| 3.8 | ✅ Supported | Minimum version, always tested |
| 3.9 | ✅ Supported | Full push testing |
| 3.10 | ✅ Supported | Full push testing |
| 3.11 | ✅ Supported | Full push testing |
| 3.12 | ✅ Supported | Latest stable |

### Matrix Configuration

```yaml
strategy:
  fail-fast: false  # Continue other jobs even if one fails
  matrix:
    python-version:
      ${{ github.event_name == 'push' && 
          fromJSON('["3.8", "3.9", "3.10", "3.11", "3.12"]') || 
          fromJSON('["3.8"]') }}
```

**Why `fail-fast: false`?**
- Allows seeing all failing versions, not just the first
- Useful for debugging version-specific issues

---

## Coverage Reporting

### Upload Strategy

**All Python versions upload coverage** to ensure comprehensive reporting:

```yaml
- name: Upload coverage
  uses: actions/upload-artifact@v4
  with:
    name: coverage-${{ matrix.python-version }}-${{ github.run_id }}
    path: coverage.xml
```

### Coverage Integration

We recommend integrating with Codecov:

```yaml
- name: Upload to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: coverage.xml
    flags: python-${{ matrix.python-version }}
    fail_ci_if_error: false
```

### Minimum Coverage Threshold

Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"
```

---

## Branch Protection

### Recommended Settings

For the `main` branch, configure in GitHub Settings:

| Setting | Value | Purpose |
|---------|-------|---------|
| Require pull request | ✅ | No direct pushes |
| Require status checks | ✅ | CI must pass |
| Required checks | lint, type-check, test | Specific jobs |
| Require up-to-date | ✅ | Must be current with main |
| Require review | ✅ | At least 1 approval |

### Required Status Checks

```
✅ lint
✅ type-check
✅ test (3.8)
```

---

## Troubleshooting

### Common Issues

#### 1. Cache Issues

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

If cache seems corrupted, increment cache version:

```yaml
key: v2-${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
```

#### 2. Test Timeout

```yaml
- name: Run tests
  run: pytest --timeout=300
  timeout-minutes: 10
```

#### 3. Matrix Expansion Debug

```yaml
- name: Debug matrix
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Python: ${{ matrix.python-version }}"
```

#### 4. Re-run Failed Jobs

1. Go to the Actions tab
2. Select the failed workflow run
3. Click "Re-run failed jobs"

### Debugging Locally

Simulate CI locally before pushing:

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow
act -j test
```

Or manually run the same commands:

```bash
# Lint
ruff check src/ tests/
ruff format --check src/ tests/

# Type check
mypy src/

# Test
pytest --cov=src
```

---

## Workflow File Location

The workflow file is located at:

```
.github/workflows/ci.yml
```

---

## Related Documentation

- [Developer Guide](./en-US_developers_guide.md)
- [Local Testing Guide](./en-US_local_testing.md)
- [Code Standards](./en-US_code_standards.md)
