# 开发工作流

## 路由原则

**默认走标准流程。** 执行中根据反馈动态调整：

- **降级为简单**（跳过调研/规划/TDD/审查）：你能从用户请求直接看出改什么、怎么改，无需设计决策。例如 typo、重命名、配置值变更、明显的 lint 修复。
- **升级为复杂**（走完整 8 步）：执行中发现修改范围超出预期、需要架构层面的选择、或需求比初始理解更模糊。这时停下先规划。

## 标准流程

1. **调研与复用** — 阅读已有产物（`docs/product/`、`docs/designs/`）；搜索现有实现；优先成熟库
2. **规划** → planner agent → 保存至 `docs/plans/` → **用户批准前不写代码**
3. **TDD** → tdd-guide agent → RED→GREEN→IMPROVE → 覆盖率 80%+
4. **质量门控** → code-quality-gate skill → 格式化 + lint + 类型检查
5. **代码审查** → code-reviewer agent（Python 项目加 python-reviewer agent；TS 项目加 typescript-reviewer agent；安全相关加 security-reviewer agent）
6. **文档** — 删除 `docs/plans/`；模块文档 → doc-writer agent 模板：`module-doc`；完成后 → doc-updater agent 更新模块索引和 codemap
7. **Commit** → commit-quality skill → Conventional Commits → 禁止 `--no-verify`
8. **预审查** — CI/CD 通过、冲突已解决、分支已同步

## 简化流程（降级后）

质量门控 → Commit。跳过其他所有步骤。

## 复杂流程（升级后）

完整执行标准流程所有 8 步。升级时先向用户说明原因并展示规划。
