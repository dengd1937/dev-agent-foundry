# 代码审查规范

## 何时审查

**强制触发**（commit 前 / merge 前）：
- 向共享分支提交任何 commit 前
- 安全敏感代码变更时（auth、支付、用户数据）
- 合并 pull request 前

**建议触发**：写完或修改代码后、架构变更时

**审查前提**：CI/CD 通过、merge 冲突已解决、分支已同步

## 严重等级

| 等级 | 含义 | 处理方式 |
|------|------|---------|
| CRITICAL | 安全漏洞或数据丢失风险 | **阻塞** — merge 前必须修复 |
| HIGH | Bug 或重大质量问题 | **警告** — 建议 merge 前修复 |
| MEDIUM | 可维护性问题 | **提示** — 考虑修复 |
| LOW | 风格或次要建议 | **备注** — 可选 |

## Agent 使用

| Agent | 用途 |
|-------|------|
| **code-reviewer** | 通用代码质量、模式、最佳实践 |
| **security-reviewer** | 安全漏洞、OWASP Top 10 |
| **python-reviewer** | Python 专项问题 |
| **typescript-reviewer** | TypeScript/React 类型安全、异步模式、hooks |

## 审批标准

- **通过**：无 CRITICAL 或 HIGH 问题
- **警告**：仅有 HIGH 问题（谨慎合并）
- **阻塞**：发现 CRITICAL 问题

→ code-quality-gate skill / security-reviewer agent
