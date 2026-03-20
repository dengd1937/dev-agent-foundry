# dev-agent-foundry

面向现代开发工作流的跨工具 dev-agent 能力底座。

`dev-agent-foundry` 的目标，是把之前在 `sre-copilot` 中验证过的一些通用经验沉淀出来，整理成可复用的规则层和共享 skill 层，方便新项目直接接入，并尽量减少对单一工具协议的绑定。

当前组织方向更明确偏向 `everything-claude-code` 的规则分层方式，同时保留 `sre-copilot` 那种可以直接复制使用的 skill 目录体验。

适用工具包括但不限于 Claude Code、Codex、Cursor、Trae，以及其他支持项目级指令文件、rules、prompts 或 agent 协议的 AI 编码工具。

## 当前设计

仓库围绕四层内容组织：

1. `AGENTS.md`
   仓库总入口、总导航、优先级说明
2. `.agents/skills/`
   共享 skill 真源，保持开箱即用
3. `rules/`
   通用规则层，优先沉淀编码规范、测试规范、交付流程、review 和 agent 协作约束
4. `.claude/`、`.cursor/`、`.trae/`
   工具适配层，尽量保持轻量

## 目录结构

```text
dev-agent-foundry/
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── git-workflow/
│       ├── code-review-expert/
│       ├── design-review/
│       ├── self-review/
│       └── doc-gardening/
├── rules/
│   ├── README.md
│   ├── common/
│       ├── coding-style.md
│       ├── documentation.md
│       ├── configuration.md
│       ├── git-workflow.md
│       ├── testing.md
│       ├── code-review.md
│       ├── security.md
│       └── agents.md
│   └── python/
│       ├── coding-style.md
│       ├── testing.md
│       ├── security.md
│       └── patterns.md
├── .claude/
│   ├── README.md
│   └── skills -> ../.agents/skills
├── .cursor/
│   ├── README.md
│   └── skills -> ../.agents/skills
└── .trae/
    ├── README.md
    └── skills -> ../.agents/skills
```

## 当前 Skills

| Skill | 用途 | 说明 |
|---|---|---|
| [.agents/skills/git-workflow](.agents/skills/git-workflow/SKILL.md) | 交付工作流 | commit / push / PR / CI / merge 全流程闭环 |
| [.agents/skills/code-review-expert](.agents/skills/code-review-expert/SKILL.md) | 独立代码审查 | findings 驱动的结构化 review 协议 |
| [.agents/skills/self-review](.agents/skills/self-review/SKILL.md) | 本地自审 | 提交前的作者视角质量验证 |
| [.agents/skills/design-review](.agents/skills/design-review/SKILL.md) | 设计方案审查 | 完整性、可行性、安全性、可维护性四维度 |
| [.agents/skills/doc-gardening](.agents/skills/doc-gardening/SKILL.md) | 文档园艺 | 检测并修复文档与代码之间的漂移 |

## 使用方式

### 方式一：直接复制共享 skill

将需要的 skill 目录复制到项目中：

```bash
# 复制单个 skill
cp -r .agents/skills/git-workflow /your-project/.agents/skills/

# 复制全部 skill
cp -r .agents/skills/* /your-project/.agents/skills/
```

### 方式二：Git submodule

```bash
cd /your-project
git submodule add https://github.com/dengd1937/dev-agent-foundry.git .agents/dev-agent-foundry
```

### 方式三：手动同步

定期从本仓库拉取更新，再合并到项目自己的 agent 目录中。适合希望保留深度定制能力的团队。

## 规则层定位

`rules/` 参考 `everything-claude-code` 的做法，用来沉淀默认应遵守的规则，而不是具体任务协议。

当前已落地的第一批通用规则包括：

- [rules/common/coding-style.md](rules/common/coding-style.md)
- [rules/common/documentation.md](rules/common/documentation.md)
- [rules/common/configuration.md](rules/common/configuration.md)
- [rules/common/git-workflow.md](rules/common/git-workflow.md)
- [rules/common/testing.md](rules/common/testing.md)
- [rules/common/code-review.md](rules/common/code-review.md)
- [rules/common/security.md](rules/common/security.md)
- [rules/common/agents.md](rules/common/agents.md)

同时已经补出第一批语言层规则：

- [rules/python/coding-style.md](rules/python/coding-style.md)
- [rules/python/testing.md](rules/python/testing.md)
- [rules/python/security.md](rules/python/security.md)
- [rules/python/patterns.md](rules/python/patterns.md)

## 设计原则

- 共享 skill 只有一份真源，统一放在 `.agents/skills/`
- 工具适配层尽量不复制 skill 内容，优先通过软链接接入
- `rules/` 和 `skills/` 职责分离，避免相互混杂
- 规则采用 `common/ + language-specific/` 分层，语言层覆盖通用默认值
- 新项目应能在最少改动下直接复用已有 skill

## 当前状态

这一轮已经完成仓库骨架重组，并沉淀了第一批从 `sre-copilot` 提炼出来的通用规则。下一步可以继续判断哪些内容适合扩展到语言层规则，哪些仍然应该保留在项目私有文档中。

## License

MIT
