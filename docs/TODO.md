# Release Script Implementation TODO

## Requirements
Create a convenient version release script that:
1. Reminds user to ensure CHANGELOG.md is updated
2. Switches to main branch and pulls latest code
3. Prompts user for version tag (e.g., v0.1.1rc1)
4. Creates and pushes git tag
5. Triggers publish-test workflow via gh CLI and waits for completion
6. Displays result and guides user for next steps (publish-pypi)

## TODO List

### Phase 1: Environment Setup
- [x] 1.1 Add `gh` to environment.yml (conda-forge channel)
- [x] 1.2 Test gh installation works in conda environment

### Phase 2: Fix publish-test.yml Workflow
- [x] 2.1 Remove "Create git tag (if not exists)" step
- [x] 2.2 Remove/fix permissions block (use default ref, not auto-create tags)
- [x] 2.3 Ensure checkout uses triggering ref with fetch-depth: 0
- [ ] 2.4 Test workflow with existing tag to verify it works

### Phase 3: Script Development
- [x] 3.1 Create release script: `scripts/release.sh`
- [x] 3.2 Implement CHANGELOG.md update reminder (step 0)
- [x] 3.3 Implement git branch switch to main + pull (step 1)
- [x] 3.4 Implement version tag input prompt (step 2)
- [x] 3.5 Implement git tag creation and push (step 3)
- [x] 3.6 Implement gh workflow trigger for publish-test (step 4)
- [x] 3.7 Implement workflow status monitoring and wait
- [x] 3.8 Implement result display and user guidance (step 5)
- [x] 3.9 Add error handling for all steps

### Phase 4: Testing & Debugging
- [ ] 4.1 Test error case: v0.1.1 (existing tag)
- [ ] 4.2 Test happy case: v0.1.1rc1 (new tag)
- [ ] 4.3 Verify gh CLI triggers workflow correctly
- [ ] 4.4 Verify workflow completion detection works
- [ ] 4.5 Verify user prompts are clear and helpful

### Phase 5: Documentation
- [x] 5.1 Update docs/agent.md (English) - add quick release at start of Section 3
- [x] 5.2 Update docs/zh-CN/agent.md (Chinese) - add quick release at start of Section 3
- [x] 5.3 Add prerequisite: gh auth login setup instructions
- [x] 5.4 Add usage examples with expected output

## Current Implementation Status

### ✅ Completed
- Environment setup (gh CLI added to environment.yml)
- Workflow fixes (removed auto-tag creation, fixed permissions)
- Script development (all 6 steps implemented)
- Error handling and validation
- Documentation updates (English + Chinese)

### ⏳ Ready for Testing
The script is ready to test with real scenarios:
1. Error case: v0.1.1 (existing tag) - should detect and reject
2. Happy case: v0.1.1rc1 (new tag) - should complete full workflow

### 📝 Testing Instructions for User
To test the script:
```bash
# Test error case (tag exists)
bash scripts/release.sh
# When prompted, enter: v0.1.1
# Expected: Script should detect tag exists and exit

# Test happy case (new tag)
bash scripts/release.sh
# Follow the prompts:
# 1. Confirm CHANGELOG updated (y)
# 2. Enter version: v0.1.1rc1
# 3. Wait for workflow to complete
# 4. Follow instructions for PyPI publish
```

## Delivery Checklist
- [ ] Script executes without errors
- [ ] Script validates version format (vX.Y.Z)
- [ ] Script creates git tag properly
- [ ] Script triggers GitHub release
- [ ] Script has helpful error messages
- [ ] Documentation is clear and complete
- [ ] Prerequisites (gh auth) are documented
- [ ] Both English and Chinese docs updated

## Implementation Notes
- Script location: `scripts/release.sh`
- Uses bash for consistency with existing scripts
- Requires gh authentication (user will handle `gh auth login`)
- Should be idempotent (safe to re-run)
- Should validate before making changes
