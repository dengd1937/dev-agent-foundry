---
name: git-workflow
description: |
  交付类工作流 skill。用于在用户要求提交代码、推送远端、创建 PR、继续跟 CI、推进合并时，按仓库 Git/PR 规范执行完整流程，而不是停在中间步骤。

  当用户提到"commit""push""提交到远端""创建 PR""继续处理 CI""推进合并"等交付动作时触发。
---

# Git Workflow

> 本 skill 将仓库的 Git/PR 规范转成执行工作流。目标不是复述规则，而是确保交付类请求按既定门禁推进到下一稳定状态。

## 何时使用

以下任一场景应使用本 skill：

- 用户要求 `commit`、`push`、`提交到远端`
- 用户要求创建或继续推进 PR
- 用户要求等待 CI、处理 CI 失败、推进到可合并
- 用户要求继续某个已有 commit / 分支 / PR 的交付流程

以下场景通常不需要单独触发：

- 纯代码解释、架构讨论
- 只修改本地文件、明确不涉及交付

## 核心原则

- 默认采用 PR 工作流，**禁止直接 push 到主分支**（`main` / `master`）
- 交付类请求的默认完成态不是 `push`，也不是"PR 已创建"，而是：
  - 已进入正确分支/PR 流程
  - CI 和必要 review 已处理到当前可推进的稳定状态
- 除非用户明确要求停在某一步，否则不能在中间步骤提前结束
- 当前 CI 只负责基础质量门禁，不再负责校验 reviewer 结果或 PR 模版中的自审内容
- 本地 reviewer 是默认协作流程，但 reviewer 结果不作为 CI 强制门禁

### 补充规则来源

如果项目中存在以下文档，应优先参照：

- Git 流程文档（如 `docs/devops/git_workflow.md` 或类似路径）
- 本地 reviewer 规范（如 `docs/devops/local_independent_reviewer.md`）
- reviewer 请求模板（如 `docs/devops/review_request_template.md`）

相关 skill：

- 可选本地自审：`self-review`
- 独立 reviewer 协议：`code-review-expert`

## 执行流程

### Step 1：确认当前交付阶段

先识别用户要推进到哪一步：

- 本地提交前：需要开发、本地验证、必要时 reviewer
- 远端交付：需要分支、push、PR
- PR 跟进：需要等待 CI、读取反馈、修复后再推
- 合并收口：需要确认门禁通过并完成 merge

如果用户只给了模糊请求，例如"提交到远端"，默认按完整交付流程推进，而不是只执行一次 `git push`。

### Step 2：检查仓库状态与约束

至少检查：

```bash
git status --short --branch
git branch --show-current
git remote -v
```

必要时继续检查：

- 当前是否在主分支（`main` / `master`）
- 工作区是否有未提交变更
- 是否已有对应 PR
- 当前请求是否会触发 PR 工作流

若当前在主分支且需要远端交付：

- 不要直推
- 创建符合规范的工作分支后继续

### Step 3：完成与任务对应的本地验证

按以下规则判断：

- 代码改动、配置、脚本、CI、依赖、部署、行为性文档改动：至少运行与任务对应的本地验证
- 纯说明性文档改动：可走轻量路径
- 只有用户明确要求额外本地自审时，才额外运行 `self-review`

如果关键本地验证尚未完成：

- 先补验证
- 不要直接进入 commit / push

### Step 4：判断是否需要独立 reviewer

按以下规则判断：

- 代码改动：默认需要独立 reviewer
- 高风险配置、流程、架构、行为性文档改动：默认需要独立 reviewer
- 纯说明性文档改动：通常可跳过

当前默认独立 reviewer 是本地新会话的 `code-review-expert`。

reviewer 结果应直接通过 GitHub PR review 或 PR comment 回写到当前 PR，而不是在 Author / Reviewer 两个会话中复制粘贴。
这里要求的独立性是"新开 Agent 会话"的流程隔离，不要求 reviewer 使用不同 GitHub 账号。

