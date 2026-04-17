# Git 工作流

## Commit Message 格式

```
<type>: <description>

<optional body>
```

类型：feat, fix, refactor, docs, test, chore, perf, ci

注：署名已通过 `~/.claude/settings.json` 全局禁用。

## Pull Request

- 合并时：`gh pr merge <pr-number> --squash --delete-branch`
- 新分支推送：使用 `-u` 标志

→ git-workflow skill
