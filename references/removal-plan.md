# Removal and Iteration Plan Template

## Priority Levels

- [ ] **P0**: Immediate removal needed (security risk, significant cost, blocking other work)
- [ ] **P1**: Remove in current sprint
- [ ] **P2**: Backlog / next iteration

---

## Safe to Remove Now

### Item: [Name/Description]

| Field | Details |
|-------|---------|
| **Location** | `path/to/file.py:line` |
| **Rationale** | Why this should be removed |
| **Evidence** | Unused (no references), dead feature flag, deprecated API |
| **Impact** | None / Low - no active consumers |
| **Deletion steps** | 1. Remove code 2. Remove tests 3. Remove config |
| **Verification** | Run tests, check no runtime errors, monitor logs |

---

## Defer Removal (Plan Required)

### Item: [Name/Description]

| Field | Details |
|-------|---------|
| **Location** | `path/to/file.py:line` |
| **Why defer** | Active consumers, needs migration, stakeholder sign-off |
| **Preconditions** | Feature flag off for 2 weeks, telemetry shows 0 usage |
| **Breaking changes** | List any API/contract changes |
| **Migration plan** | Steps for consumers to migrate |
| **Timeline** | Target date or sprint |
| **Owner** | Person/team responsible |
| **Validation** | Metrics to confirm safe removal (error rates, usage counts) |
| **Rollback plan** | How to restore if issues found |

---

## Checklist Before Removal

- [ ] Searched codebase for all references
- [ ] Checked for dynamic/reflection-based usage
- [ ] Verified no external consumers (APIs, SDKs, docs)
- [ ] Feature flag telemetry reviewed (if applicable)
- [ ] Tests updated/removed
- [ ] Documentation updated
- [ ] Team notified (if shared code)

---

## Language-Specific Considerations

### Dynamic References

Some languages allow dynamic imports, reflection, or string-based references that may hide usage. Search for patterns like:

- Dynamic imports (`importlib`, `require()`, `reflect`)
- String-based references to class/function names
- Decorator/annotation registration
- Plugin registration patterns

### Search Commands

```bash
# Find all references (adjust tool for your project)
rg "function_name" --type-add 'code:*.{py,js,ts,go,java}'

# Find dynamic usage patterns
rg "importlib|getattr|globals|require|reflect" --type-add 'code:*.{py,js,ts,go,java}'
```
