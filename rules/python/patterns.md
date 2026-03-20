---
paths:
  - "**/*.py"
  - "**/*.pyi"
---

# Python Patterns

> 本文件在 [common/patterns.md](../common/patterns.md) 的基础上补充 Python 特有内容。

## Protocol（Duck Typing）

```python
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: str) -> dict | None: ...
    def save(self, entity: dict) -> dict: ...
```

## 使用 Dataclass 作为 DTO

```python
from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int | None = None
```

## Context Managers 与 Generators

- 使用 context manager（`with` 语句）做资源管理
- 使用 generator 做惰性求值和内存高效的迭代

## 参考

参见 skill：`python-patterns`，获取关于装饰器、并发和包组织的更详细模式。
