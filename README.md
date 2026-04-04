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
│   │   ├── agents.md
│   │   ├── code-review.md
│   │   ├── coding-style.md
│   │   ├── development-workflow.md
│   │   ├── git-workflow.md
│   │   ├── patterns.md
│   │   ├── security.md
│   │   └── testing.md
│   └── skills/
│       ├── code-quality-gate/
│       ├── commit-quality/
│       ├── design-review/
│       ├── design-review-codex/
│       ├── git-workflow/
│       ├── tdd-workflow/
│       ├── django-security/
│       ├── python-patterns/
│       └── python-testing/
├── .claude/
│   ├── agents/
│   │   ├── planner.md
│   │   ├── tdd-guide.md
│   │   ├── code-reviewer.md
│   │   ├── security-reviewer.md
│   │   ├── refactor-cleaner.md
│   │   ├── doc-updater.md
│   │   ├── docs-lookup.md
│   │   └── python-reviewer.md
│   ├── rules -> ../.agents/rules
│   └── skills -> ../.agents/skills
└── .trae/
    └── skills -> ../.agents/skills
```

## 当前 Skills

| Skill | 用途 |
|---|---|
| [git-workflow](.agents/skills/git-workflow/SKILL.md) | commit / push / PR / CI / merge 全流程闭环 |
| [tdd-workflow](.agents/skills/tdd-workflow/SKILL.md) | 测试优先实现，执行 `RED -> GREEN -> REFACTOR` |
| [code-quality-gate](.agents/skills/code-quality-gate/SKILL.md) | 编辑文件后的质量检查门禁（格式、类型检查、调试代码检测） |
| [commit-quality](.agents/skills/commit-quality/SKILL.md) | 提交前质量检查（commit 格式、lint、secrets 扫描） |
| [python-patterns](.agents/skills/python-patterns/SKILL.md) | Pythonic idioms、类型注解、异常处理、包组织 |
| [python-testing](.agents/skills/python-testing/SKILL.md) | pytest、TDD、fixtures、mock、覆盖率与测试分层 |
| [django-security](.agents/skills/django-security/SKILL.md) | Django 认证鉴权、CSRF/XSS/SQL 注入、生产安全配置 |
| [investigate](.agents/skills/investigate/SKILL.md) | Bug 根因调查门禁 — 假设优先调试，禁止无调查改代码 |
| [retro](.agents/skills/retro/SKILL.md) | 任务复盘 — 审视流程遵守、决策路径与 AI 行为，提出改进建议 |
| [design-review](.agents/skills/design-review/SKILL.md) | 方案对抗性审查 — 在批准前压力测试架构、可行性、测试、性能与范围 |
| [design-review-codex](.agents/skills/design-review-codex/SKILL.md) | 通过 Codex 获取独立跨模型方案审查（Claude Code 专用） |

## 当前 Claude Code Agents

| Agent | 用途 | 触发时机 |
|---|---|---|
| `planner` | 实施规划 | 新功能、多文件改动、复杂重构 |
| `tdd-guide` | 测试优先实现 | 新功能、bug 修复、行为调整 |
| `code-reviewer` | 代码质量与可维护性审查 | 编写或修改代码后 |
| `security-reviewer` | 安全漏洞检测 | 提交前、敏感代码 |
| `refactor-cleaner` | 死代码清理 | 代码维护 |
| `doc-updater` | 文档与 codemap 更新 | 文档同步 |
| `docs-lookup` | 通过 Context7 查阅文档 | API / 文档查询 |
| `python-reviewer` | Python 代码审查 | Python 项目 |

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
- rules 和 skills 职责分离，避免相互混杂
- 新项目应能在最少改动下直接复用已有资产

## License

MIT
