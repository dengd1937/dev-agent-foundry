# CI Workflow

> 本文档定义默认的 CI 门禁与处理规则。

## 核心原则

- CI 是交付门禁，不是可选补充
- 能在本地前置的检查，应尽量在创建 PR 前完成
- 关键检查仍应在 CI 中重复执行，保证结果口径一致

## 核心检查分类

建议优先保留以下 4 类检查：

### 1. 代码质量检查

常见命令：

```bash
uv run ruff format --check .
uv run ruff check .
```

### 2. 文档入口检查

常见命令：

```bash
uv run pytest tests/test_docs_links.py
```

### 3. 自动化测试

常见命令：

```bash
uv run pytest --ignore=tests/test_docs_links.py
```

### 4. 运行环境准备

常见动作：

- 安装依赖，例如 `uv sync`
- 启动测试依赖容器或服务
- 等待 readiness 检查通过
- 测试失败时输出依赖服务日志

## 失败处理

### 代码质量检查失败

优先动作：

```bash
uv run ruff format .
uv run ruff check --fix .
```

### 文档入口检查失败

优先动作：

```bash
uv run pytest tests/test_docs_links.py
```

修复失效入口后再重跑检查。

### 自动化测试失败

- 先定位具体失败用例
- 判断失败来自代码、测试数据还是环境依赖
- 先重跑相关测试，必要时再补跑主测试集

### 运行环境准备失败

- 保留失败日志
- 区分代码问题和环境问题
- 视仓库约定决定重试、重新触发还是升级人工判断

## 完成态

- required checks 仍处于 `queued`、`pending` 或 `in_progress` 时，不算完成
- `push` 成功不等于 CI 成功
- `PR 已创建` 不等于 CI 稳定
- required checks 全部通过，或失败原因与下一步动作已明确同步后，当前 CI 阶段才算稳定

## 边界

- 开发主流程见 [development-workflow.md](./development-workflow.md)
- 提交、推送、PR、review、合并阶段见 [git-workflow.md](./git-workflow.md)
