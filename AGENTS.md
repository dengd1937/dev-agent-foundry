# AGENTS

`dev-agent-foundry` 的总入口文档。

这个仓库的目标，是沉淀一套可跨项目、跨工具复用的 dev-agent 资产，让 Claude Code、Codex、Cursor、Trae 等工具都可以围绕同一批共享能力协作。

## 导航

### 1. 共享 Skill 真源

共享 skill 统一维护在 `.agents/skills/`。

这里的 skill 设计目标是：

- 新项目可直接复制或同步使用
- 尽量保持自包含
- 不依赖单一工具私有格式

### 2. 规则层

`rules/` 用于沉淀默认应遵守的规则，优先参考 `everything-claude-code` 的组织方式。

当前第一批通用规则已经落在 `rules/common/`，后续再按语言或技术栈扩展。

规则层回答的是：

- 应该遵守什么
- 默认流程是什么
- 代码、测试、review、安全等方面的最低约束是什么

当前入口：

- [rules/common/coding-style.md](rules/common/coding-style.md)
- [rules/common/documentation.md](rules/common/documentation.md)
- [rules/common/configuration.md](rules/common/configuration.md)
- [rules/common/git-workflow.md](rules/common/git-workflow.md)
- [rules/common/testing.md](rules/common/testing.md)
- [rules/common/code-review.md](rules/common/code-review.md)
- [rules/common/security.md](rules/common/security.md)
- [rules/common/agents.md](rules/common/agents.md)

当前语言层入口：

- [rules/python/coding-style.md](rules/python/coding-style.md)
- [rules/python/testing.md](rules/python/testing.md)
- [rules/python/security.md](rules/python/security.md)
- [rules/python/patterns.md](rules/python/patterns.md)

### 3. 工具适配层

工具适配目录包括：

- `.claude/`
- `.cursor/`
- `.trae/`

这些目录只负责接入层，不应成为共享 skill 的真源。

当前默认做法是：

- `.claude/skills -> ../.agents/skills`
- `.cursor/skills -> ../.agents/skills`
- `.trae/skills -> ../.agents/skills`

### 4. 使用优先级

建议遵循以下优先级：

1. 项目自己的明确规则
2. 本仓库 `rules/common/` 中的通用规则
3. 本仓库语言层规则，例如 `rules/python/`
4. `.agents/skills/` 中的任务执行协议
5. 工具自身默认行为

当项目私有规则与通用规则冲突时，优先项目私有规则。

## 当前仓库结构

```text
dev-agent-foundry/
├── AGENTS.md
├── .agents/
│   └── skills/
├── rules/
│   ├── common/
│   └── python/
├── .claude/
├── .cursor/
└── .trae/
```

## 后续方向

- 继续扩展 `rules/common/` 的覆盖面，并逐步沉淀语言或技术栈专属规则
- 继续保持 `.agents/skills/` 的开箱即用属性
- 再视成熟度补充更多工具适配说明
