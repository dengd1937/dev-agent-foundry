---
name: code-review-expert
description: |
  独立 reviewer 协议。用于对当前变更执行以 findings 为中心的结构化审查。

  当前默认用于本地 reviewer：在新的 Agent 会话中审查当前 git diff，并通过 PR review 或 PR comment 回写结果。
---

# Code Review Expert

> 本 skill 不负责作者自查，也不默认负责直接改代码。它的职责是作为独立 reviewer，基于 diff、验证证据和仓库约束输出可执行的审查结论。

## 角色定位

- `self-review`：可选的作者本地自查
- `code-review-expert`：reviewer 的审查协议
- 人工 review：高风险、强歧义、证据不足时的升级路径

`code-review-expert` 的目标不是复述作者结论，而是回答：

- 当前改动是否存在会阻塞合并的问题
- 有哪些回归风险、架构问题、安全问题或测试缺口
- 哪些问题必须修，哪些可以作为后续改进

## 适用场景

### 场景 A：本地 reviewer

适用于以下情况：

- 需要在提交前或 PR 阶段执行独立审查
- 需要在 Author agent 之外开启新会话做隔离审查
- 需要将 findings 直接回写到 GitHub PR

要求：

- 尽量在新会话中运行，避免复用 Author agent 的长上下文
- 优先读取客观工件，而不是作者的主观结论
- 当前流程要求的是会话隔离，不要求 reviewer 使用不同 GitHub 账号

### 场景 B：协议复用

本协议可作为未来自动化 reviewer 的协议来源。

要求：

- reviewer 运行在隔离环境中
- 默认只读，不直接改代码
- 结果优先回写为 GitHub PR review

## 审查要求

reviewer 应尽量满足以下条件：

1. 角色隔离
- reviewer 不参与本次实现
- reviewer 默认不直接改代码，先输出 findings

2. 上下文隔离
- 不继承 Author agent 的完整会话历史
- 不把作者的长链路推理直接当作 reviewer 输入

3. 证据优先
- 先看 `git diff`、关键文件、测试结果和本地验证摘要
- 后看作者说明，且作者说明不能替代执行证据

4. 结论独立
- reviewer 必须给出结构化 verdict
- reviewer 的 `REQUEST_CHANGES` 不能被作者在同一轮中自动覆盖

## 输入材料

本地 reviewer 应尽量基于以下工件工作：

- 任务说明：本次改动要完成什么
- `git diff --stat`
- `git diff` 或 PR diff
- 关键文件内容
- 本地验证摘要
- 测试/验证证据摘要
- 可选：CI 结果、日志、截图、接口样例、风险说明

如果输入材料缺失，应明确指出，而不是假设"应该没问题"。

## 审查重点

### 1. 正确性与回归风险

- 改动是否真的实现了目标
- 是否破坏现有行为、接口契约或数据结构
- 是否遗漏边界条件、异常路径和回退逻辑
- 是否存在"测试恰好没覆盖，但实现并不正确"的情况

### 2. 架构与仓库约束

- 是否破坏项目约定的分层架构
- 是否在不应该的位置直接读取环境变量或硬编码配置
- 是否引入不必要耦合、重复逻辑或临时代码
- 是否同步更新相关 docstring、注释、配置文档

如果项目有 Agent 指令文件（如 `CLAUDE.md`、`AGENTS.md`），reviewer 应读取其中的架构约束作为审查依据。

### 3. 安全性与可观测性

- 是否暴露敏感信息、硬编码密钥或不安全默认值
- 是否缺少关键日志上下文或错误定位信息
- 是否引入权限、认证、外部系统调用的风险

### 4. 测试与验证充分性

- 现有测试是否覆盖了实际改动
- 是否缺少对核心风险的直接验证
- 本地验证提供的证据是否足够支撑通过
- CI 通过是否真的代表风险已覆盖

## 严重级别

