# 在 Claude Code 项目中使用 dev-agent-skills

## 快速接入

### 1. 复制 skill 到项目

```bash
# 复制全部 skill
cp -r /path/to/dev-agent-skills/skills/* /your-project/.agents/skills/

# 或只复制需要的 skill
cp -r /path/to/dev-agent-skills/skills/git-workflow /your-project/.agents/skills/
cp -r /path/to/dev-agent-skills/skills/code-review-expert /your-project/.agents/skills/
```

### 2. 在 CLAUDE.md 中注册 skill

在项目的 `CLAUDE.md` 中添加 skill 引用：

```markdown
## Skills

根据任务类型选择：

- `git-workflow`：交付类工作流
- `code-review-expert`：独立 reviewer 协议
- `self-review`：可选的本地自审
- `design-review`：设计方案审查
- `doc-gardening`：文档园艺
```

### 3. 使用

在 Claude Code 中直接通过 skill 名称触发：

- 输入"提交代码"或"push" → 自动触发 `git-workflow`
- 输入"/design-review" → 触发设计方案审查
- 输入"帮我做本地自审" → 触发 `self-review`

## 项目适配建议

### Git 流程文档

如果项目有自己的 Git 规范文档，`git-workflow` 会自动查找并参照。建议将 Git 规范放在以下常见路径之一：

- `docs/devops/git_workflow.md`
- `docs/git-workflow.md`
- `CONTRIBUTING.md`

### 技术栈 References

`code-review-expert` 附带了 Python/FastAPI 专用清单。如果项目使用其他技术栈：

- 通用清单（`references/general/`）始终适用
- 可为项目技术栈添加专用清单到 `references/` 下
- 后续本仓库会逐步补充更多语言的清单

### Agent 指令文件

Skill 中提到的"项目级 Agent 指令文件"指的是：

- Claude Code：`CLAUDE.md`
- 通用：`AGENTS.md`
- 其他工具：按工具约定的指令文件
