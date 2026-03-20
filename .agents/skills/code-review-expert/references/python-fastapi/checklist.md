# Python/FastAPI Best Practices Checklist

## Type Hints

### Anti-patterns

- **Missing type hints on public functions**: All public functions should have type annotations
- **Using `Any` unnecessarily**: Prefer specific types
- **Legacy typing syntax**: Use modern Python 3.10+ syntax (`list[X]` instead of `List[X]`, `X | None` instead of `Optional[X]`)

### Best Practices

- [ ] All public functions have type hints (parameters + return type)
- [ ] Class attributes are annotated at class level
- [ ] Use `| None` instead of `Optional` (Python 3.10+)
- [ ] Use `list[X]` instead of `List[X]`
- [ ] Avoid `Any` unless truly necessary

---

## Pydantic Models

### Model Configuration

- **Missing `extra` configuration**: New models should declare extra handling
- **Missing validators for business rules**: Use `@field_validator` for constraints
- **Mutable default values**: Use `default_factory` for mutable defaults

---

## Async/Await

### Common Anti-patterns

- **Blocking in async context**: Using `time.sleep()`, `requests.get()`, sync I/O in async functions
- **Missing await**: Forgetting to await coroutine
- **`asyncio.gather` error handling**: First exception raised, others silently cancelled

### Best Practices

- [ ] Use `asyncio.sleep()` instead of `time.sleep()` in async functions
- [ ] Use async HTTP clients (httpx, aiohttp) instead of requests
- [ ] Use async DB drivers (asyncpg, databases)
- [ ] Properly await all coroutines
- [ ] Use `TaskGroup` over `gather` for structured concurrency (Python 3.11+)
- [ ] Never mutate shared state in `run_in_executor` callbacks
- [ ] Ensure context (request_id, tracing) propagates to background tasks

---

## FastAPI Specifics

### Dependency Injection

- **Hard-coded dependencies**: Should use `Depends` for testability

### Request/Response Models

- **Missing response models**: Should declare response schema with `response_model`

### Error Handling

- **Using HTTPException correctly**: Return appropriate status codes with descriptive detail

---

## Imports & Dependencies

### Import Organization

- **Circular imports**: Avoid circular dependencies between modules
- **Import order**: Standard library -> Third-party -> Local
- **Unused imports**: Clean up unused imports
- **Shadowing builtins**: Don't shadow `list`, `dict`, `id`, `type`, etc.

---

## Logging

### Best Practices

- **Use module-level logger**: `logger = logging.getLogger(__name__)`
- **Never use print** in production code
- **Include context** in log messages (request_id, user_id, etc.)
- **Don't log sensitive data**: passwords, tokens, PII

---

## Testing

### Common Issues

- **Missing tests for new code paths**: Every new branch/function should have corresponding tests
- **Tests that depend on external services** (should mock)
- **No async test marker**: Missing `@pytest.mark.asyncio`
- **Empty assertions**: Tests that always pass
- **Testing implementation, not behavior**: Tests coupled to internal details
- **Flaky tests**: Timing dependencies, random data, order-dependent state

### Coverage Expectations for Changed Code

- [ ] New public functions have at least one test
- [ ] New error handling paths have tests
- [ ] New validators/business rules have tests with boundary values
- [ ] Modified functions have tests updated to reflect new behavior

---

## Configuration Management

### Config Access Patterns

- **Direct env access in business code**: Using `os.environ` or `os.getenv()` outside config module
- **Hardcoded config values**: Magic strings/numbers that should be configurable
- **Missing config validation**: New config fields without type/range validation
- **Sensitive config in non-secret stores**: API keys in config files instead of env/secrets
