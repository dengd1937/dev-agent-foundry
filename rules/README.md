# Rules

`rules/` 用于沉淀跨项目复用的默认规则。

这里参考 `everything-claude-code` 的思路，将“规则”与“skill”分开：

- `rules/` 回答应该遵守什么
- `.agents/skills/` 回答遇到任务时怎么做

## 当前结构

- `common/`：尽量适用于大多数项目的通用规则
- `python/`：Python 项目的扩展规则
- 后续可继续增加更多语言、框架或技术栈专属规则目录

## 当前主题

- [common/coding-style.md](common/coding-style.md)
- [common/documentation.md](common/documentation.md)
- [common/configuration.md](common/configuration.md)
- [common/git-workflow.md](common/git-workflow.md)
- [common/testing.md](common/testing.md)
- [common/code-review.md](common/code-review.md)
- [common/security.md](common/security.md)
- [common/agents.md](common/agents.md)

## 使用原则

- 这些规则默认作为项目级基线
- 如果目标项目已有更具体、更新更近的规则，应优先服从项目规则
- 若某条规则明显依赖特定技术栈或组织流程，应拆到更具体的规则层，而不是留在 `common/`
- 当语言层规则与 `common/` 冲突时，语言层规则优先

## 分层原则

- `common/` 只保留语言无关的默认原则，不放强绑定语言工具链的细节
- 语言目录在对应主题文件中扩展 `common/`，例如 `python/coding-style.md` 扩展 `common/coding-style.md`
- 项目接入时，应先加载 `common/`，再加载与技术栈匹配的语言目录

## 当前语言层入口

- [python/coding-style.md](python/coding-style.md)
- [python/testing.md](python/testing.md)
- [python/security.md](python/security.md)
- [python/patterns.md](python/patterns.md)
