---
paths:
  - "**/*.py"
  - "**/*.pyi"
---

# Python Coding Style

> 本文件在 [common/coding-style.md](../common/coding-style.md) 的基础上补充 Python 特有内容。

## 标准

- 遵循 **PEP 8** 规范
- 在所有函数签名上使用 **类型注解**

## 不可变性

优先使用不可变数据结构：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

## 格式化

- 使用 **black** 做代码格式化
- 使用 **isort** 做 import 排序
- 使用 **ruff** 做 lint 检查

## 提交前门禁

- 修改 Python 文件后，提交前必须完成格式化、lint 和类型检查
- 本地可提前执行这些检查，以减少在 PR 阶段返工
- CI 应重复执行同一组核心检查，并作为最终门禁

最小检查集合：

```bash
black .
isort .
ruff check .
mypy .
```

## 参考

参见 skill：`python-patterns`，获取更全面的 Python 习惯用法和模式。
