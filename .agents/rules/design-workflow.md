# 设计工作流（路由）

> 完整流程在 `design-workflow` skill 中，按需加载。

## 激活条件

| 激活 | 跳过 |
|---|---|
| 新 UI 功能 / 页面 / 组件 / 视觉改动 | 纯后端 / 配置 / 文档修改 |
| 新 token / 新交互模型 | 无视觉变化的重构 |
| 涉及 `docs/designs/`、`.pen`、Pencil MCP | 不涉及 UI |

## L1 vs L2 路由

- **L1（轻量）**：无新 token、无新组件、无新页面、无新交互 → 加载 `design-workflow` skill L1
- **L2（标准）**：其他所有 UI 工作 → 加载 `design-workflow` skill V2-1 到 V2-5

L2 Gate 3 通过后的产物（intent.md、screenshots/、components/、tokens/）进入 development-workflow。开发时通过 Pencil MCP 实时读取设计属性。

## 文档维护

设计工作流（L1 或 L2）完成后：
→ doc-updater agent 更新 component catalog 和 feature catalog
