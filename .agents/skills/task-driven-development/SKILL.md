---
name: task-driven-development
description: 标准开发流程的执行引擎。按任务粒度执行 TDD + 审查循环。
---

# 任务驱动开发

标准开发流程的执行引擎。非降级场景默认使用。

---

## Phase 0：环境就绪检查

从计划的"Environment Prerequisites"段读取依赖清单，逐项验证：

1. 执行每项的 **Verify** 命令，收集结果
2. 全部通过 → 进入 Phase 1
3. 有失败 → 列出失败项 + 错误输出 + 计划中的 Suggested Fix → 阻塞等待用户手动处理 → 用户确认后重验 → 全部通过才继续

**不自动执行 Fix 命令。环境准备是用户的责任。**

---

## Phase 1：加载与校验

1. 读取计划文件（`docs/plans/`）
2. 提取所有任务文本
3. 检查粒度：每任务 1-3 文件，有独立 TDD 步骤和审查门控
4. 如果任务涉及 UI，实现前确认计划已引用：
   - `DESIGN.md`（如存在）
   - `docs/designs/<feature>/review-verdict.md`
   - `docs/designs/<feature>/tokens/`
   - `docs/designs/<feature>/components/*.md`
   - 已记录的 design identity gap 及其用户决策
5. 不合格 → 报告用户，建议重新拆分

---

## Phase 2：逐任务执行循环

对每个任务顺序执行以下步骤：

### Step 1：调度 tdd-guide（Task Executor Mode）

通过 Agent tool 调度 `tdd-guide` 子代理：

- 粘贴完整任务文本到 prompt，不让子代理读计划文件（上下文隔离）
- 子代理执行：TDD RED→GREEN→IMPROVE
- 等待状态报告

| 状态 | 处理 |
|------|------|
| DONE | → Step 2 |
| DONE_WITH_CONCERNS | 记录关注点，→ Step 2 |
| BLOCKED | 报告用户，拆分或补充上下文 |
| NEEDS_CONTEXT | 补充信息，重新调度 |

### Step 2：质量门控

tdd-guide 完成后，调用 `/code-quality-gate` skill：

- 格式化（ruff format / prettier）
- Lint（ruff check / eslint）
- 类型检查（mypy / tsc --noEmit）
- Debug 产物检测（console.log / print / debugger）

全项通过 → Step 3。有失败 → 修复后重跑质量门控。

### Step 3：规格合规审查

调度 `code-reviewer`，对照原始任务要求：是否完成全部要求、是否遗漏边界条件、是否偏离范围。

UI 任务额外检查：

- 是否使用 semantic tokens，而不是硬编码颜色、圆角、阴影、字体等视觉值
- 是否避免 arbitrary Tailwind 作为常规样式方案
- 是否符合组件契约、`review-verdict.md` 和 DESIGN.md（如存在）
- 是否补齐缺失 token / 设计契约，而不是在实现层临时绕过
- 是否产出 Playwright 视觉回归和 axe 可访问性验证结果（适用于可运行前端）

### Step 4：代码质量审查

规格合规通过后，调度 `code-reviewer` 做标准质量审查。安全敏感代码加 security-reviewer；Python 加 python-reviewer；TS 加 typescript-reviewer。

### Step 5：门控判定

通过 → Step 6。未通过 → 修复 → 回到 Step 2 重新质量门控和审查。

### Step 6：Commit

调用 `/commit-quality` skill 提交当前任务。commit 后 → 下一任务。

---

## Phase 3：整体审查

所有任务完成后，调度 `code-reviewer` 做整体审查：任务间集成一致性、遗漏的全局性问题。

---

## Phase 4：最终确认

- [ ] 测试覆盖率 >= 80%
- [ ] 无残留调试产物
- [ ] commit 符合 Conventional Commits
- [ ] docs/plans/ 已清理

---

## 反逃避机制

**NEVER：** 跳过任务 TDD 循环 / 跳过质量门控 / 合并多任务审查 / 审查未通过就下一任务 / 让子代理读计划文件 / 自行判定"太简单不需要 TDD" / 批量写测试或批量实现

**Red Flags：** 跳过审查的理由是"改动小" / 多任务合并审查 / 子代理状态不明确 / 先实现后补测试 / 问题标记为"后续处理"

→ 出现任何 Red Flag → 停止，当前任务重新开始。

---

## 模型选择

| 步骤 | 模型 | 原因 |
|------|------|------|
| 任务执行（tdd-guide） | sonnet | 速度快 |
| 规格合规审查 | sonnet | 对照检查，无需深度推理 |
| 代码质量审查 | opus | 需要深度理解 |
| 整体审查 | opus | 跨任务集成分析 |

---

## 无子代理时的回退

主会话顺序执行每任务 TDD 循环：写测试 → RED → 实现 → GREEN → 重构 → 质量门控 → code-reviewer → commit。逐任务串行，不跳跃。

---

## 关键原则

- **隔离**：每任务独立上下文
- **串行**：任务间严格顺序
- **门控**：每任务必须通过 TDD + 质量门控 + 审查
- **当场修复**：审查问题不拖延
