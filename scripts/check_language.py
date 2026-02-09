#!/usr/bin/env python3
"""
Language checker for deep-solutions project.

This script checks:
1. Source code contains only English (no Chinese characters in comments/strings)
2. English documentation exists for each doc file
3. Chinese documentation exists (warning only if missing)

Exit codes:
- 0: All checks passed (may have warnings)
- 1: Errors found (Chinese in source code)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Regex pattern for Chinese characters (CJK Unified Ideographs)
# Using proper Unicode escapes for extended ranges
CHINESE_PATTERN = re.compile(
    r"[\u4e00-\u9fff"  # CJK Unified Ideographs
    r"\u3400-\u4dbf"   # CJK Unified Ideographs Extension A
    r"\U00020000-\U0002a6df"  # CJK Unified Ideographs Extension B (use \U for 8-digit)
    r"\u3000-\u303f"   # CJK Symbols and Punctuation
    r"\uff00-\uffef]"  # Halfwidth and Fullwidth Forms
)

# Files/directories to exclude from source code check
EXCLUDE_PATTERNS = [
    "__pycache__",
    "/.git/",  # Use directory separators to avoid matching .github
    "/.git\\",
    ".tox",
    "*.egg-info",
    "build",
    "dist",
    ".nonpublic",
]


class LanguageChecker:
    """Check language requirements for the project."""

    def __init__(self, root_dir: str, verbose: bool = False):
        self.root_dir = Path(root_dir)
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def check_file_for_chinese(self, filepath: Path) -> List[Tuple[int, str]]:
        """
        Check a file for Chinese characters.

        Returns list of (line_number, line_content) tuples where Chinese was found.
        """
        chinese_lines = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    if CHINESE_PATTERN.search(line):
                        chinese_lines.append((line_num, line.strip()))
        except (UnicodeDecodeError, IOError) as e:
            self.log(f"Warning: Could not read {filepath}: {e}")
        return chinese_lines

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from checking."""
        path_str = str(path)
        for pattern in EXCLUDE_PATTERNS:
            if pattern in path_str:
                return True
        return False

    def check_source_code(self) -> int:
        """
        Check source code for Chinese characters.

        Returns number of files with Chinese characters.
        """
        self.log("\n=== Checking source code for Chinese characters ===")
        src_dir = self.root_dir / "src"
        tests_dir = self.root_dir / "tests"

        files_with_chinese = 0

        for directory in [src_dir, tests_dir]:
            if not directory.exists():
                continue

            for filepath in directory.rglob("*.py"):
                if self.should_exclude(filepath):
                    continue

                chinese_lines = self.check_file_for_chinese(filepath)
                if chinese_lines:
                    files_with_chinese += 1
                    rel_path = filepath.relative_to(self.root_dir)
                    for line_num, content in chinese_lines:
                        error_msg = f"ERROR: Chinese found in {rel_path}:{line_num}: {content[:60]}..."
                        self.errors.append(error_msg)
                        print(error_msg)

        if files_with_chinese == 0:
            self.log("✓ No Chinese characters found in source code")

        return files_with_chinese

    def check_ci_configs(self) -> int:
        """
        Check CI/CD configuration files for Chinese characters.

        Returns number of files with Chinese characters.
        """
        self.log("\n=== Checking CI/CD configuration files ===")
        github_dir = self.root_dir / ".github"

        files_with_chinese = 0

        if not github_dir.exists():
            self.log("✓ .github directory does not exist")
            return 0

        # Check workflow files (YAML)
        workflows_dir = github_dir / "workflows"
        if workflows_dir.exists():
            for filepath in workflows_dir.glob("*.yml"):
                if self.should_exclude(filepath):
                    continue

                chinese_lines = self.check_file_for_chinese(filepath)
                if chinese_lines:
                    files_with_chinese += 1
                    rel_path = filepath.relative_to(self.root_dir)
                    for line_num, content in chinese_lines:
                        error_msg = f"ERROR: Chinese found in {rel_path}:{line_num}: {content[:60]}..."
                        self.errors.append(error_msg)
                        print(error_msg)
            
            if files_with_chinese == 0:
                self.log(f"✓ No Chinese found in {workflows_dir.relative_to(self.root_dir)}")

        # Check issue template files (Markdown)
        templates_dir = github_dir / "ISSUE_TEMPLATE"
        if templates_dir.exists():
            for filepath in templates_dir.glob("*.md"):
                if self.should_exclude(filepath):
                    continue

                chinese_lines = self.check_file_for_chinese(filepath)
                if chinese_lines:
                    files_with_chinese += 1
                    rel_path = filepath.relative_to(self.root_dir)
                    for line_num, content in chinese_lines:
                        error_msg = f"ERROR: Chinese found in {rel_path}:{line_num}: {content[:60]}..."
                        self.errors.append(error_msg)
                        print(error_msg)
            
            if files_with_chinese == 0:
                self.log(f"✓ No Chinese found in {templates_dir.relative_to(self.root_dir)}")

        # Check PR template
        pr_template = github_dir / "PULL_REQUEST_TEMPLATE.md"
        if pr_template.exists():
            chinese_lines = self.check_file_for_chinese(pr_template)
            if chinese_lines:
                files_with_chinese += 1
                rel_path = pr_template.relative_to(self.root_dir)
                for line_num, content in chinese_lines:
                    error_msg = f"ERROR: Chinese found in {rel_path}:{line_num}: {content[:60]}..."
                    self.errors.append(error_msg)
                    print(error_msg)
            else:
                self.log(f"✓ Found: {pr_template.relative_to(self.root_dir)}")

        return files_with_chinese

    def check_documentation(self) -> Tuple[int, int]:
        """
        Check documentation for bilingual support.

        Scans all files in docs/ directory (baseline for English files),
        checks if corresponding files exist in docs/zh-CN/.
        Also reports extra files in zh-CN that don't have English versions.

        Returns (missing_chinese_count, extra_chinese_count).
        """
        self.log("\n=== Checking documentation for bilingual support ===")
        docs_dir = self.root_dir / "docs"
        zh_cn_dir = docs_dir / "zh-CN"

        missing_chinese = 0
        extra_chinese = 0

        # Ensure directories exist
        if not docs_dir.exists():
            warning_msg = f"WARNING: docs/ directory does not exist"
            self.warnings.append(warning_msg)
            return 0, 0

        if not zh_cn_dir.exists():
            warning_msg = f"WARNING: docs/zh-CN/ directory does not exist"
            self.warnings.append(warning_msg)
            return 0, 0

        # Get all files in English docs (excluding subdirectories)
        en_files = set()
        for item in docs_dir.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                en_files.add(item.name)

        # Get all files in Chinese docs
        zh_files = set()
        for item in zh_cn_dir.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                zh_files.add(item.name)

        # Check for missing Chinese versions
        for en_file in sorted(en_files):
            self.log(f"✓ Found: docs/{en_file}")
            if en_file not in zh_files:
                warning_msg = f"WARNING: Missing Chinese documentation: docs/zh-CN/{en_file}"
                self.warnings.append(warning_msg)
                print(warning_msg)
                missing_chinese += 1
            else:
                self.log(f"✓ Found: docs/zh-CN/{en_file}")

        # Check for extra files in Chinese docs (not in English)
        for zh_file in sorted(zh_files):
            if zh_file not in en_files:
                warning_msg = f"WARNING: Extra Chinese documentation without English version: docs/zh-CN/{zh_file}"
                self.warnings.append(warning_msg)
                print(warning_msg)
                extra_chinese += 1

        return missing_chinese, extra_chinese

    def check_readme(self) -> Tuple[bool, bool]:
        """
        Check README files exist.

        Returns (english_exists, chinese_exists).
        """
        self.log("\n=== Checking README files ===")
        readme_en = self.root_dir / "README.md"
        readme_zh = self.root_dir / "README.zh-CN.md"

        en_exists = readme_en.exists()
        zh_exists = readme_zh.exists()

        if not en_exists:
            error_msg = "ERROR: Missing English README.md"
            self.errors.append(error_msg)
            print(error_msg)
        else:
            self.log("✓ Found: README.md")

        if not zh_exists:
            warning_msg = "WARNING: Missing Chinese README.zh-CN.md"
            self.warnings.append(warning_msg)
            print(warning_msg)
        else:
            self.log("✓ Found: README.zh-CN.md")

        return en_exists, zh_exists

    def run_all_checks(self) -> int:
        """
        Run all language checks.

        Returns exit code (0 = success, 1 = errors found).
        """
        print("=" * 60)
        print("Language Check for deep-solutions")
        print("=" * 60)

        # Check source code
        chinese_in_source = self.check_source_code()

        # Check CI/CD configuration
        chinese_in_ci = self.check_ci_configs()

        # Check documentation
        missing_zh_docs, extra_zh_docs = self.check_documentation()

        # Check README
        readme_en_exists, readme_zh_exists = self.check_readme()

        # Summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All language checks passed!")

        # Return error code only for actual errors (not warnings)
        return 1 if self.errors else 0

    def get_warnings_json(self) -> str:
        """Return warnings as JSON for CI integration."""
        import json

        return json.dumps(
            {"warnings": self.warnings, "errors": self.errors}, indent=2
        )


def main():
    parser = argparse.ArgumentParser(
        description="Check language requirements for deep-solutions project"
    )
    parser.add_argument(
        "--root",
        "-r",
        default=".",
        help="Root directory of the project (default: current directory)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--json", "-j", action="store_true", help="Output warnings as JSON"
    )
    parser.add_argument(
        "--source-only",
        "-s",
        action="store_true",
        help="Only check source code for Chinese",
    )
    parser.add_argument(
        "--docs-only",
        "-d",
        action="store_true",
        help="Only check documentation",
    )

    args = parser.parse_args()

    checker = LanguageChecker(args.root, args.verbose)

    if args.source_only:
        exit_code = 1 if checker.check_source_code() > 0 else 0
    elif args.docs_only:
        missing_en, _ = checker.check_documentation()
        checker.check_readme()
        exit_code = 1 if missing_en > 0 else 0
    else:
        exit_code = checker.run_all_checks()

    if args.json:
        print("\n--- JSON Output ---")
        print(checker.get_warnings_json())

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
