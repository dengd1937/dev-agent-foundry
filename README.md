# meridian

面向现代开发工作流的跨工具 AI Coding agent 基准线。

`meridian` 的目标是沉淀一套可跨项目、跨工具复用的 agent 资产，让 Claude Code、Trae 等工具围绕同一批共享 rules 与 skills 协作。

## 当前设计

仓库围绕三层内容组织：

1. **`AGENTS.md`** — 仓库总入口、agent 导航、优先级说明
2. **`.agents/`** — 共享 rules 和 skills 真源，保持开箱即用
3. **`.claude/`、`.trae/`** — 工具适配层，通过软链接接入共享资产，尽量保持轻量

## 目录结构

```text
meridian/
├── AGENTS.md
├── .agents/
│   ├── rules/
│   │   ├── agents.md              # Agent 编排与分工
│   │   ├── common.md              # 代码质量、安全、测试通用规范
│   │   ├── code-review.md         # 代码审查流程与严重等级
│   │   ├── communication.md       # 交互原则（暴露不确定性）
│   │   ├── development-workflow.md # 开发工作流（动态路由）
│   │   ├── design-workflow.md     # 设计工作流路由
│   │   ├── git-workflow.md        # Git 规范
│   │   └── languages.md           # Python / TypeScript 语言规范
│   └── skills/
│       ├── code-quality-gate/     # 编辑后质量门禁
│       ├── commit-quality/        # 提交前质量检查
│       ├── design-review/         # 方案对抗性审查
│       ├── design-review-codex/   # Codex 跨模型审查
│       ├── design-workflow/       # UI 设计工作流 V2（含 L1 轻量引用）
│       ├── django-security/       # Django 安全最佳实践
│       ├── e2e-testing/           # Playwright E2E 测试
│       ├── git-workflow/          # Git 全流程闭环
│       ├── ideate/                # 产品想法细化（PM skill）
│       ├── investigate/           # 根因分析门禁
│       ├── pencil-design/         # Pencil MCP 设计+代码生成（含 6 份参考）
│       ├── python-patterns/       # Pythonic 模式
│       ├── python-testing/        # pytest 测试策略
│       ├── retro/                 # 任务复盘
│       ├── security-reviewer/     # 安全审查清单
│       ├── tdd-workflow/          # 测试驱动开发
│       ├── typescript-patterns/   # TypeScript/React 模式
│       ├── typescript-testing/    # Vitest + RTL 测试策略
│       └── using-git-worktrees/   # Git worktree 并行开发
├── .claude/
│   ├── agents/
│   │   ├── planner.md
│   │   ├── tdd-guide.md
│   │   ├── code-reviewer.md
│   │   ├── security-reviewer.md
│   │   ├── design-reviewer.md
│   │   ├── refactor-cleaner.md
│   │   ├── doc-writer.md          # 工作流文档写入（模板格式化）
│   │   ├── doc-updater.md         # 跨领域文档维护（catalog/codemap）
│   │   ├── docs-lookup.md
│   │   ├── python-reviewer.md
│   │   ├── typescript-reviewer.md
│   │   └── e2e-runner.md
│   ├── hooks/
│   │   ├── pre-bash-guard.sh      # 拦截危险 shell 命令
│   │   ├── pre-write-secrets.sh   # 拦截密钥写入
│   │   ├── post-write-debug.sh    # 检测调试代码
│   │   └── pre-commit-review-check.py  # 提交前代码审查提醒
│   ├── rules -> ../.agents/rules
│   └── skills -> ../.agents/skills
└── .trae/
    └── skills -> ../.agents/skills
```

## 当前 Skills

