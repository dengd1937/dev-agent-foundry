# Security and Reliability Checklist

## Input/Output Safety

- **XSS**: Unsafe HTML rendering in templates, missing auto-escaping
- **Injection**: SQL/NoSQL/command injection via string interpolation or concatenation
- **SSRF**: User-controlled URLs reaching internal services without allowlist validation
- **Path traversal**: User input in file paths without sanitization (`../` attacks)

## AuthN/AuthZ

- Missing tenant or ownership checks for read/write operations
- New endpoints without auth guards or RBAC enforcement
- Trusting client-provided roles/flags/IDs
- Broken access control (IDOR - Insecure Direct Object Reference)
- Session fixation or weak session management

## JWT & Token Security

- Algorithm confusion attacks (accepting `none` algorithm)
- Weak or hardcoded secrets
- Missing expiration (`exp`) or not validating it
- Sensitive data in JWT payload (tokens are base64, not encrypted)
- Not validating `iss` (issuer) or `aud` (audience)

## Secrets and PII

- API keys, tokens, or credentials in code/config/logs
- Secrets in git history or environment variables exposed to client
- Excessive logging of PII or sensitive payloads
- Missing data masking in error messages

## Dependencies & Supply Chain

- Unpinned dependencies allowing malicious updates
- Dependency confusion (private package name collision)
- Installing from untrusted sources
- Outdated dependencies with known CVEs

## CORS & Headers

- Overly permissive CORS (`allow_origins=["*"]` with credentials)
- Missing security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- Exposed internal headers or stack traces in production

## Runtime Risks

- Unbounded loops, recursive calls, or large in-memory buffers
- Missing timeouts, retries, or rate limiting on external calls
- Blocking operations in async context
- Resource exhaustion (file handles, connections, memory)
- ReDoS (Regular Expression Denial of Service)

## Cryptography

- Weak algorithms (MD5, SHA1 for security purposes)
- Hardcoded IVs or salts
- Using encryption without authentication (ECB mode)
- Insufficient key length
- Insecure random number generation (using math/random instead of crypto/secure random)

## Race Conditions

### Shared State Access
- Multiple concurrent tasks accessing shared variables without synchronization
- Global state or singletons modified concurrently
- Lazy initialization without proper locking

### Check-Then-Act (TOCTOU)
- `if exists: then use` patterns without atomic operations
- `if authorized: then perform` where authorization can change
- File existence check followed by file operation

### Database Concurrency
- Missing optimistic locking
- Missing pessimistic locking
- Read-modify-write without transaction isolation
- Counter increments without atomic operations

### Questions to Ask
- "What happens if two requests hit this code simultaneously?"
- "Is this operation atomic or can it be interrupted?"
- "What shared state does this code access?"

## File Upload

- **Missing file type validation**: Only checking extension, not MIME type or magic bytes
- **No file size limit**: Allowing arbitrarily large uploads
- **Unsafe storage path**: Using user-provided filenames directly
- **Missing content inspection**: Accepting files without validation

## Open Redirect

- **Unvalidated redirect URLs**: Accepting user-controlled redirect parameters
- **Protocol-relative URLs**: `//evil.com` bypassing naive domain checks
- **URL parsing bypass**: Using `@` in URLs

## Mass Assignment

- **Accepting all fields from request**: Passing raw request data to model updates without filtering
- **Missing field-level access control**: Admin-only fields modifiable by regular users

## Data Integrity

- Missing transactions, partial writes, or inconsistent state updates
- Weak validation before persistence
- Missing idempotency for retryable operations
- Lost updates due to concurrent modifications
