---
paths:
  - "**/*.py"
  - "**/*.pyi"
---

# Python Security

> 本文件在 [common/security.md](../common/security.md) 的基础上补充 Python 特有内容。

## Secret 管理

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]  # 如果缺失会抛出 KeyError
```

## 安全扫描

- 使用 **bandit** 做静态安全分析：

```bash
bandit -r src/
```

## 参考

参见 skill：`django-security`，获取 Django 专属的安全指南（如适用）。
