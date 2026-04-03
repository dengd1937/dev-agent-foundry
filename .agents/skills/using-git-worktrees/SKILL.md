---
name: using-git-worktrees
description: Parallel development with git worktrees — isolate branches into separate working directories so multiple features or hotfixes can be developed simultaneously without stashing or context switching.
origin: meridian
---

# Using Git Worktrees

Git worktrees let you check out multiple branches simultaneously in separate directories — no stashing, no context switching. Invoke this skill on demand when you need parallel branch isolation.

## When It's Useful

- Working on a new feature while another branch is already in progress
- Applying a hotfix without interrupting an ongoing feature
- Running tests on branch A while developing branch B
- Delegating a task to a Claude Code agent with full branch isolation (`isolation: "worktree"`)

## Conventions

### Directory Layout

All worktrees are created in a sibling directory `.worktrees/` next to the repo root:

```
~/projects/
├── meridian/              ← main working tree (main branch)
└── .worktrees/
    ├── meridian-feat-auth/    ← feature/auth branch
    └── meridian-hotfix-login/ ← hotfix/login branch
```

### Naming Rule

```
<repo-name>-<branch-name>
```

Replace `/` in branch names with `-`:
- `feature/auth` → `meridian-feat-auth`
- `hotfix/login-null` → `meridian-hotfix-login-null`

This makes `ls ../.worktrees/` immediately readable without needing to remember which directory maps to which branch.

## Workflow

### 1. Create a Worktree

```bash
# Create a new branch and worktree simultaneously
git worktree add ../.worktrees/meridian-feat-auth -b feature/auth

# Or check out an existing branch
git worktree add ../.worktrees/meridian-feat-auth feature/auth
```

### 2. List Active Worktrees

```bash
git worktree list
```

Output example:
```
/Users/you/projects/meridian                          abc1234 [main]
/Users/you/projects/.worktrees/meridian-feat-auth     def5678 [feature/auth]
```

### 3. Work in the Worktree

Open a separate editor window pointing to the worktree directory, or use Claude Code agents with `isolation: "worktree"` for fully automated isolation.

Each worktree is an independent working directory with its own:
- Staged files and index
- Unstaged changes
- HEAD pointer

### 4. Remove a Worktree When Done

```bash
# After merging or abandoning the branch
git worktree remove ../.worktrees/meridian-feat-auth

# Force remove if the worktree has untracked changes you want to discard
git worktree remove --force ../.worktrees/meridian-feat-auth

# Prune stale worktree metadata
git worktree prune
```

## Rules

### Commit Operations Must Be Serial

Git's index lock prevents two worktrees from staging or committing simultaneously. Never run `git add` or `git commit` in two different worktrees at the exact same time. File editing, test execution, and formatting can all run in parallel — only the git staging/commit step must be sequential.

### Pre-commit Hooks Run Per Worktree — This Is Correct

Each worktree runs its own pre-commit hooks on commit. This is the intended behavior: every branch gets independently validated before its changes are committed. If hooks feel slow, optimize them to run only on staged files — do not disable them.

### IDE: Use Separate Windows Per Worktree

Open each worktree as its own project window in Cursor or VS Code. Do not try to manage multiple worktrees from a single editor window — each worktree is effectively a separate project.

### Claude Code Agent Isolation

When delegating a task to a Claude Code agent, pass `isolation: "worktree"` to the Agent tool. The agent will operate in a fresh worktree, and the worktree is automatically cleaned up if no changes are made:

```
Agent tool: isolation = "worktree"
```

This is the recommended approach for agent-driven parallel tasks.

## Pass Criteria

A worktree workflow is set up correctly when:

- [ ] Worktree directory is under `../.worktrees/` with the correct naming convention
- [ ] `git worktree list` shows the expected branches
- [ ] Each active worktree has its own editor window or agent context
- [ ] Commit operations are not being run concurrently across worktrees
- [ ] Completed worktrees are removed and pruned

## Quick Reference

```bash
# Create
git worktree add ../.worktrees/<repo>-<branch> -b <branch-name>

# List
git worktree list

# Remove
git worktree remove ../.worktrees/<repo>-<branch>

# Prune stale entries
git worktree prune
```
