# 通用规范

## 代码质量

- **不可变性（CRITICAL）**：永远创建新对象，禁止原地修改 → python-patterns skill / typescript-patterns skill
- **文件组织**：多小文件 > 少大文件；高内聚低耦合；典型 200-400 行，最大 800 行
- **错误处理**：每一层显式处理；永不静默吞掉 → python-patterns skill / typescript-patterns skill
- **输入验证**：系统边界验证，schema 验证，快速失败 → python-patterns skill / typescript-patterns skill
- **外科手术式修改**：每行改动对应任务；发现无关死代码告知用户而非擅自删除
→ code-quality-gate skill

## 架构模式

- **骨架项目**：搜索成熟模板 → 并行 agent 评估 → 克隆最优方案迭代
- **Repository 模式**：数据访问封装在标准接口后，业务逻辑依赖抽象 → typescript-patterns skill
- **API 响应格式**：统一信封（成功标志、数据载荷、错误字段、分页元数据）→ typescript-patterns skill

## 安全

密钥由 hooks 物理拦截。以下情况触发 security-reviewer agent：
- 认证/授权代码、用户输入处理、数据库查询、文件系统操作
- 外部 API 调用、加密操作、支付/金融代码

发现安全问题：立即停下 → security-reviewer agent → 修复 CRITICAL → 轮换密钥 → 排查同类
→ security-reviewer skill

## 测试

最低覆盖率 **80%**（单元 + 集成 + E2E）。强制 RED → GREEN → IMPROVE。
→ tdd-workflow skill
