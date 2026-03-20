# Python Security

> This file extends [../common/security.md](../common/security.md) with Python-specific content.

本文件定义 Python 项目里与配置、日志和输入模型相关的安全建议。

## 配置与 Secret

- 业务模块不应直接调用 `os.environ.get()` 读取 secret
- 应在统一配置模块中处理环境变量读取、默认值、类型转换和优先级
- `.env.example`、示例配置和测试样例中不得包含真实凭据

## 日志

- 优先使用项目约定的 logging 机制，而不是 `print`
- 记录异常时优先保留堆栈信息，例如 `logger.exception(...)` 或等价方案
- 不要在日志中输出完整 token、认证头、密码或外部系统完整凭据

## 输入校验

- 对请求体、事件载荷、Webhook 输入和第三方 API 响应，优先使用 schema / model 校验
- 对额外字段、向后兼容字段和协议演进策略应有显式决定，而不是隐式接受
- 对跨边界数据优先先校验、再转换、再向核心逻辑传递
