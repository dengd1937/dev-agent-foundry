# Agent 编排

## 可用 Agent

| Agent | 用途 |
|-------|------|
| planner | 实现方案规划 |
| tdd-guide | 测试驱动开发 |
| code-reviewer | 代码审查（commit 前强制） |
| security-reviewer | 安全分析（auth/输入/支付相关强制） |
| refactor-cleaner | 清理死代码 |
| docs-lookup | Context7 查文档 |
| python-reviewer | Python 代码审查 |
| typescript-reviewer | TypeScript/React 代码审查 |
| e2e-runner | 浏览器 E2E 测试 |
| design-reviewer | 设计产物审查 |

## 关键 Skill

| Skill | 用途 | 触发方式 |
|-------|------|---------|
| investigate | 根因分析 | bug 修复前 |
| ideate | 产品想法细化 | `/ideate` |
| design-review | 方案对抗性审查 | planner 之后、实现前 |
| retro | 任务后复盘 | 功能/修复完成后 |

## 执行原则

- **独立操作并行执行**，有依赖的才串行
- **复杂问题可用分角色子 agent**（事实审查、工程、安全、一致性、冗余检查）
