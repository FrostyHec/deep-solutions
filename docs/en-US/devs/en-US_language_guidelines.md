# Language Guidelines

This document describes the language requirements for the `deep-solutions` project to ensure consistency and accessibility for international contributors.

## Table of Contents
- [Overview](#overview)
- [Source Code](#source-code)
- [Documentation](#documentation)
- [Commit Messages and PRs](#commit-messages-and-prs)
- [Enforcement](#enforcement)

---

## Overview

The project follows a **bilingual approach** with English as the primary language:

| Content Type | Language Requirement |
|--------------|---------------------|
| Source code (comments, docstrings) | **English only** |
| Commit messages | **English only** |
| PR titles and descriptions | **English only** |
| Documentation | **English required**, Chinese optional |
| README | **English required**, Chinese version recommended |

---

## Source Code

### Comments and Docstrings

All comments and docstrings **must be in English**:

```python
# ✅ Good - English comment
def process_data(data: List[int]) -> List[int]:
    """Process the input data.

    Args:
        data: List of integers to process.

    Returns:
        Processed list of integers.
    """
    # Filter out negative values
    return [x for x in data if x >= 0]


# ❌ Bad - Chinese comment
def process_data(data: List[int]) -> List[int]:
    """处理输入数据。"""  # Not allowed
    # 过滤负值  # Not allowed
    return [x for x in data if x >= 0]
```

### String Literals

User-facing strings should be in English. If internationalization is needed, use a proper i18n framework.

### Why English Only?

1. **Accessibility**: International contributors can understand and contribute
2. **Consistency**: Uniform codebase across all modules
3. **Tooling**: Better compatibility with code analysis tools
4. **Searchability**: Easier to search and reference

---

## Documentation

### Structure

```
docs/
├── developers_guide.md      # English (required)
├── project_structure.md     # English (required)
├── code_standards.md        # English (required)
├── ...
└── zh-CN/                   # Chinese translations
    ├── developers_guide.md  # Chinese (recommended)
    ├── project_structure.md
    └── ...
```

### Requirements

| Documentation | English | Chinese |
|--------------|---------|---------|
| Core docs (`docs/*.md`) | ✅ Required | - |
| Chinese translations (`docs/zh-CN/*.md`) | - | ⚠️ Recommended |
| README.md | ✅ Required | - |
| README.zh-CN.md | - | ⚠️ Recommended |

### Priority

- **English is always the source of truth**
- Chinese translations should be kept in sync with English versions
- If translations are out of sync, English takes precedence

---

## Commit Messages and PRs

### Commit Messages

All commit messages **must be in English** following Conventional Commits:

```
# ✅ Good
feat(core): add data validation function
fix(utils): resolve parsing edge case

# ❌ Bad
feat(core): 添加数据验证功能
修复: 解析边界情况
```

### PR Titles and Descriptions

- PR titles: **English only**
- PR descriptions: **English only** (may include Chinese translation as supplementary)

```markdown
# ✅ Good PR Description

## Description
Add data validation pipeline for input processing.

## 中文说明 (Optional)
添加输入处理的数据验证管道。
```

---

## Enforcement

### Automated Checks

The project includes automated language and documentation checks:

1. **Source code check** (`check_language.py`): Detects Chinese characters in `src/` and `tests/`
2. **Documentation check** (`document_checker.py`): 
   - Verifies bilingual structure (en-US ↔ zh-CN) recursively
   - Checks for missing documentation counterparts
   - Detects broken documentation references
   - Ensures `index.md` exists in all directories
3. **CI integration**: All checks run as part of the CI pipeline

### Running Locally

```bash
# Run all language checks (includes documentation)
python scripts/check_language.py

# Check source code only
python scripts/check_language.py --source-only

# Check documentation only
python scripts/check_language.py --docs-only
# Or directly:
python scripts/document_checker.py

# Verbose output
python scripts/check_language.py --verbose
python scripts/document_checker.py --verbose
```

### CI Behavior

| Check | Failure Behavior |
|-------|------------------|
| Chinese in source code | ❌ Error - CI fails |
| Missing English documentation | ❌ Error - CI fails |
| Missing Chinese documentation | ❌ Error - CI fails |
| Broken documentation references | ❌ Error - CI fails |
| Missing `index.md` files | ❌ Error - CI fails |

**All documentation issues are now treated as errors**, not warnings. This ensures bilingual parity and prevents broken links.

---

## Contributing Translations

We welcome contributions to improve Chinese translations:

1. Create/update the corresponding file in `docs/zh-CN/{subdir}/` with `zh-CN_` prefix
2. Keep the structure consistent with the English version in `docs/en-US/{subdir}/`
3. Submit a PR with type `docs`

Example:
```
docs(zh-CN): add Chinese translation for developers_guide
```

---

## Related Documentation

- [Commit Conventions](./en-US_commit_conventions.md)
- [Code Standards](./en-US_code_standards.md)
- [Developer Guide](./en-US_developers_guide.md)
