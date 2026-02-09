# Contributing to deep-solutions

🎉 **Thank you for your interest in contributing to deep-solutions!** Your contributions help make this project better for everyone. We welcome all kinds of contributions — bug fixes, feature enhancements, documentation improvements, and more.

---

## 📋 Table of Contents

- [Before You Start](#before-you-start)
- [Contribution Workflow](#contribution-workflow)
  - [Step 1: Setup Development Environment](#step-1-setup-development-environment)
  - [Step 2: Create an Issue (Optional)](#step-2-create-an-issue-optional)
  - [Step 3: Create a Feature Branch](#step-3-create-a-feature-branch)
  - [Step 4: Run Local Tests](#step-4-run-local-tests)
  - [Step 5: Commit Your Changes](#step-5-commit-your-changes)
  - [Step 6: Submit a Pull Request](#step-6-submit-a-pull-request)
  - [Step 7: Review & Merge](#step-7-review--merge)
  - [Step 8: Clean Up](#step-8-clean-up)
- [Code Standards & Conventions](#code-standards--conventions)
- [FAQ](#faq)

---

## Before You Start

Please take a moment to familiarize yourself with the project:

1. **Read the [Agent Development Guide](en-US_agent.md)** — Comprehensive technical documentation covering project structure, code standards, testing, and release procedures. **This is essential reading for all contributors.**

2. **Check [Code Standards](en-US_code_standards.md)** — Understanding commit conventions and PR requirements.

3. **Review [Project Structure](en-US_project_structure.md)** — Learn about dependencies and how the project is organized.

---

## Contribution Workflow

Follow these steps to contribute a new feature or fix:

### Step 1: Setup Development Environment

First, ensure you have Python 3.8 and conda installed.

```bash
# Clone the repository
git clone https://github.com/FrostyHec/deep-solutions.git
cd deep-solutions

# Create development environment
conda env create -f environment.yml

# Activate environment
conda activate deep-solutions

# Install package with dev dependencies
pip install -e ".[dev]"

# Verify setup
python -c "import deep_solutions; print(deep_solutions.__version__)"
```

> **Important**: Read the [Agent Development Guide](en-US_agent.md) **before proceeding**. It contains essential information about project structure, code specifications, and best practices.

### Step 2: Create an Issue (Optional)

Before starting work on a feature, consider creating an issue to:
- Discuss your proposed changes
- Get feedback from maintainers
- Ensure it aligns with project goals

**Issue Template**:
- **Title**: Brief description of the feature/fix
- **Description**: What problem does this solve? Why is it needed?
- **Acceptance Criteria**: How will we know it's complete?

---

### Step 3: Create a Feature Branch

Create a branch from the `main` branch with a descriptive name.

**Branch Naming Convention**:
- Features: `feature/description-of-feature`
- Bug fixes: `fix/description-of-bug`
- Documentation: `docs/description-of-docs`
- Examples: 
  - `feature/add-tensor-utils`
  - `fix/resolve-import-error`
  - `docs/improve-contributing-guide`

```bash
# Ensure you're on main and up-to-date
git checkout main
git pull origin main

# Create and switch to your feature branch
git checkout -b feature/your-feature-name
```

> **⚠️ Important**: Always create your branch from `main`, never from other feature branches.

---

### Step 4: Run Local Tests

Before submitting a pull request, ensure all tests pass locally.

**Run all checks**:
```bash
bash scripts/check.sh
```

This will:
- ✅ Check code formatting (ruff format)
- ✅ Run linting (ruff check)
- ✅ Type check (mypy)
- ✅ Verify no Chinese characters in code/docs
- ✅ Run unit tests (pytest)

**Other useful test commands**:
```bash
# Run only unit tests
pytest

# Run tests with coverage
pytest --cov=deep_solutions --cov-report=html

# Test on multiple Python versions (3.8-3.12)
tox

# Simulate full CI locally
bash scripts/ci-local.sh
```

> **❌ Do not push** if any checks fail. Fix issues locally first.

---

### Pre-Submission Checklist

Before submitting your PR, verify the following:

- [ ] **Commit conventions**: All commits follow [Conventional Commits](en-US_commit_conventions.md) format
- [ ] **All checks pass**: `bash scripts/check.sh` completes with no errors
- [ ] **Tests pass**: `pytest` runs without failures; new features have unit tests
- [ ] **Documentation updated**: If you changed behavior, file structure, or APIs, update the relevant docs (both EN and ZH versions)
- [ ] **No stale references**: If you moved/renamed files, update all cross-references in docs and READMEs

---

### Step 5: Commit Your Changes

Follow the project's commit convention for clear, descriptive commits.

**Commit Message Format** (Conventional Commits):
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `chore`: Dependency updates, configuration changes

**Examples**:
```bash
git commit -m "feat(core): add new utility function for tensor processing"
git commit -m "fix(utils): resolve edge case in format_output"
git commit -m "docs(contributing): improve contributor guide"
```

> For detailed conventions, see [Commit Conventions](en-US_commit_conventions.md).

---

### Step 6: Submit a Pull Request

Push your branch and create a PR on GitHub.

**Push your branch**:
```bash
git push origin feature/your-feature-name
```

**Create PR on GitHub**:
1. Visit the repository: https://github.com/FrostyHec/deep-solutions
2. Click **"Pull requests"** tab
3. Click **"New pull request"** button
4. Set:
   - **Base branch**: `main`
   - **Compare branch**: `feature/your-feature-name`
5. Click **"Create pull request"**

**PR Description Template**:
```markdown
## Description
Brief description of what this PR does.

## Related Issue
Closes #123 (if applicable)

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How did you test this change? (e.g., "Ran pytest locally and all tests pass")

## Checklist
- [ ] I have read the contributing guide
- [ ] All tests pass locally (`bash scripts/check.sh`)
- [ ] Code follows project conventions
- [ ] Commit messages follow Conventional Commits
- [ ] Documentation is updated (if applicable)
```

**Pro Tips**:
- ✅ Link related issues in the PR description (e.g., `Closes #123`)
- ✅ Keep PRs focused — one feature per PR when possible
- ✅ Write clear, descriptive PR titles

---

### Step 7: Review & Merge

After submitting your PR:

1. **CI Checks Run Automatically**: GitHub Actions will run all tests and checks. Check the status in the PR.

2. **Code Review**: Maintainers will review your code and may request changes. Address feedback by:
   ```bash
   # Make changes to your files
   git add .
   git commit -m "refactor: address review feedback"
   git push origin feature/your-feature-name
   ```

3. **Approval & Merge**: Once approved and CI passes:
   - The maintainer will merge using **Squash and Merge**
   - This combines all your commits into a single, clean commit
   - The commit message will follow Conventional Commits format

**Merge Details**:
- **Strategy**: Squash and Merge (keeps `main` history clean)
- **Commit Message**: Based on your PR title and description
- **Format**: `feat(scope): description` (Conventional Commits)

---

### Step 8: Clean Up

**After your PR is merged, delete your local and remote branches**:

```bash
# Delete local branch
git branch -d feature/your-feature-name

# Delete remote branch
git push origin --delete feature/your-feature-name
```

> ⚠️ **Important**: Once deleted, **never push to this branch again**. Create a new branch if you need to make additional changes.

**Verify cleanup**:
```bash
# List local branches (feature/your-feature-name should not appear)
git branch -a

# Update local branch list from remote
git fetch --prune
```

---

## Code Standards & Conventions

When contributing, please follow these standards:

### Code Style
- **Formatter**: Ruff (`ruff format src/ tests/`)
- **Linter**: Ruff (`ruff check src/ tests/`)
- **Type Hints**: All functions must have type hints (`mypy src/`)
- **Python Version**: Minimum 3.8, test with 3.8-3.12

### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Testing
- All new features must have unit tests
- Aim for >80% code coverage
- Tests go in `tests/` directory

### Documentation
- Docstrings: Google-style or NumPy-style
- Include examples where helpful
- Update README if behavior changes

### Git Hygiene
- ✅ Meaningful commit messages
- ✅ Small, focused commits
- ✅ No merge commits in feature branches
- ✅ Delete branches after merge

For more details, see [Code Standards](en-US_code_standards.md) and [Commit Conventions](en-US_commit_conventions.md).

---

## FAQ

### Q: Can I contribute if I'm not a team member?
**A:** Yes! We welcome external contributors. Follow the same workflow — fork the repo, create a branch, and submit a PR.

### Q: Do I need to create an issue before submitting a PR?
**A:** No, it's optional. Small fixes can go directly to PR. For larger features, an issue discussion is helpful.

### Q: What if my PR doesn't pass CI?
**A:** Check the CI logs (click "Details" on the failed check). Fix the issues locally, commit, and push to your branch. The PR will update automatically.

### Q: How long does review take?
**A:** Depends on the PR complexity. We aim to review within 2-3 days. Thank you for your patience!

### Q: Can I push to my branch after submitting a PR?
**A:** Yes! Push updates to the same branch and the PR will update automatically.

### Q: What happens to my commits after merge?
**A:** They are squashed into a single commit with your PR title/description as the commit message, following Conventional Commits format.

### Q: I accidentally pushed to the wrong branch. What do I do?
**A:** Create a new correct branch from `main`, cherry-pick your commits, and submit a new PR. We can help if needed!

---

## Getting Help

- **Questions?** Open an [issue](https://github.com/FrostyHec/deep-solutions/issues)
- **Need guidance?** Check the [Agent Development Guide](en-US_agent.md) or [Developer Guide](en-US_developers_guide.md)
- **Found a bug?** Report it on [GitHub Issues](https://github.com/FrostyHec/deep-solutions/issues)

---

## 🙏 Thank You!

**We deeply appreciate your contributions!** Whether it's code, documentation, bug reports, or feature suggestions — every bit helps. The open-source community thrives because of contributors like you.

**Let's build something amazing together! 🚀**

---

*Last updated: February 2026*
