# dev-agent-foundry — Agent Instructions

这是 `dev-agent-foundry` 的总入口文档。这个仓库的目标，是沉淀一套可跨项目、跨工具复用的 dev-agent 资产，让 Claude Code、Codex、Cursor、Trae 等工具围绕同一批共享 `rules` 与 `skills` 协作。

## Core Principles

1. **Rules First** — 先读规则，再执行任务
2. **Skill as Protocol** — skill 负责执行协议，rules 负责默认约束
3. **Plan Before Execute** — 复杂改动先规划，再实现
4. **Test-Driven** — 默认采用 `RED -> GREEN -> REFACTOR`
5. **Security-First** — 输入校验、敏感信息处理、权限边界优先
6. **Cross-Tool Reuse** — 共享资产不绑定单一工具私有格式

## Available Skills

共享 skill 真源统一维护在 `.agents/skills/`。

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `git-workflow` | Git / PR / CI 交付协议 | 提交、推送、创建 PR、跟进 CI、推进合并 |
| `code-review-expert` | 独立 reviewer 协议 | 需要 findings-first 的结构化代码审查 |
| `design-review` | 设计评审 | 方案、架构、边界、可维护性评估 |
| `doc-gardening` | 文档治理 | 检查并修复文档与代码、规则、目录的漂移 |
| `self-review` | 作者本地自审 | 需要额外自查时使用，不属于默认流程 |
| `python-patterns` | Python 开发模式 | 编写、重构、审查 Python 代码 |
| `django-security` | Django 安全实践 | Django 认证鉴权、部署、安全审查 |
| `python-testing` | Python 测试策略 | pytest、TDD、fixtures、mock、覆盖率 |

## Rule Navigation

`rules/` 用于沉淀默认应遵守的规则，优先参考 `everything-claude-code` 的组织方式。

### Common Rules

- [rules/common/development-workflow.md](rules/common/development-workflow.md)
- [rules/common/coding-style.md](rules/common/coding-style.md)
- [rules/common/patterns.md](rules/common/patterns.md)
- [rules/common/performance.md](rules/common/performance.md)
- [rules/common/security.md](rules/common/security.md)
- [rules/common/testing.md](rules/common/testing.md)
- [rules/common/git-workflow.md](rules/common/git-workflow.md)
- [rules/common/ci-workflow.md](rules/common/ci-workflow.md)

### Python Rules

- [rules/python/coding-style.md](rules/python/coding-style.md)
- [rules/python/patterns.md](rules/python/patterns.md)
- [rules/python/security.md](rules/python/security.md)
- [rules/python/testing.md](rules/python/testing.md)

默认导航顺序：

1. 先从 [rules/common/development-workflow.md](rules/common/development-workflow.md) 进入开发主流程
2. 涉及通用编码约束时，读取 [rules/common/coding-style.md](rules/common/coding-style.md)
3. 涉及设计模式、性能、安全、测试时，读取对应 `common` 主题文档
4. 涉及 Python 项目时，再叠加读取 `rules/python/`
5. 进入提交、推送、PR、review、合并阶段后，切到 [rules/common/git-workflow.md](rules/common/git-workflow.md)
6. 进入 CI 检查阶段后，参考 [rules/common/ci-workflow.md](rules/common/ci-workflow.md)

## Development Workflow

默认开发主线：

1. **Research & Reuse** — 先查已有实现、模板、文档和成熟方案
2. **Plan First** — 复杂改动先规划依赖、风险和阶段
3. **TDD Approach** — 先写失败测试，再最小实现，再重构
4. **Commit & Push** — 进入交付阶段后遵循 `git-workflow`

## Git Workflow

- 默认采用 **Pull Request** 工作流
- **禁止直接 push 到主分支**
- `push` 不是完成态，`PR 已创建` 也通常不是完成态
- 提交、推送、PR、CI、merge 等交付动作，优先使用 `git-workflow`
- 需要独立 reviewer 时，优先使用 `code-review-expert`

## Security Baseline

- 禁止硬编码 secret、token、密码和密钥
- 所有外部输入都应视为不可信，并在边界层校验
- 数据库访问默认使用参数化查询或等价防注入方式
- 错误信息与日志不得泄露敏感数据
- 发现安全问题时，先停止推进交付，再修复高风险项

## Coding Style

- 默认优先不可变更新，避免随意原地修改
- 文件保持高内聚、低耦合；过大文件应主动拆分
- 错误必须显式处理，禁止静默吞错
- 输入校验应前置到系统边界
- 代码命名应直接表达意图，优先可读性而不是技巧性

## Testing Requirements

- 默认目标覆盖率不少于 `80%`
- 单元测试、集成测试、端到端测试都应具备
- 默认采用 `RED -> GREEN -> REFACTOR`
- 测试失败时先检查隔离性、mock、fixture 和实现，不要直接改断言

## Tool Adapters

工具适配目录：

- `.claude/`
- `.cursor/`
- `.trae/`

这些目录只负责接入层，不应成为共享 skill 的真源。当前默认做法是：

- `.claude/skills -> ../.agents/skills`
- `.cursor/skills -> ../.agents/skills`
- `.trae/skills -> ../.agents/skills`

## Priority Order

当规则冲突时，遵循以下优先级：

1. 项目自己的明确规则
2. 项目级 Agent 入口文档
3. 本仓库语言层规则，例如 `rules/python/`
4. 本仓库 `rules/common/`
5. `.agents/skills/` 中的任务执行协议
6. 工具自身默认行为

当项目私有规则与通用规则冲突时，优先项目私有规则。

## Project Structure

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

## Success Criteria

- 规则层和 skill 层职责清晰，不混杂
- 共享 skill 可直接被新项目复制或同步使用
- 规则可被不同编程工具稳定消费
- 开发、测试、交付和安全流程有统一入口
