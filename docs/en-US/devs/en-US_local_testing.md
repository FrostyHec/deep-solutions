# Local Testing Guide

This document describes how to test the `deep-solutions` project locally.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Testing with pytest](#testing-with-pytest)
- [Code Quality Checks](#code-quality-checks)
- [Multi-Version Testing with tox](#multi-version-testing-with-tox)
- [Pre-commit Hooks](#pre-commit-hooks)
- [CI Simulation](#ci-simulation)
- [Common Issues](#common-issues)

---

## Prerequisites

Before testing, ensure you have:

- Python 3.8+ installed
- Package installed in development mode: `pip install -e ".[dev]"`
- (Optional) Multiple Python versions for tox testing

---

## Quick Start

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_example.py

# Run specific test function
pytest tests/test_example.py::test_function_name
```

---

## Testing with pytest

### Basic Commands

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -x` | Stop on first failure |
| `pytest -s` | Show print statements |
| `pytest --tb=short` | Shorter traceback |

### Coverage Reporting

```bash
# Terminal coverage report
pytest --cov=src --cov-report=term-missing

# HTML coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser

# XML coverage report (for CI)
pytest --cov=src --cov-report=xml
```

### Test Selection

```bash
# Run tests matching pattern
pytest -k "test_validation"

# Run tests with specific marker
pytest -m "slow"

# Run tests in specific directory
pytest tests/unit/

# Exclude slow tests
pytest -m "not slow"
```

### Markers

Define custom markers in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
```

Use in tests:

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_integration():
    pass
```

---

## Code Quality Checks

### Lint Check (Ruff)

```bash
# Check for lint errors
ruff check src/ tests/

# Auto-fix lint errors
ruff check --fix src/ tests/

# Show detailed information
ruff check --show-fixes src/ tests/
```

### Format Check (Ruff)

```bash
# Check formatting (no changes)
ruff format --check src/ tests/

# Format code
ruff format src/ tests/

# Show diff
ruff format --diff src/ tests/
```

### Type Check (MyPy)

```bash
# Basic type check
mypy src/

# Strict mode
mypy --strict src/

# Show error codes
mypy --show-error-codes src/
```

### One-Click Check Script

Create `scripts/check.sh`:

```bash
#!/bin/bash
set -e

echo "=== Lint Check ==="
ruff check src/ tests/

echo "=== Format Check ==="
ruff format --check src/ tests/

echo "=== Type Check ==="
mypy src/

echo "=== Tests ==="
pytest

echo "=== All Checks Passed! ==="
```

Run:

```bash
chmod +x scripts/check.sh
./scripts/check.sh
```

---

## Multi-Version Testing with tox

### Installation

```bash
pip install tox
```

### Configuration

`tox.ini` or in `pyproject.toml`:

```toml
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py38,py39,py310,py311,py312

[testenv]
deps = pytest
commands = pytest {posargs}
"""
```

### Usage

```bash
# Run all environments
tox

# Run specific environment
tox -e py38

# Run with specific arguments
tox -- -v --tb=short

# Rebuild environments
tox --recreate

# List environments
tox -l
```

### Parallel Execution

```bash
# Run environments in parallel
tox -p auto

# Run 4 environments in parallel
tox -p 4
```

---

## Pre-commit Hooks

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Manual Run

```bash
# Run on staged files
pre-commit run

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

### Update Hooks

```bash
pre-commit autoupdate
```

### Configuration

See `.pre-commit-config.yaml` for configured hooks:
- Ruff format
- Ruff check
- MyPy
- Commitizen

---

## CI Simulation

### Full CI Simulation Script

Create `scripts/ci-local.sh`:

```bash
#!/bin/bash
set -e

echo "========================================"
echo "Starting Local CI Simulation"
echo "========================================"

echo ""
echo "--- Step 1: Lint Check ---"
ruff check src/ tests/

echo ""
echo "--- Step 2: Format Check ---"
ruff format --check src/ tests/

echo ""
echo "--- Step 3: Type Check ---"
mypy src/

echo ""
echo "--- Step 4: Language Check ---"
python scripts/check_language.py

echo ""
echo "--- Step 5: Tests with Coverage ---"
pytest --cov=src --cov-report=term-missing --cov-report=xml

echo ""
echo "========================================"
echo "All CI Checks Passed!"
echo "========================================"
```

### Using act (GitHub Actions Local Runner)

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run default workflow
act

# Run specific job
act -j test

# List available jobs
act -l

# Dry run
act -n
```

---

## Common Issues

### 1. Import Errors

**Problem**: `ModuleNotFoundError` when running tests

**Solution**: Ensure package is installed in development mode:
```bash
pip install -e ".[dev]"
```

### 2. Test Discovery Issues

**Problem**: Tests not discovered by pytest

**Solution**: Ensure:
- Test files are named `test_*.py` or `*_test.py`
- Test functions are named `test_*`
- Test directories have `__init__.py` (optional but recommended)

### 3. Coverage Not Collected

**Problem**: Coverage shows 0% or missing files

**Solution**: Check source path:
```bash
pytest --cov=src --cov-report=term-missing
```

Ensure `src/` contains your actual source code.

### 4. MyPy False Positives

**Problem**: MyPy reports errors for valid code

**Solutions**:
```python
# Type ignore for specific line
result = some_function()  # type: ignore[arg-type]

# Type ignore for block
# mypy: ignore-errors
```

Or configure in `pyproject.toml`:
```toml
[tool.mypy]
ignore_missing_imports = true
```

### 5. tox Environment Issues

**Problem**: tox can't find Python version

**Solution**: 
```bash
# Check available Python versions
python3.8 --version
python3.9 --version
# etc.

# Install missing versions with pyenv
pyenv install 3.9.18
```

### 6. Pre-commit Hook Failures

**Problem**: Pre-commit hook fails after git commit

**Solution**:
```bash
# Fix issues and re-stage
ruff format src/ tests/
ruff check --fix src/ tests/
git add -u
git commit
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Run all tests | `pytest` |
| Run with coverage | `pytest --cov=src` |
| HTML coverage | `pytest --cov=src --cov-report=html` |
| Lint check | `ruff check src/ tests/` |
| Format code | `ruff format src/ tests/` |
| Type check | `mypy src/` |
| Multi-version test | `tox` |
| Pre-commit check | `pre-commit run --all-files` |
| Full CI simulation | `./scripts/ci-local.sh` |

---

## Related Documentation

- [Developer Guide](./en-US_developers_guide.md)
- [CI Workflow](./en-US_ci_workflow.md)
- [Code Standards](./en-US_code_standards.md)
