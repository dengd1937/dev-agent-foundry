# dev-agent-skills

面向 AI Agent 辅助编码的通用 Skill 集合。

适用于 Claude Code、Cursor、Codex、Trae 等支持 skill/prompt 协议的 AI 编码工具。

## Skill 列表

| Skill | 用途 | 说明 |
|---|---|---|
| [git-workflow](skills/git-workflow/SKILL.md) | 交付工作流 | commit / push / PR / CI / merge 全流程闭环 |
| [code-review-expert](skills/code-review-expert/SKILL.md) | 独立代码审查 | findings 驱动的结构化 review 协议 |
| [self-review](skills/self-review/SKILL.md) | 本地自审 | 提交前的作者视角质量验证 |
| [design-review](skills/design-review/SKILL.md) | 设计方案审查 | 完整性/可行性/安全性/可维护性四维度 |
| [doc-gardening](skills/doc-gardening/SKILL.md) | 文档园艺 | 检测并修复文档与代码之间的漂移 |

## 使用方式

### 方式一：直接复制（推荐起步）

将需要的 skill 目录复制到项目中：

```bash
# 复制单个 skill
cp -r skills/git-workflow /your-project/.agents/skills/

# 复制全部 skill
cp -r skills/* /your-project/.agents/skills/
```

复制后可根据项目需求自行调整。

### 方式二：Git submodule

```bash
cd /your-project
git submodule add https://github.com/dengd1937/dev-agent-skills.git .agents/dev-agent-skills
```

### 方式三：手动同步

定期从本仓库拉取更新，合并到项目中。适合需要深度定制的场景。

## 项目适配

Skill 设计为项目无关，但部分 skill 会引用项目级文件（如 Agent 指令文件、Git 流程文档）。

适配时只需注意：

1. **Agent 指令文件** — 如果项目有 `CLAUDE.md`、`AGENTS.md` 或类似文件，skill 会自动参照
2. **Git 流程文档** — `git-workflow` 会查找项目中的 Git 规范文档，未找到时按内置默认流程执行
3. **技术栈 references** — `code-review-expert` 的 references 按语言分组，按需引用

## 目录结构

```
dev-agent-skills/
├── skills/
│   ├── git-workflow/          # 交付工作流
│   ├── code-review-expert/    # 独立代码审查
│   │   ├── references/general/        # 通用审查清单
│   │   └── references/python-fastapi/ # Python/FastAPI 专用清单
│   ├── design-review/         # 设计方案审查
│   ├── self-review/           # 本地自审
│   └── doc-gardening/         # 文档园艺
├── references/                # 跨 skill 共享参考材料
└── examples/                  # 接入示例
```

## 贡献

欢迎提交 Issue 和 PR。新增 skill 请遵循现有目录结构和文件命名约定。

## License

MIT