当进入独立 reviewer 路径时，当前 Author 会话必须明确提醒：

```markdown
下一步需要执行独立 reviewer 审查。

请新开一个 Agent 会话窗口，并使用 `code-review-expert` 对当前变更做独立审查。
不要在当前 Author 会话里继续 review 自己的改动。
reviewer 完成后，请直接把结构化结论提交为当前 PR 的 review，而不是回复到聊天窗口。
若 GitHub 因 reviewer 与 PR 作者同账号而拒绝 `--approve` / `--request-changes`，可退化为 `COMMENT` review，但 body 中仍需明确 `Overall assessment`。

建议提供给 reviewer 的材料：
- 当前 `git diff --stat`
- 当前 `git diff`
- 本地验证结果
- 已知风险 / 未覆盖项

如果项目中有 reviewer 请求模板，可直接使用。
```

除非用户明确要求忽略，否则当前会话不得在同一上下文中充当独立 reviewer。

### Step 5：提交并推送到正确分支

如果已经满足提交前门禁，再执行：

```bash
git add <relevant-files>
git commit -m "<type>: <description>"
git push origin <branch-name>
```

执行前再确认一次：

- 不会直推主分支
- 不会把与当前任务无关的本地改动一并提交

### Step 6：创建或继续推进 PR

如果仓库采用 PR 工作流，`push` 后必须继续判断：

- 用户是否明确要求停在 `push`
- 是否已经存在对应 PR

若没有"停在 push"的明确要求：

- 无 PR：创建 PR
- 已有 PR：继续跟进现有 PR

PR 描述至少应包含：

- 改动目标
- 关键变更点
- 本地验证方式
- reviewer 需要的上下文（可选）
- 遗留风险

如果项目中存在 PR 模版（如 `.github/pull_request_template.md`），应优先使用。

### Step 7：等待 CI 并处理反馈

创建或定位到 PR 后，默认继续等待并检查：

- CI 状态
- review comments
- reviewer findings

等待规则：

- `queued`、`pending`、`in_progress` 都不算完成
- 默认持续等待，直到出现终态
- 超过 15 分钟仍未终态时，只能向用户同步中间进度，不能宣称流程完成

若出现失败或 feedback：

1. 修复问题
2. 重跑相关本地验证
3. 必要时再次发起独立 reviewer
4. 重新 push
5. 继续等待 CI / review

### Step 8：收口条件

只有满足以下任一条件，才可以把交付类请求视为当前阶段完成：

1. 用户明确要求停在某个中间步骤
2. PR 已达到可合并状态，且已向用户同步结果
3. PR 已合并
4. CI / review 长时间未到终态，已向用户明确说明当前仍在等待中

禁止把以下状态误判为完成：

- 分支已推送
- PR 已创建
- CI 已触发但仍在排队

## 输出要求

处理交付类请求时，优先同步"当前处于哪一步、下一步是什么"，例如：

- 当前已完成本地验证，下一步需要新开会话执行 reviewer
- 当前 reviewer 已把结果写回 PR，下一步将读取 PR review findings 并决定修复或继续等待
- 当前已 push 分支，下一步将创建 PR
- 当前 PR 已创建，正在等待 CI
- 当前 CI 失败，下一步将修复并重跑验证

若流程未结束，不要把中间进度描述成"已完成"。

## 失败与升级条件

命中以下任一情况时，不要继续盲推：

- 关键本地验证未通过
- 独立 reviewer 给出 `REQUEST_CHANGES`
- 当前分支或提交范围不清晰
- PR / CI 状态无法确认
- 远端规则与本地预期冲突

命中以下情况时，建议升级为人工判断：

- 权限、认证、敏感数据、外部系统关键链路改动
- reviewer / CI 出现难以解释的异常
- 需求本身仍存在歧义，无法仅靠代码与文档判断