| Skill | 用途 |
|---|---|
| [ideate](.agents/skills/ideate/SKILL.md) | 产品想法细化 — Product Discovery、竞品调研、功能分析、文档输出 |
| [design-workflow](.agents/skills/design-workflow/SKILL.md) | UI 设计工作流 V2 — L1 轻量 / L2 标准（wireframe → 高保真 → 审查 → 交付） |
| [pencil-design](.agents/skills/pencil-design/SKILL.md) | Pencil MCP 设计与代码生成 — token 管理、组件映射、视觉验证 |
| [design-review](.agents/skills/design-review/SKILL.md) | 方案对抗性审查 — 压力测试架构、可行性、测试、性能与范围 |
| [design-review-codex](.agents/skills/design-review-codex/SKILL.md) | 通过 Codex 获取独立跨模型方案审查（Claude Code 专用） |
| [tdd-workflow](.agents/skills/tdd-workflow/SKILL.md) | 测试驱动开发，执行 RED → GREEN → IMPROVE |
| [code-quality-gate](.agents/skills/code-quality-gate/SKILL.md) | 编辑文件后的质量门禁（格式、类型检查、调试代码检测） |
| [commit-quality](.agents/skills/commit-quality/SKILL.md) | 提交前质量检查（commit 格式、lint、secrets 扫描） |
| [git-workflow](.agents/skills/git-workflow/SKILL.md) | commit / push / PR / CI / merge 全流程闭环 |
| [python-patterns](.agents/skills/python-patterns/SKILL.md) | Pythonic 模式、类型注解、异常处理、包组织 |
| [python-testing](.agents/skills/python-testing/SKILL.md) | pytest、TDD、fixtures、mock、覆盖率与测试分层 |
| [typescript-patterns](.agents/skills/typescript-patterns/SKILL.md) | TypeScript/React 模式、shadcn/ui、Tailwind v4 |
| [typescript-testing](.agents/skills/typescript-testing/SKILL.md) | Vitest + React Testing Library + Playwright E2E |
| [django-security](.agents/skills/django-security/SKILL.md) | Django 认证鉴权、CSRF/XSS/SQL 注入、生产安全配置 |
| [security-reviewer](.agents/skills/security-reviewer/SKILL.md) | 敏感功能开发与提交前的安全审查清单、漏洞模式与防护建议 |
| [e2e-testing](.agents/skills/e2e-testing/SKILL.md) | Playwright E2E 测试模式、POM、CI 集成、flaky 测试治理 |
| [investigate](.agents/skills/investigate/SKILL.md) | 根因分析门禁 — 假设优先调试，禁止无调查改代码 |
| [retro](.agents/skills/retro/SKILL.md) | 任务复盘 — 审视流程遵守、决策路径与 AI 行为，提出改进建议 |
| [using-git-worktrees](.agents/skills/using-git-worktrees/SKILL.md) | Git worktree 并行开发，减少 stash 和上下文切换 |

## 当前 Claude Code Agents

| Agent | 用途 | 触发时机 |
|---|---|---|
| `planner` | 实施方案规划 | 新功能、多文件改动、复杂重构 |
| `tdd-guide` | 测试驱动开发 | 新功能、bug 修复、行为调整 |
| `code-reviewer` | 代码质量与可维护性审查 | 编写或修改代码后 |
| `security-reviewer` | 安全漏洞检测 | 提交前、敏感代码 |
| `design-reviewer` | 设计产物审查 | 设计工作流 V2-4 |
| `refactor-cleaner` | 死代码清理 | 代码维护 |
| `doc-writer` | 工作流文档写入（模板格式化+写文件） | 工作流产出文档后 |
| `doc-updater` | 跨领域文档维护（catalog、索引、codemap） | 工作流完成后 |
| `docs-lookup` | 通过 Context7 查阅文档 | API / 文档查询 |
| `python-reviewer` | Python 代码审查 | Python 项目 |
| `typescript-reviewer` | TypeScript / React / Next.js 代码审查 | TypeScript / Next.js 项目 |
| `e2e-runner` | 浏览器端 E2E 测试执行 | 关键用户路径变更 |

## 三层文档架构

工作流产出文档经过两层 agent 处理，形成闭环：

```
工作流（ideate / design / development）
  │  产出结构化数据（对话中确认）
  ▼
doc-writer agent（独立上下文）
  │  按模板格式化 → 写入文件
  ▼
文件落盘（docs/product/、docs/designs/、docs/modules/）
  │
  ▼
doc-updater agent（独立上下文）
  │  更新 catalog / 索引 / codemap
  ▼
共享知识层同步
```

- **工作流**：只产出结构化数据，不写文件、不含模板
- **doc-writer**：集中管理 7 个文档模板，接收数据后格式化写入
- **doc-updater**：维护 feature catalog、component catalog、module index、codemap，评估 README 同步需求

## 使用方式

### 方式一：直接复制共享资产

```bash
# 复制单个 skill
cp -r .agents/skills/git-workflow /your-project/.agents/skills/

# 复制全部 skills
cp -r .agents/skills/* /your-project/.agents/skills/

# 复制全部 rules
cp -r .agents/rules/* /your-project/.agents/rules/
```

### 方式二：Git submodule

```bash
cd /your-project
git submodule add https://github.com/dengd1937/meridian.git .agents/meridian
```

### 方式三：手动同步

定期从本仓库拉取更新，再合并到项目自己的 agent 目录中。适合希望保留深度定制能力的团队。

## 设计原则

- 共享 rules 和 skills 只有一份真源，统一放在 `.agents/`
- 工具适配层通过软链接接入，不复制资产内容
- agent 适配优先做薄 wrapper；无法确认官方仓库格式时，先落蓝图文档，不发明伪标准
- rules 保持"薄"——只放硬性约束和触发入口，详细指导推到 skills 按需加载
- 文档模板集中管理（doc-writer agent），工作流不含内联模板
- Hooks 提供确定性安全执行层（物理拦截），rules 提供软性行为引导

## License

MIT