| Level | Name | 含义 | 动作 |
|-------|------|------|------|
| `P0` | Critical | 安全漏洞、数据破坏、严重正确性问题 | 必须阻塞 |
| `P1` | High | 明显逻辑错误、关键回归风险、关键测试缺失 | 合并前应修复 |
| `P2` | Medium | 可维护性问题、一般性架构问题、非关键测试缺口 | 建议本次修复或记录 follow-up |
| `P3` | Low | 风格、命名、轻微改进建议 | 可选 |

## 审查流程

### 1. 建立审查范围

- 读取项目级 Agent 指令文件和相关设计文档
- 使用 `git status -sb`、`git diff --stat`、`git diff` 或 PR diff 确定范围
- 识别入口点、关键路径、外部依赖和 blast radius

若 diff 很大：

- 先按模块/特性分组
- 优先看高风险部分，而不是平均分配注意力

### 2. 审查验证证据

- 阅读本地验证摘要
- 判断验证计划是否覆盖主要风险
- 检查测试、CI、日志或接口证据是否与任务目标对应

如果存在以下情况，应直接提高严重级别：

- 高风险改动没有对应验证
- 关键测试未运行或失败
- 本地验证结论与执行证据不匹配

### 3. 审查代码与设计

- 查找 correctness、架构、安全、可维护性问题
- 必要时使用 `rg` 查调用方、模型字段、配置来源和关键路径
- 对每个高优先级 finding，说明影响面和触发条件

### 4. 输出结构化结论

- 先列 findings，后写总结
- 没有 findings 时，要明确说明检查范围和残余风险
- 默认不给出"直接改代码"的动作，除非用户明确要求

## 输出格式

必须使用 findings-first 格式：

~~~markdown
## Code Review Summary

**Review mode**: local-reviewer
**Scope**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]
**Evidence checked**: <diff / tests / docs / logs ...>

## Findings

### P0 - Critical
(none or list)

### P1 - High
1. **[path:line]** 标题
   - 问题描述
   - 风险或影响
   - 修复方向

### P2 - Medium
2. **[path:line]** 标题
   - 问题描述
   - 修复方向

### P3 - Low
...

## Open Questions

- 若无则写 `None`

## Residual Risks

- 若无则写 `None`
~~~

### Clean review 规则

如果未发现 findings，必须明确说明：

- 审查了哪些内容
- 哪些内容未覆盖
- 仍然存在什么残余风险

禁止只写：

- `LGTM`
- `Looks good`
- `没问题，可以合并`

## Verdict 规则

- `APPROVE`
  - 未发现阻塞性 findings
  - 审查证据基本充分

- `COMMENT`
  - 有建议，但不阻塞当前合并

- `REQUEST_CHANGES`
  - 存在 `P0` / `P1`
  - 或关键信息、关键验证缺失，无法合理放行

## 与当前流程的关系

- 当前默认用于本地 reviewer
- 由 Author agent 在完成本地验证后触发
- 应在新会话中运行，尽量减少作者上下文污染
- reviewer 应直接通过 `gh pr review` 或 PR comment 将结构化结论提交到当前 PR
- Author agent 负责读取 findings 并修复

## 升级条件

命中以下任一条件时，建议升级为人工 review 或人工决策：

- 权限、认证、敏感数据、外部系统关键链路改动
- reviewer 发现问题但证据不足以判断正确方案
- CI / reviewer 出现难以解释的不稳定行为
- 需求含义仍不明确，无法仅靠代码判断对错

## 重要约束

- 本 skill 默认是 review-first，不默认实现修复
- reviewer 不能因为作者写了"测试已通过"就跳过独立判断
- reviewer 不能把 CI 通过等同于可以合并
- reviewer 的价值在于发现问题，而不是补充总结作者已经说过的话

## References

本 skill 附带以下审查清单，reviewer 可按需参考：

- 通用：`references/general/` — SOLID、代码质量、安全与可靠性
- Python/FastAPI：`references/python-fastapi/` — 类型注解、Pydantic、异步、FastAPI 最佳实践

如果项目使用其他技术栈，通用清单仍然适用，技术栈专用清单可忽略。
