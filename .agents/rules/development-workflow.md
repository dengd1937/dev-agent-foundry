# Development Workflow

> This file extends [git-workflow.md](./git-workflow.md) with the full feature development process that happens before git operations.

The Feature Implementation Workflow describes the development pipeline: research, planning, TDD, code review, and then committing to git.

## Feature Implementation Workflow

1. **Research & Reuse** _(mandatory before any new implementation)_
   - **If `docs/product/<feature>.md` exists**, read it first: MVP scope, feature priorities, competitor analysis, and technical constraints come from the PM stage
   - **If `docs/designs/<feature>/` exists**, invoke **design-workflow** skill and read design artifacts per the V2-5 handoff table (intent.md, screenshots, review-verdict.md)
   - **GitHub code search first:** Run *GitHub MCP* to find existing implementations, templates, and patterns before writing anything new.
   - **Library docs second:** Use Context7 or primary vendor docs to confirm API behavior, package usage, and version-specific details before implementing.
   - **Use docs-lookup when behavior is unclear:** If framework, API, or third-party library behavior is uncertain, run **docs-lookup** agent before implementing.
   - **Exa only when the first two are insufficient:** Use Exa for broader web research or discovery after GitHub search and primary docs.
   - **Check package registries:** Search npm, PyPI, crates.io, and other registries before writing utility code. Prefer battle-tested libraries over hand-rolled solutions.
   - **Search for adaptable implementations:** Look for open-source projects that solve 80%+ of the problem and can be forked, ported, or wrapped.
   - Prefer adopting or porting a proven approach over writing net-new code when it meets the requirement.

2. **Plan First**
   - Use **planner** agent to create implementation plan
   - Save planning doc to `docs/plans/<feature-name>.md` before coding
   - **If `docs/designs/<feature>/` exists**, invoke **design-workflow** skill and reference component contracts and review findings in the plan per the V2-5 handoff table
   - Identify dependencies and risks
   - Break down into phases
   - **[Hard Gate]** Present the plan to the user for approval before proceeding — **do not write any code until the user explicitly approves**
   - _Optional:_ For complex plans, run **design-review** skill before approval for adversarial review (Claude Code users can also use **design-review-codex** for independent cross-model analysis)

3. **TDD Approach**
   - If fixing a bug, run **investigate** skill first before writing any fix code
   - Use **tdd-guide** agent
   - **If `docs/designs/<feature>/` exists**, invoke **design-workflow** skill to validate token usage and test documented states, variants, and accessibility requirements per the V2-5 handoff table
   - Write tests first (RED)
   - Implement to pass tests (GREEN)
   - Refactor (IMPROVE)
   - Critical user flow changes: add/update E2E coverage and run **e2e-runner** agent
   - Verify 80%+ coverage

4. **Quality Gate** _(after editing files)_
   - Run **code-quality-gate** skill after writing or modifying source files
   - Format all modified files (Biome/Prettier/Ruff/Black)
   - Lint and auto-fix issues (Biome/ESLint/Ruff)
   - Run type checker (tsc/mypy)
   - Remove debug artifacts (console.log, debugger, print statements)
   - Fix all errors before proceeding to code review

5. **Code Review** _(before commit)_
   - Run **code-reviewer** agent after Quality Gate passes; the `pre-commit-review-check` hook will remind if skipped
   - Python projects: also run **python-reviewer**
   - TypeScript/Next.js: also run **typescript-reviewer**
   - Auth, input validation, public endpoints, HTML rendering, file upload, or secret/env handling: also run **security-reviewer**
   - Address CRITICAL and HIGH issues before commit; consider MEDIUM issues
   - Override hook reminder when reviewing by other means: `export SKIP_REVIEW_CHECK=1`

6. **Documentation Decision** _(before commit)_
   - Delete `docs/plans/<feature-name>.md` — planning docs are process artifacts, not long-term knowledge
   - Create/update `docs/modules/<module>.md` if **any** of the following apply:
     - New standalone module (new package / Django app)
     - New external integration (third-party API or service)
     - New tech stack component (new database, message queue, etc.)
   - If a module doc is created, also update the module table in `docs/index.md`
   - If none of the above apply, ensure code comments are sufficient — no new doc needed

7. **Commit & Push**
   - Run **commit-quality** skill before committing
   - Validate commit message format (Conventional Commits)
   - Lint staged files only
   - Debug artifacts and secrets are caught automatically by pre-write / pre-bash hooks
   - Never use `--no-verify` — blocked by hook; fix the failing check instead
   - See [git-workflow.md](./git-workflow.md) for commit message format and PR process

8. **Pre-Review Checks**
   - Verify all automated checks (CI/CD) are passing
   - Resolve any merge conflicts
   - Ensure branch is up to date with target branch
   - Only request review after these checks pass
