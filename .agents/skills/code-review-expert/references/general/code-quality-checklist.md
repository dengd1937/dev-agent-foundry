# Code Quality Checklist

## Error Handling

### Anti-patterns to Flag

- **Swallowed exceptions**: Empty except/catch blocks or catch with only logging
- **Overly broad catch**: Catching base Exception/Error instead of specific types
- **Error information leakage**: Stack traces or internal details exposed to users
- **Missing error handling**: No try-catch around fallible operations (I/O, network, parsing)
- **Async error handling**: Unhandled exceptions in async tasks, missing error handling in background tasks

### Best Practices to Check

- [ ] Errors are caught at appropriate boundaries
- [ ] Error messages are user-friendly (no internal details exposed)
- [ ] Errors are logged with sufficient context for debugging
- [ ] Async errors are properly propagated or handled
- [ ] Fallback behavior is defined for recoverable errors
- [ ] Critical errors trigger alerts/monitoring

### Questions to Ask
- "What happens when this operation fails?"
- "Will the caller know something went wrong?"
- "Is there enough context to debug this error?"

---

## Performance & Caching

### CPU-Intensive Operations

- **Expensive operations in hot paths**: Regex compilation, JSON parsing, crypto in loops
- **Blocking operations in async context**: Sync I/O in async functions
- **Unnecessary recomputation**: Same calculation done multiple times
- **Missing memoization**: Pure functions called repeatedly with same inputs

### Database & I/O

- **N+1 queries**: Loop that makes a query per item instead of batch
- **Missing indexes**: Queries on unindexed columns
- **Over-fetching**: Selecting all columns when only few needed
- **No pagination**: Loading entire dataset into memory

### Caching Issues

- **Missing cache for expensive operations**: Repeated API calls, DB queries, computations
- **Cache without TTL**: Stale data served indefinitely
- **Cache without invalidation strategy**: Data updated but cache not cleared
- **Cache key collisions**: Insufficient key uniqueness
- **Caching user-specific data globally**: Security/privacy issue

### Memory

- **Unbounded collections**: Lists/arrays that grow without limit
- **Large object retention**: Holding references preventing GC
- **String concatenation in loops**: Use builder/join instead
- **Loading large files entirely**: Use streaming instead

### Questions to Ask
- "What's the time complexity of this operation?"
- "How does this behave with 10x/100x data?"
- "Is this result cacheable? Should it be?"
- "Can this be batched instead of one-by-one?"

---

## Boundary Conditions

### None/Null Handling

- **Missing null checks**: Accessing attributes on potentially null objects
- **Truthy/falsy confusion**: Truthy check when 0 or empty string are valid
- **Chained attribute access**: Deep property access hiding structural issues

### Empty Collections

- **Empty list not handled**: Code assumes collection has items
- **First/last element access**: Without length check

### Numeric Boundaries

- **Division by zero**: Missing check before division
- **Floating point comparison**: Using `==` instead of approximate comparison
- **Negative values**: Index or count that shouldn't be negative
- **Off-by-one errors**: Loop bounds, list slicing, pagination

### String Boundaries

- **Empty string**: Not handled as edge case
- **Whitespace-only string**: Passes truthy check but is effectively empty
- **Very long strings**: No length limits causing memory/display issues

### Questions to Ask
- "What if this is null/None?"
- "What if this collection is empty?"
- "What's the valid range for this number?"
- "What happens at the boundaries (0, -1, MAX)?"

---

## Observability

### Logging Quality

- **Missing structured logging**: Using string interpolation instead of structured format
- **Insufficient context**: Log messages missing correlation identifiers (request_id, task_id, etc.)
- **Missing error signatures**: Errors without stable, low-cardinality signatures for aggregation
- **Inconsistent log levels**: Using INFO for errors or DEBUG for critical events

### Metrics & Monitoring

- **Missing metrics for critical paths**: No counters/histograms for key operations
- **No latency tracking**: External calls without duration measurement
- **Missing health check endpoints**: No liveness/readiness probes
- **Alerting blind spots**: New failure modes without corresponding alerts

### Questions to Ask
- "If this fails in production, can I find the root cause from logs alone?"
- "Is there a metric that would fire an alert for this failure mode?"
- "Can I trace a request end-to-end through this code path?"

---

## Resource Management

### Context Managers / Cleanup

- **Missing cleanup**: Opening files, connections, or locks without proper cleanup
- **Manual resource management**: Using try/finally instead of language-provided patterns
- **Resource leak on error path**: Resources not released when exceptions occur

### Questions to Ask
- "Is every opened resource properly closed on all code paths?"
- "What happens if an exception occurs between acquire and release?"
