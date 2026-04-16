# Security Guidelines

## Common
### Mandatory Security Checks

Before ANY commit:
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitized HTML)
- [ ] CSRF protection enabled
- [ ] Authentication/authorization verified
- [ ] Rate limiting on all endpoints
- [ ] Error messages don't leak sensitive data

### Secret Management

- Secrets must not appear in source code — enforced by `pre-write-secrets` hook at write time
- Validate that required secrets are present at startup; rotate any that may have been exposed

### Security Response Protocol

If security issue found:
1. STOP immediately
2. Use **security-reviewer** agent
3. Fix CRITICAL issues before continuing
4. Rotate any exposed secrets
5. Review entire codebase for similar issues

## Python Security

### Secret Management

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]  # Raises KeyError if missing
```

### Reference

See skill: `django-security` for Django-specific security guidelines (if applicable).


## TypeScript/JavaScript Security

### Secret Management

Use `process.env` with startup validation — throw if missing, never silently default to undefined.

```typescript
const apiKey = process.env.API_KEY
if (!apiKey) throw new Error('API_KEY not configured')
```

### Agent Support

- Use **security-reviewer** skill for comprehensive security audits
