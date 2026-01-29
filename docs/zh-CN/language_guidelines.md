# 语言规范

本文档描述 `deep-solutions` 项目的语言要求，以确保一致性和对国际贡献者的可访问性。

## 目录
- [概述](#概述)
- [源代码](#源代码)
- [文档](#文档)
- [Commit Messages 和 PRs](#commit-messages-和-prs)
- [强制执行](#强制执行)

---

## 概述

项目采用**双语方式**，以英文为主：

| 内容类型 | 语言要求 |
|----------|----------|
| 源代码（注释、文档字符串） | **仅英文** |
| Commit messages | **仅英文** |
| PR 标题和描述 | **仅英文** |
| 文档 | **英文必须**，中文可选 |
| README | **英文必须**，推荐中文版本 |

---

## 源代码

### 注释和文档字符串

所有注释和文档字符串**必须是英文**：

```python
# ✅ 正确 - 英文注释
def process_data(data: List[int]) -> List[int]:
    """Process the input data.

    Args:
        data: List of integers to process.

    Returns:
        Processed list of integers.
    """
    # Filter out negative values
    return [x for x in data if x >= 0]


# ❌ 错误 - 中文注释
def process_data(data: List[int]) -> List[int]:
    """处理输入数据。"""  # 不允许
    # 过滤负值  # 不允许
    return [x for x in data if x >= 0]
```

### 字符串字面量

面向用户的字符串应使用英文。如果需要国际化，请使用适当的 i18n 框架。

### 为什么只用英文？

1. **可访问性**：国际贡献者可以理解和贡献
2. **一致性**：所有模块的代码库统一
3. **工具兼容**：与代码分析工具更好地兼容
4. **可搜索性**：更容易搜索和引用

---

## 文档

### 结构

```
docs/
├── developers_guide.md      # 英文（必须）
├── project_structure.md     # 英文（必须）
├── code_standards.md        # 英文（必须）
├── ...
└── zh-CN/                   # 中文翻译
    ├── developers_guide.md  # 中文（推荐）
    ├── project_structure.md
    └── ...
```

### 要求

| 文档 | 英文 | 中文 |
|------|------|------|
| 核心文档 (`docs/*.md`) | ✅ 必须 | - |
| 中文翻译 (`docs/zh-CN/*.md`) | - | ⚠️ 推荐 |
| README.md | ✅ 必须 | - |
| README.zh-CN.md | - | ⚠️ 推荐 |

### 优先级

- **英文始终是事实来源**
- 中文翻译应与英文版本保持同步
- 如果翻译不同步，以英文为准

---

## Commit Messages 和 PRs

### Commit Messages

所有 commit messages **必须是英文**，遵循 Conventional Commits：

```
# ✅ 正确
feat(core): add data validation function
fix(utils): resolve parsing edge case

# ❌ 错误
feat(core): 添加数据验证功能
修复: 解析边界情况
```

### PR 标题和描述

- PR 标题：**仅英文**
- PR 描述：**仅英文**（可以包含中文翻译作为补充）

```markdown
# ✅ 正确的 PR 描述

## Description
Add data validation pipeline for input processing.

## 中文说明（可选）
添加输入处理的数据验证管道。
```

---

## 强制执行

### 自动检查

项目包含自动语言检查：

1. **源代码检查**：检测 `src/` 和 `tests/` 中的中文字符
2. **文档检查**：验证英文文档存在，如果中文缺失则警告
3. **CI 集成**：语言检查作为 lint job 的一部分运行

### 本地运行

```bash
# 运行所有语言检查
python scripts/check_language.py

# 仅检查源代码
python scripts/check_language.py --source-only

# 仅检查文档
python scripts/check_language.py --docs-only

# 详细输出
python scripts/check_language.py --verbose
```

### CI 行为

| 检查 | 失败行为 |
|------|----------|
| 源代码中有中文 | ❌ 错误 - CI 失败 |
| 缺少英文文档 | ❌ 错误 - CI 失败 |
| 缺少中文文档 | ⚠️ 警告 - CI 通过但有警告 |

警告会在 PR check run 中报告以提高可见性。

---

## 贡献翻译

我们欢迎改进中文翻译的贡献：

1. 在 `docs/zh-CN/` 中创建/更新相应文件
2. 保持结构与英文版本一致
3. 提交类型为 `docs` 的 PR

示例：
```
docs(zh-CN): add Chinese translation for developers_guide
```

---

## 相关文档

- [Commit 规范](./commit_conventions.md)
- [代码规范](./code_standards.md)
- [开发者指南](./developers_guide.md)
