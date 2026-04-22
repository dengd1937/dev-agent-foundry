# 开发工作流

## 铁律（IRON LAWS）

铁律 1：每一个任务独立走 TDD → 实现 → 审查循环。不允许"实现所有文件后统一审查"。
铁律 2：降级必须用户明确批准。模型不可自主判定"简单"并跳过流程。
铁律 3：没有通过审查的代码，不允许 commit（hook 硬阻塞）。

## 路由原则

**默认走任务驱动流程。** 执行中根据反馈动态调整：

- **降级**：改动仅涉及 1 个文件，且用户明确确认降级。模型必须向用户展示："请求降级到简化流程。理由：[具体理由]。确认？" 并等待响应。涉及 >=2 个文件的改动不允许降级。
- **架构级浮现**：调研或阅读代码时发现需要架构决策（不限于新模块/新依赖，也包括重构中浮现的边界问题）→ 停下规划，建议使用者执行 `/architect`；是否触发由使用者和模型共同判断，不设硬规则

## 任务驱动流程

### 前置：调研与规划

1. **调研与复用** — 阅读已有产物（`docs/product/`、`docs/designs/`）；搜索现有实现；优先成熟库
   - UI 任务必须额外读取：项目根目录 `DESIGN.md`（如存在）、`docs/designs/<feature>/review-verdict.md`、`docs/designs/<feature>/tokens/`、`docs/designs/<feature>/components/*.md`
   - 如果设计产物记录了 design identity gap，计划阶段必须说明采用“收敛设计”还是“等待用户更新 DESIGN.md”
2. **规划** → planner agent → 输出任务级计划（每任务 1-3 文件）→ 保存至 `docs/plans/` → **用户批准前不写代码**

### 循环：逐任务执行

对计划中的每个任务，重复以下步骤。每个任务完成后才能进入下一个任务。

3. **TDD** → tdd-guide agent → RED→GREEN→IMPROVE → 覆盖率 80%+
   - UI 实现不得绕过设计 token：禁止硬编码颜色、圆角、阴影、字体等视觉值，禁止使用 arbitrary Tailwind 作为常规方案
   - UI 实现必须保持组件契约和 DESIGN.md（如存在）一致；发现缺失 token 或契约缺口时回到设计产物补齐
4. **质量门控** → code-quality-gate skill → 格式化 + lint + 类型检查
5. **代码审查** → code-reviewer agent（Python 项目加 python-reviewer agent；TS 项目加 typescript-reviewer agent；安全相关加 security-reviewer agent）
   - UI 任务审查必须检查 semantic token 使用、组件契约一致性、DESIGN.md 约束继承、Playwright 视觉回归和 axe 可访问性验证

不允许跨任务合并审查。不允许"实现所有文件后统一审查"。

→ task-driven-development skill（编排细节）

### 收尾

6. **文档** — 删除 `docs/plans/`；模块文档 → doc-writer agent 模板：`module-doc`；完成后 → doc-updater agent 更新模块索引和 codemap
7. **Commit** → commit-quality skill → Conventional Commits → 禁止 `--no-verify`
8. **预审查** — CI/CD 通过、冲突已解决、分支已同步

## 降级流程

质量门控 → Commit。跳过其他所有步骤。降级仅限单文件改动，且必须用户明确确认。
