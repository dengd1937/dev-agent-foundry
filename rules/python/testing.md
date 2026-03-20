# Python Testing

> This file extends [../common/testing.md](../common/testing.md) with Python-specific content.

本文件定义 Python 项目的测试工具和组织建议。

## 默认工具

- 优先使用 `pytest`
- 异步代码优先使用 `pytest-asyncio` 或项目约定的异步测试方案
- 格式化和 lint 仍应作为提交前验证的一部分，与测试一起执行

## 常见验证命令

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

如项目规模较大，优先运行与本次改动直接相关的测试子集，再决定是否补全量测试。

## Python 测试组织建议

- 纯逻辑函数、解析器、字段映射、边界处理优先写单元测试
- FastAPI / Django / Flask 等 Web 层优先补路由到服务的集成测试
- 外部客户端应尽量通过 mock、stub 或 fake service 固定响应契约
- 对上游 API schema、关键 JSON 结构和模型映射，优先补契约型测试

## 异步与外部依赖

- 异步测试应显式标记或使用统一 fixture，不要混用多套运行方式
- 外部真实服务若只在特定环境可达，应通过环境变量、skip 标记或 smoke 测试隔离
- 不要让“公司内网依赖不可达”直接阻塞普通本地开发

## Fixtures 与样例数据

- 能复用现有 fixture、snapshot、样例 JSON 时优先复用
- fixture 数据的变更应是显式更新，而不是被测试被动跟随
- 当项目依赖快照数据时，应明确说明快照的维护方式和更新意图
