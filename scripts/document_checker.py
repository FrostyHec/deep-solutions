#!/usr/bin/env python3
"""
Documentation checker for deep-solutions project.

This module checks:
1. Bilingual documentation structure (en-US <-> zh-CN)
2. All subdirectories under docs/ recursively
3. Broken documentation references (links to non-existent local docs)
4. Index.md files exist in all directories

All issues are treated as ERRORS (not warnings) and will cause CI to fail.

Exit codes:
- 0: All checks passed
- 1: Errors found
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Set, Tuple


class DocumentChecker:
    """Check documentation requirements for the project."""

    def __init__(self, root_dir: str, verbose: bool = False):
        self.root_dir = Path(root_dir)
        self.verbose = verbose
        self.errors: List[str] = []

    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def find_all_subdirs(self, base_dir: Path) -> List[str]:
        """
        Recursively find all subdirectories under base_dir.
        
        Returns list of relative paths (e.g., ["devs", "devs/tutorials", "user-guide"]).
        """
        if not base_dir.exists():
            return []
        
        subdirs = []
        for item in base_dir.rglob("*"):
            if item.is_dir() and not item.name.startswith('.'):
                rel_path = item.relative_to(base_dir)
                subdirs.append(str(rel_path))
        
        return sorted(subdirs)

    def extract_local_doc_links(self, filepath: Path) -> Set[str]:
        """
        Extract local markdown links from a file.
        
        Returns set of referenced filenames (e.g., {"en-US_guide.md", "zh-CN_intro.md"}).
        Only extracts links to .md files in same directory or relative paths.
        """
        links = set()
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Pattern: [text](filename.md) or [text](./filename.md) or [text](subdir/filename.md)
            # We'll capture both relative and same-directory links
            pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
            matches = re.findall(pattern, content)
            
            for _, link in matches:
                # Skip absolute URLs
                if link.startswith('http://') or link.startswith('https://'):
                    continue
                
                # Remove anchors (#section)
                link = link.split('#')[0]
                
                # Clean up the link
                link = link.strip()
                
                if link:
                    links.add(link)
        
        except (UnicodeDecodeError, IOError) as e:
            self.log(f"Warning: Could not read {filepath}: {e}")
        
        return links

    def check_broken_references(self) -> int:
        """
        Check for broken documentation references.
        
        Returns number of broken references found.
        """
        self.log("\n=== Checking for broken documentation references ===")
        docs_dir = self.root_dir / "docs"
        
        if not docs_dir.exists():
            error_msg = "ERROR: docs/ directory does not exist"
            self.errors.append(error_msg)
            print(error_msg)
            return 1
        
        broken_count = 0
        
        # Check all markdown files in docs/
        for md_file in docs_dir.rglob("*.md"):
            if md_file.name.startswith('.'):
                continue
            
            # Get the directory containing this markdown file
            md_dir = md_file.parent
            
            # Extract links from this file
            links = self.extract_local_doc_links(md_file)
            
            for link in links:
                # Resolve the link relative to the markdown file's directory
                if link.startswith('./'):
                    link = link[2:]  # Remove ./
                
                target_path = md_dir / link
                
                # Check if target exists
                if not target_path.exists():
                    broken_count += 1
                    rel_source = md_file.relative_to(self.root_dir)
                    rel_target = target_path.relative_to(self.root_dir)
                    error_msg = f"ERROR: Broken link in {rel_source}: {link} -> {rel_target} (not found)"
                    self.errors.append(error_msg)
                    print(error_msg)
                else:
                    self.log(f"✓ Valid link in {md_file.relative_to(self.root_dir)}: {link}")
        
        if broken_count == 0:
            self.log("✓ No broken documentation references found")
        
        return broken_count

    def check_bilingual_structure(self) -> Tuple[int, int]:
        """
        Check documentation for bilingual support with recursive subdirectory checking.

        Structure: docs/{en-US,zh-CN}/**/*
        - English files use en-US_ prefix, Chinese files use zh-CN_ prefix
        - Each directory must have an index.md
        - Every en-US doc must have a zh-CN counterpart (and vice versa)
        - Checks ALL subdirectories recursively, not just predefined ones

        Returns (missing_counterpart_count, missing_index_count).
        """
        self.log("\n=== Checking bilingual documentation structure ===")
        docs_dir = self.root_dir / "docs"
        en_us_dir = docs_dir / "en-US"
        zh_cn_dir = docs_dir / "zh-CN"

        missing_counterpart = 0
        missing_index = 0

        if not docs_dir.exists():
            error_msg = "ERROR: docs/ directory does not exist"
            self.errors.append(error_msg)
            print(error_msg)
            return 1, 0

        # Check language root directories exist
        for lang_dir, lang_label in [(en_us_dir, "en-US"), (zh_cn_dir, "zh-CN")]:
            if not lang_dir.exists():
                error_msg = f"ERROR: docs/{lang_label}/ directory does not exist"
                self.errors.append(error_msg)
                print(error_msg)
                return 1, 0

        # Check index.md in each language root
        for lang_dir, lang_label in [(en_us_dir, "en-US"), (zh_cn_dir, "zh-CN")]:
            index_file = lang_dir / "index.md"
            if not index_file.exists():
                error_msg = f"ERROR: Missing index.md in docs/{lang_label}/"
                self.errors.append(error_msg)
                print(error_msg)
                missing_index += 1
            else:
                self.log(f"✓ Found: docs/{lang_label}/index.md")

        # Find ALL subdirectories recursively in en-US
        en_subdirs = self.find_all_subdirs(en_us_dir)
        zh_subdirs = self.find_all_subdirs(zh_cn_dir)

        # Merge to get unique set of all subdirs that should exist in both languages
        all_subdirs = sorted(set(en_subdirs) | set(zh_subdirs))

        self.log(f"\nFound {len(all_subdirs)} subdirectories to check: {all_subdirs}")

        # Check each subdirectory
        for subdir in all_subdirs:
            en_subdir = en_us_dir / subdir
            zh_subdir = zh_cn_dir / subdir

            # Check subdirectory existence
            if not en_subdir.exists():
                error_msg = f"ERROR: Missing directory: docs/en-US/{subdir}/ (exists in zh-CN)"
                self.errors.append(error_msg)
                print(error_msg)
                missing_counterpart += 1
            
            if not zh_subdir.exists():
                error_msg = f"ERROR: Missing directory: docs/zh-CN/{subdir}/ (exists in en-US)"
                self.errors.append(error_msg)
                print(error_msg)
                missing_counterpart += 1

            # Check index.md exists in each subdirectory (if dir exists)
            for d, label in [(en_subdir, f"en-US/{subdir}"), (zh_subdir, f"zh-CN/{subdir}")]:
                if d.exists():
                    index_file = d / "index.md"
                    if not index_file.exists():
                        error_msg = f"ERROR: Missing index.md in docs/{label}/"
                        self.errors.append(error_msg)
                        print(error_msg)
                        missing_index += 1
                    else:
                        self.log(f"✓ Found: docs/{label}/index.md")

            # Skip bilingual pairing if either dir doesn't exist
            if not en_subdir.exists() or not zh_subdir.exists():
                continue

            # Collect doc files (exclude index.md and hidden files)
            en_files = set()
            for item in en_subdir.iterdir():
                if item.is_file() and item.name != "index.md" and not item.name.startswith('.'):
                    en_files.add(item.name)

            zh_files = set()
            for item in zh_subdir.iterdir():
                if item.is_file() and item.name != "index.md" and not item.name.startswith('.'):
                    zh_files.add(item.name)

            # Build base name mapping: strip prefix to get base name
            # en-US_foo.md -> foo.md, zh-CN_foo.md -> foo.md
            en_base_to_file = {}
            for f in en_files:
                base = f.replace("en-US_", "", 1) if f.startswith("en-US_") else f
                en_base_to_file[base] = f

            zh_base_to_file = {}
            for f in zh_files:
                base = f.replace("zh-CN_", "", 1) if f.startswith("zh-CN_") else f
                zh_base_to_file[base] = f

            # Check EN files have ZH counterparts
            for base, en_file in sorted(en_base_to_file.items()):
                self.log(f"✓ Found: docs/en-US/{subdir}/{en_file}")
                if base not in zh_base_to_file:
                    error_msg = (
                        f"ERROR: Missing Chinese counterpart for "
                        f"docs/en-US/{subdir}/{en_file} "
                        f"(expected docs/zh-CN/{subdir}/zh-CN_{base})"
                    )
                    self.errors.append(error_msg)
                    print(error_msg)
                    missing_counterpart += 1
                else:
                    self.log(f"✓ Found: docs/zh-CN/{subdir}/{zh_base_to_file[base]}")

            # Check ZH files have EN counterparts
            for base, zh_file in sorted(zh_base_to_file.items()):
                if base not in en_base_to_file:
                    error_msg = (
                        f"ERROR: Missing English counterpart for "
                        f"docs/zh-CN/{subdir}/{zh_file} "
                        f"(expected docs/en-US/{subdir}/en-US_{base})"
                    )
                    self.errors.append(error_msg)
                    print(error_msg)
                    missing_counterpart += 1

        return missing_counterpart, missing_index

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
            error_msg = "ERROR: Missing Chinese README.zh-CN.md"
            self.errors.append(error_msg)
            print(error_msg)
        else:
            self.log("✓ Found: README.zh-CN.md")

        return en_exists, zh_exists

    def run_all_checks(self) -> int:
        """
        Run all documentation checks.

        Returns exit code (0 = success, 1 = errors found).
        """
        print("=" * 60)
        print("Documentation Check for deep-solutions")
        print("=" * 60)

        # Check bilingual structure
        missing_counterparts, missing_indexes = self.check_bilingual_structure()

        # Check README
        readme_en_exists, readme_zh_exists = self.check_readme()

        # Check broken references
        broken_refs = self.check_broken_references()

        # Summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for error in self.errors:
                print(f"  - {error}")
            print("\n❌ Documentation checks FAILED!")
            return 1
        else:
            print("\n✅ All documentation checks passed!")
            return 0


def main():
    parser = argparse.ArgumentParser(
        description="Check documentation requirements for deep-solutions project"
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

    args = parser.parse_args()

    checker = DocumentChecker(args.root, args.verbose)
    exit_code = checker.run_all_checks()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
