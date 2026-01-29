# Developer Guide

This guide helps you get started contributing to the `deep-solutions` project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting the Code](#getting-the-code)
- [Environment Setup](#environment-setup)
- [Installing Dependencies](#installing-dependencies)
- [Verifying Setup](#verifying-setup)
- [Development Workflow](#development-workflow)
- [Quick Reference](#quick-reference)
- [Next Steps](#next-steps)

---

## Prerequisites

Before starting, ensure your system has:

- **Git** - Version control
- **Conda** (Miniconda/Anaconda) - Python environment management
- **Python 3.8** - Development environment (required)

> **⚠️ Important**: This project requires development in **Python 3.8** environment. Although the project supports 3.8-3.12, development must use the minimum supported version to ensure compatibility.

---

## Getting the Code

### 1. Fork the Repository (External Contributors)

If you're an external contributor, first fork the repository:

1. Visit [deep-solutions](https://github.com/FrostyHec/deep-solutions)
2. Click the **Fork** button in the top right
3. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/deep-solutions.git
cd deep-solutions
```

4. Add upstream remote:

```bash
git remote add upstream https://github.com/FrostyHec/deep-solutions.git
```

### 2. Direct Clone (Team Members)

If you're a team member, clone directly:

```bash
git clone https://github.com/FrostyHec/deep-solutions.git
cd deep-solutions
```

---

## Environment Setup

### Dependency Management Strategy: Pip-in-Conda

This project uses the **Pip-in-Conda** strategy:

| Tool | Responsibility |
|------|----------------|
| **Conda** | Manages Python version only (creates isolated environment) |
| **Pip** | Manages all Python package dependencies |

> 📌 **Why this design?**
> - Avoids dependency conflicts from mixing conda and pip
> - `pyproject.toml` is the single source of truth for dependencies
> - Consistent with CI/CD environment

### Create Development Environment

```bash
# Create Python 3.8 environment
conda create -n deep-solutions python=3.8 -y

# Activate environment
conda activate deep-solutions
```

---

## Installing Dependencies

After activating the environment, install the project in editable mode with dev dependencies:

```bash
# Install project (editable mode) + dev dependencies
pip install -e ".[dev]"
```

This installs:
- The project itself (editable mode, changes take effect immediately)
- Core dependencies (numpy, scipy)
- Development dependencies (pytest, ruff, mypy, tox, commitizen, pre-commit, etc.)

### Setup Pre-commit Hooks

```bash
# Install pre-commit hooks (one-time setup)
pre-commit install --hook-type commit-msg
pre-commit install
```

---

## Verifying Setup

Run the following commands to verify your environment is correctly configured:

```bash
# Check Python version
python --version
# Output should be: Python 3.8.x

# Check package is installed
python -c "import deep_solutions; print(deep_solutions.__version__)"

# Run tests
pytest

# Run code checks
ruff check src/ tests/

# Run type checks
mypy src/
```

If all commands succeed, your environment is correctly configured!

---

## Development Workflow

### 1. Create Feature Branch

Always create a new branch from the latest main:

```bash
# Get latest code
git fetch origin
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Write Code

- Source code goes in `src/deep_solutions/` directory
- Test files go in `tests/` directory
- Ensure code has proper type annotations and docstrings
- **All comments and docstrings must be in English**

### 3. Run Checks

Before committing, use the one-click check script:

```bash
./scripts/check.sh
```

This script runs:
1. Code formatting (ruff format)
2. Lint check (ruff check)
3. Type check (mypy)
4. Run tests (pytest)

### 4. Commit Changes

Use Commitizen for conventional commits:

```bash
# Interactive commit (recommended)
cz commit

# Or standard git commit with proper format
git commit -m "feat: add new feature X"

# Push to remote
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Visit the GitHub repository
2. Click "Compare & pull request"
3. Fill in PR description using the template
4. Wait for CI checks and code review

> **Merge Requirements**: PR must pass all CI checks and receive at least one review approval before merging.

---

## Quick Reference

| Task | Command |
|------|---------|
| Activate environment | `conda activate deep-solutions` |
| Install dependencies | `pip install -e ".[dev]"` |
| Run tests | `pytest` |
| Format code | `ruff format src/ tests/` |
| Lint check | `ruff check src/ tests/` |
| Type check | `mypy src/` |
| One-click check | `./scripts/check.sh` |
| Simulate CI | `./scripts/ci-local.sh` |
| Tox test | `tox -e py38` |
| Interactive commit | `cz commit` |
| Language check | `python scripts/check_language.py` |

---

## Next Steps

After completing environment setup, we recommend reading:

- [Project Structure](./project_structure.md) - Understand directory structure and dependency management
- [Code Standards](./code_standards.md) - Learn commit conventions and code style
- [Local Testing Guide](./local_testing.md) - Learn various local testing methods
- [CI Workflow](./ci_workflow.md) - Understand CI/CD process
- [Language Guidelines](./language_guidelines.md) - Understand bilingual requirements
- [Commit Conventions](./commit_conventions.md) - Learn commit message format

---

## Getting Help

If you encounter issues:

1. Check [GitHub Issues](https://github.com/FrostyHec/deep-solutions/issues)
2. Create a new Issue describing your problem
3. Participate in Discussions

Welcome to join us! 🎉
