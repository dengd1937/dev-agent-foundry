# Git Workflow

> 本文档定义跨项目通用的 Git / PR 交付规则。
> 具体执行步骤优先由 `git-workflow` skill 落地；本文只保留规则、门禁与完成态定义。

## 核心原则

- 默认采用 **Pull Request 模式**，代码变更应通过工作分支和 PR 进入主分支
- **禁止直接 push 到主分支**，例如 `main` 或 `master`
- 用户请求“提交代码”“提交到远端”“创建 PR”等交付动作时，默认目标是推进完整交付链路，而不是只执行单个 Git 命令
- `push` 不是完成态；`PR 已创建` 通常也不是完成态
- 只有在实现、验证、必要审查都完成后，才进入 Git / PR 交付阶段

开发前的完整流程见 [development-workflow.md](./development-workflow.md)。

## 分支与提交

推荐使用工作分支交付，例如：

```bash
git checkout -b <type>/<short-description>
```

常见分支前缀：

| 前缀 | 用途 | 示例 |
|---|---|---|
| `feature/` | 新功能 | `feature/add-metrics-endpoint` |
| `fix/` | Bug 修复 | `fix/dedup-race-condition` |
| `refactor/` | 重构 | `refactor/simplify-config` |
| `docs/` | 文档 | `docs/update-readme` |
| `chore/` | 杂项 | `chore/update-ci-config` |

提交规则：

- 远端交付前应位于符合团队约定的工作分支
- 若当前在主分支，不应直接推送；应先创建工作分支
- commit message 应采用项目约定格式；若项目未定义，推荐使用 `<type>: <description>`
- 不应把与当前任务无关的本地改动混入同一次提交

## 提交前门禁

在执行 `commit` 前，至少确认：

- 已完成 [development-workflow.md](./development-workflow.md) 中要求的研究、规划、验证和审查
- 已明确本次改动要解决的问题、成功标准和主要回归风险
- 已完成与改动范围匹配的本地验证
- 已同步更新受影响的注释、文档、配置说明和测试
- 若改动风险较高、跨度较大或涉及关键链路，已完成必要的独立 review

纯说明性文档改动可走轻量路径；会影响流程、配置、部署、排障、验收标准或 agent 行为的行为性文档改动，应补充最小验证摘要。

## 独立 Reviewer 协作

以下情况默认建议发起独立 reviewer：

- 生产代码、测试、脚本、配置、依赖、CI、部署改动
- Bug 修复、跨模块重构、外部系统集成改动
- 会影响行为、流程、配置、排障或验收标准的文档改动

协作规则：

1. Author 先完成本地改动与最小必要验证
2. Author 创建或更新 PR
3. Author 新开一个 Agent 会话执行 `code-review-expert`
4. reviewer 基于 PR diff、关键文件和本地验证摘要输出 findings
5. reviewer 结果应直接回写到 PR review 或 PR comment
6. Author 读取 findings，修复后继续 push / 更新 PR

执行约束：

- 当前 Author 会话不得在同一上下文中充当独立 reviewer
- 这里要求的是“新开 Agent 会话”的流程独立性，不要求 reviewer 使用不同 GitHub 账号
- reviewer 结果默认作为协作信息，不由 CI 自动阻塞或放行

## Pull Request 规则

- 对采用 PR 工作流的仓库，`push` 后应继续判断是否需要创建或更新 PR
- 若用户未明确要求停在某个中间步骤，应继续推进到 `PR -> CI -> 处理反馈` 的下一稳定状态
- 若仓库已有 PR 模版，应直接使用，而不是另起一套格式

PR 描述至少应包含：

- 改动目标
- 关键变更点
- 本地验证方式
- reviewer 需要优先关注的上下文（可选）
- 仍存在的风险或未覆盖项（可选）

## CI 与反馈处理规则

- 创建或更新 PR 后，应继续进入 CI 阶段，而不是把 `push` 或 `PR 已创建` 误判为完成
- CI 的具体检查项、失败分类和处理口径，统一以 [ci-workflow.md](./ci-workflow.md) 为准
- 若仓库维护 required checks、branch protection 或合并策略，应遵循仓库现有设置，而不是临时发明新门禁

若 CI 或 reviewer 提出问题，应循环执行：

1. 修复问题
2. 重跑相关本地验证
3. 必要时再次发起独立 reviewer
4. 重新 push 分支或更新 PR

## 人类介入时机

以下情况建议升级为人工判断：

- 权限、认证、敏感数据、外部系统关键链路改动
- reviewer 指出了高风险问题，但证据不足以自动判断
- 修复轮次过多，问题长期不收敛
- 需求本身仍有歧义，无法仅靠代码与文档判断

## 禁止事项

- 禁止直接 push 到主分支
- 禁止把“提交到远端”理解成允许直推受保护分支
- 禁止跳过 CI 或关键反馈直接宣布交付完成
- 禁止把“分支已推送”或“PR 已创建”误判为交付完成，除非用户明确要求停在该步骤
- 禁止在当前 Author 会话中直接充当独立 reviewer

## 完成态定义

交付类请求通常只有满足以下任一条件，才可视为当前阶段完成：

1. 用户明确要求停在某个中间步骤
2. PR 已达到可推进的稳定状态，且已向用户同步结果
3. PR 已合并
4. CI 或 reviewer 长时间未到终态，且已明确向用户同步“仍在等待中”

以下状态通常都不算完成：

- 分支已推送
- PR 已创建
- CI 已触发但仍在排队或运行中

## Agent 执行入口

- 涉及 `commit`、`push`、创建 PR、等待 CI、推进合并等交付动作时，优先使用 `git-workflow`
- 独立 reviewer 协议由 `code-review-expert` 负责

## Commit Message 格式

```text
<type>: <description>

# 示例
feat: add webhook receiver endpoint
fix: resolve dedup race condition
refactor: simplify config loading
docs: update README deployment section
chore: update ci configuration
```

常见 type：

| type | 说明 |
|---|---|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构（不改变功能） |
| `docs` | 文档变更 |
| `chore` | 杂项（CI、配置等） |
| `test` | 测试相关 |
| `style` | 代码格式（不影响逻辑） |
