#!/bin/bash
# =============================================================================
# CI 本地模拟脚本
# 用途: 在提交 PR 前模拟 CI 的所有检查步骤
# =============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# =============================================================================
# Step 1: Lint & Format Check
# =============================================================================
print_header "Step 1/4: Lint & Format Check"

echo "检查代码格式..."
if ruff format --check src/ tests/; then
    print_success "代码格式检查通过"
else
    print_error "代码格式检查失败"
    echo ""
    echo "运行以下命令修复："
    echo "  ruff format src/ tests/"
    exit 1
fi

echo ""
echo "运行 Linter..."
if ruff check src/ tests/; then
    print_success "Lint 检查通过"
else
    print_error "Lint 检查失败"
    echo ""
    echo "尝试自动修复："
    echo "  ruff check --fix src/ tests/"
    exit 1
fi

# =============================================================================
# Step 2: Type Check
# =============================================================================
print_header "Step 2/4: Type Check"

echo "运行 MyPy 类型检查..."
if mypy src/; then
    print_success "类型检查通过"
else
    print_error "类型检查失败"
    exit 1
fi

# =============================================================================
# Step 3: Run Tests
# =============================================================================
print_header "Step 3/4: Run Tests"

echo "运行测试并生成报告..."
if pytest --junitxml=pytest-report.xml --cov=deep_solutions --cov-report=xml --cov-report=term-missing; then
    print_success "所有测试通过"
else
    print_error "测试失败"
    exit 1
fi

# =============================================================================
# Step 4: Build Check
# =============================================================================
print_header "Step 4/4: Build Check"

echo "清理旧的构建产物..."
rm -rf dist/ build/ *.egg-info

echo "构建包..."
if python -m build; then
    print_success "包构建成功"
else
    print_error "包构建失败"
    exit 1
fi

echo ""
echo "检查包..."
if twine check dist/*; then
    print_success "包检查通过"
else
    print_error "包检查失败"
    exit 1
fi

# =============================================================================
# Summary
# =============================================================================
print_header "总结"

echo -e "${GREEN}✓ 所有 CI 检查通过！${NC}"
echo ""
echo "生成的文件："
echo "  - pytest-report.xml (测试报告)"
echo "  - coverage.xml (覆盖率报告)"
echo "  - dist/ (构建产物)"
echo ""
print_success "代码已准备好创建 Pull Request"
