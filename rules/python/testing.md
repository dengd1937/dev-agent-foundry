---
paths:
  - "**/*.py"
  - "**/*.pyi"
---

# Python Testing

> 本文件在 [common/testing.md](../common/testing.md) 的基础上补充 Python 特有内容。

## Framework

- 优先使用 `pytest`

## Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

## Test Organization

使用 `pytest.mark` 做测试分类：

```python
import pytest

@pytest.mark.unit
def test_calculate_total():
    ...

@pytest.mark.integration
def test_database_connection():
    ...
```

## 参考

参见 skill：`python-testing`，获取更详细的 pytest 模式和 fixtures 指南。
