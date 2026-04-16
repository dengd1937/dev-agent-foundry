# Coding Style

## Common
### Immutability (CRITICAL)

ALWAYS create new objects, NEVER mutate existing ones:

```
// Pseudocode
WRONG:  modify(original, field, value) → changes original in-place
CORRECT: update(original, field, value) → returns new copy with change
```

Rationale: Immutable data prevents hidden side effects, makes debugging easier, and enables safe concurrency.

### File Organization

MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large modules
- Organize by feature/domain, not by type

### Error Handling

ALWAYS handle errors comprehensively:
- Handle errors explicitly at every level
- Provide user-friendly error messages in UI-facing code
- Log detailed error context on the server side
- Never silently swallow errors

### Input Validation

ALWAYS validate at system boundaries:
- Validate all user input before processing
- Use schema-based validation where available
- Fail fast with clear error messages
- Never trust external data (API responses, user input, file content)

### Surgical Edits

When modifying existing code:
- Every changed line should trace directly to the task at hand
- If you notice unrelated dead code, mention it to the user — don't delete it
- Only remove imports/variables/functions that YOUR changes made unused
- Don't refactor or reformat adjacent code that you weren't asked to change

### Code Quality Checklist

Before marking work complete:
- [ ] Code is readable and well-named
- [ ] Functions are small (<50 lines)
- [ ] Files are focused (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Proper error handling
- [ ] No hardcoded values (use constants or config)
- [ ] No mutation (immutable patterns used)


## Python Coding Style


### Standards

- Follow **PEP 8** conventions
- Use **type annotations** on all function signatures

### Immutability

Prefer immutable data structures:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

### Formatting

- **black** for code formatting
- **isort** for import sorting
- **ruff** for linting

### Reference

See skill: `python-patterns` for comprehensive Python idioms and patterns.

## TypeScript/JavaScript Coding Style

### Types and Interfaces

- Add parameter and return types to exported functions, shared utilities, and public class methods
- Let TypeScript infer obvious local variable types; extract repeated shapes into named types/interfaces
- Use `interface` for extensible object shapes; use `type` for unions, intersections, mapped types
- Prefer string literal unions over `enum`
- Avoid `any`; use `unknown` for external input, then narrow safely
- Define component props with a named `interface` or `type`; do not use `React.FC`
- In `.js/.jsx` files, use JSDoc when types improve clarity

### Immutability

Use spread operator for immutable updates; never mutate existing objects.

```typescript
function updateUser(user: Readonly<User>, name: string): User {
  return { ...user, name }
}
```

### Error Handling

Use async/await with try-catch; narrow `unknown` errors with `instanceof Error` check.

```typescript
function getErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message
  return 'Unexpected error'
}
```

### Input Validation

Use Zod for schema-based validation; infer types with `z.infer<typeof schema>`.

```typescript
const userSchema = z.object({ email: z.string().email(), age: z.number().int().min(0) })
type UserInput = z.infer<typeof userSchema>
```

### Tailwind CSS v4

- Semantic classes only: `bg-primary`, `rounded-md` — never `bg-[#hex]`, `w-[375px]`, `rounded-[6px]`
- CSS `@theme` blocks only — no `tailwind.config.ts` (Tailwind v3 config)
- Class merging: `cn()` from `@/lib/utils` — never string concatenation or template literals
  示例：`className={cn("rounded-md border", active && "ring-2 ring-primary")}`

### shadcn/ui Components

- Import from `@/components/ui/` — do not recreate components shadcn provides
- Component variants: use CVA (class-variance-authority)
- Icons: Lucide React only — no Material Icons or other libraries
- Lint: `eslint-plugin-tailwindcss` with `no-custom-classname: "error"`

```typescript
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
```

### Reference

See skill: `typescript-patterns` for comprehensive TypeScript/React/shadcn/Tailwind patterns and code examples.
