# Rules

`rules/` 用于沉淀跨项目复用的默认规则。

这里参考 `everything-claude-code` 的思路，将“规则”与“skill”分开：

- `rules/` 回答应该遵守什么
- `.agents/skills/` 回答遇到任务时怎么做

## 当前结构

- `common/`：尽量适用于大多数项目的通用规则
- `python/`：Python 项目的扩展规则
- 当前暂不单独维护 `hooks/`，工具执行后的自动化动作放在工具适配层中处理
- 后续可继续增加更多语言、框架或技术栈专属规则目录

## 当前主题

- [common/development-workflow.md](common/development-workflow.md)
- [common/coding-style.md](common/coding-style.md)
- [common/patterns.md](common/patterns.md)
- [common/performance.md](common/performance.md)
- [common/security.md](common/security.md)
- [common/testing.md](common/testing.md)
- [common/git-workflow.md](common/git-workflow.md)
- [common/ci-workflow.md](common/ci-workflow.md)

## 使用原则

- 这些规则默认作为项目级基线
- 如果目标项目已有更具体、更新更近的规则，应优先服从项目规则
- 若某条规则明显依赖特定技术栈或组织流程，应拆到更具体的规则层，而不是留在 `common/`
- 当语言层规则与 `common/` 冲突时，语言层规则优先

## 分层原则

- `common/` 只保留语言无关的默认原则，不放强绑定语言工具链的细节
- 语言目录维护各自独立的技术栈规则；若某个主题同时存在 `common/` 与语言层版本，默认先读 `common/`，再读语言层补充
- 项目接入时，应先加载 `common/`，再加载与技术栈匹配的语言目录
- 若语言层与 `common/` 冲突，语言层优先
- 若某条规则需要自动路由到特定文件类型，优先在语言层使用 front matter 等轻量元数据表达

## 当前语言层入口

- [python/coding-style.md](python/coding-style.md)
- [python/testing.md](python/testing.md)
- [python/security.md](python/security.md)
- [python/patterns.md](python/patterns.md)

## 接入方式

### 安装原则

- 当前 `common/` 先保留开发流程、编码风格、模式设计、性能、安全、测试、Git / PR 交付、CI 检查八份主文档
- 语言层目录按项目技术栈叠加安装
- 保留目录层级，不要把不同目录下的同名文件拍平成一个目录

### 在本仓库中的使用方式

- 共享 skill 真源在 `.agents/skills/`
- `.claude/`、`.cursor/`、`.trae/` 只负责工具接入，不应成为规则或 skill 的真源
- 项目级接入时，应先从 `AGENTS.md` 建立导航，再按任务类型加载 `rules/` 和相关 skill
- 涉及开发主流程时，优先从 `common/development-workflow.md` 进入
- 涉及通用编码风格、命名、错误处理、边界校验时，参考 `common/coding-style.md`
- 涉及通用设计模式、边界分层、接口抽象时，参考 `common/patterns.md`
- 涉及性能热点、上下文控制、渐进式优化时，参考 `common/performance.md`
- 涉及 secret、输入安全、鉴权边界和敏感信息处理时，参考 `common/security.md`
- 涉及覆盖率、测试分层、TDD 和失败排查时，参考 `common/testing.md`
- 涉及提交、推送、PR、CI、合并等交付动作时，再进入 `common/git-workflow.md`
- 涉及 CI 检查项、失败分类和等待策略时，再进入 `common/ci-workflow.md`

## Rules vs Skills

- `rules/` 定义标准、约束、完成态和检查项
- `.agents/skills/` 提供具体任务的执行协议和操作路径
- 更合适放进 skill 的内容，不应堆回 `rules/`
