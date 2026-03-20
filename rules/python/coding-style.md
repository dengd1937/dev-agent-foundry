# Python Coding Style

> This file extends [../common/coding-style.md](../common/coding-style.md) with Python-specific content.

本文件定义 Python 项目的编码、类型和模型约束。

## 工具链

- 优先使用 `uv` 作为依赖与执行入口
- 优先使用 `ruff` 作为格式化与 lint 工具
- 若项目已固定行宽，优先遵循项目配置；若未明确，推荐 120 字符以内

常见命令：

```bash
uv run ruff format .
uv run ruff check .
uv run pytest
```

## 命名

- 变量、函数、模块使用 `snake_case`
- 类使用 `PascalCase`
- 常量使用 `UPPER_CASE`
- 私有函数、私有模块使用前导下划线

## 类型注解

- 所有公共函数、公共方法和跨模块边界函数应补齐类型注解
- 优先使用现代 typing 语法，如 `list[str]`、`dict[str, int]`
- 除非处于外部动态边界，否则避免使用 `Any`
- 对外部 SDK、动态 JSON 或弱类型输入，尽量在边界层完成类型收敛，再向内传播

## 数据模型与校验

- 优先在边界层使用结构化模型而不是散乱字典
- 若项目使用 Pydantic，优先使用当前项目约定的主版本，并保持同一仓库内风格一致
- 新增输入模型时，应明确 extra 字段策略，而不是默认忽略协议变化
- 领域规则应尽量通过模型校验器、显式验证函数或统一入口收敛

## Python 代码组织

- 配置访问应通过统一 settings 层，不要在业务模块中散落 `os.environ`
- 外部输入校验、模型转换和协议兼容逻辑应尽量放在边界层
- 错误处理应保留原始异常上下文，避免随意吞错或改成无法定位的问题描述
