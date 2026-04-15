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

Use types to make public APIs, shared models, and component props explicit, readable, and reusable.

#### Public APIs

- Add parameter and return types to exported functions, shared utilities, and public class methods
- Let TypeScript infer obvious local variable types
- Extract repeated inline object shapes into named types or interfaces

```typescript
// WRONG: Exported function without explicit types
export function formatUser(user) {
  return `${user.firstName} ${user.lastName}`
}

// CORRECT: Explicit types on public APIs
interface User {
  firstName: string
  lastName: string
}

export function formatUser(user: User): string {
  return `${user.firstName} ${user.lastName}`
}
```

#### Interfaces vs. Type Aliases

- Use `interface` for object shapes that may be extended or implemented
- Use `type` for unions, intersections, tuples, mapped types, and utility types
- Prefer string literal unions over `enum` unless an `enum` is required for interoperability

```typescript
interface User {
  id: string
  email: string
}

type UserRole = 'admin' | 'member'
type UserWithRole = User & {
  role: UserRole
}
```

#### Avoid `any`

- Avoid `any` in application code
- Use `unknown` for external or untrusted input, then narrow it safely
- Use generics when a value's type depends on the caller

```typescript
// WRONG: any removes type safety
function getErrorMessage(error: any) {
  return error.message
}

// CORRECT: unknown forces safe narrowing
function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }

  return 'Unexpected error'
}
```

#### React Props

- Define component props with a named `interface` or `type`
- Type callback props explicitly
- Do not use `React.FC` unless there is a specific reason to do so

```typescript
interface User {
  id: string
  email: string
}

interface UserCardProps {
  user: User
  onSelect: (id: string) => void
}

function UserCard({ user, onSelect }: UserCardProps) {
  return <button onClick={() => onSelect(user.id)}>{user.email}</button>
}
```

#### JavaScript Files

- In `.js` and `.jsx` files, use JSDoc when types improve clarity and a TypeScript migration is not practical
- Keep JSDoc aligned with runtime behavior

```javascript
/**
 * @param {{ firstName: string, lastName: string }} user
 * @returns {string}
 */
export function formatUser(user) {
  return `${user.firstName} ${user.lastName}`
}
```

## Immutability

Use spread operator for immutable updates:

```typescript
interface User {
  id: string
  name: string
}

// WRONG: Mutation
function updateUser(user: User, name: string): User {
  user.name = name // MUTATION!
  return user
}

// CORRECT: Immutability
function updateUser(user: Readonly<User>, name: string): User {
  return {
    ...user,
    name
  }
}
```

### Error Handling

Use async/await with try-catch and narrow unknown errors safely:

```typescript
interface User {
  id: string
  email: string
}

declare function riskyOperation(userId: string): Promise<User>

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }

  return 'Unexpected error'
}

const logger = {
  error: (message: string, error: unknown) => {
    // Replace with your production logger (for example, pino or winston).
  }
}

async function loadUser(userId: string): Promise<User> {
  try {
    const result = await riskyOperation(userId)
    return result
  } catch (error: unknown) {
    logger.error('Operation failed', error)
    throw new Error(getErrorMessage(error))
  }
}
```

### Input Validation

Use Zod for schema-based validation and infer types from the schema:

```typescript
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

type UserInput = z.infer<typeof userSchema>

const validated: UserInput = userSchema.parse(input)
```

### Console-Based Debugging

- No ad-hoc console debugging statements in production code
- Use proper logging libraries instead
- See hooks for automatic detection

### Tailwind CSS v4

#### Semantic Classes Only

NEVER use arbitrary values. Always use semantic Tailwind utilities that map to design tokens.

```typescript
// WRONG: Arbitrary values bypass the design system
<div className="bg-[#3b82f6] rounded-[6px] p-[24px] text-[14px]">

// CORRECT: Semantic classes reference design tokens
<div className="bg-primary rounded-md p-6 text-sm">
```

#### CSS Theme Configuration

Use Tailwind v4 `@theme` blocks in CSS, not `tailwind.config.ts`:

```css
/* CORRECT: Tailwind v4 @theme block */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.6 0.2 260);
  --color-destructive: oklch(0.6 0.2 25);
  --radius-md: 0.375rem;
  --font-sans: "Inter", sans-serif;
}
```

```typescript
// WRONG: Tailwind v3 config file (do not use with v4)
// tailwind.config.ts
export default { theme: { extend: { ... } } }
```

#### Class Merging with cn()

Always use `cn()` from `@/lib/utils` to merge classes. Never concatenate class strings manually.

```typescript
import { cn } from "@/lib/utils"

// WRONG: String concatenation or template literals
<div className={"card " + (active ? "active" : "")}>
<div className={`card ${active ? "active" : ""}`}>

// CORRECT: cn() handles conflicts and conditionals
<div className={cn("rounded-md border", active && "ring-2 ring-primary")}>
```

### shadcn/ui Components

#### Import Convention

Import shadcn/ui components from `@/components/ui/`. Do not recreate components that shadcn already provides.

```typescript
// CORRECT: Use shadcn/ui components
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { Dialog, DialogContent } from "@/components/ui/dialog"
```

#### Component Extension

Extend shadcn/ui components for project-specific needs. Use CVA (class-variance-authority) for variants:

```typescript
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

const buttonVariants = cva("inline-flex items-center justify-center", {
  variants: {
    intent: {
      primary: "bg-primary text-primary-foreground hover:bg-primary/90",
      destructive: "bg-destructive text-destructive-foreground",
      ghost: "hover:bg-accent hover:text-accent-foreground",
    },
    size: {
      sm: "h-8 px-3 text-xs",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
    },
  },
  defaultVariants: {
    intent: "primary",
    size: "md",
  },
})
```

#### Icons

Use Lucide React icons. Do not use Material Icons or other icon libraries.

```typescript
// CORRECT
import { AlertTriangle, Check, X } from "lucide-react"

// WRONG
import WarningIcon from "@mui/icons-material/Warning"
```

### Lint Configuration

Enforce Tailwind/shadcn constraints at lint time:

```bash
npm install --save-dev eslint-plugin-tailwindcss
```

```javascript
// eslint.config.js — prevent arbitrary Tailwind values
{
  rules: {
    "tailwindcss/no-custom-classname": "error",  // blocks bg-[#hex], w-[375px], etc.
    "tailwindcss/classnames-order": "warn",       // consistent class ordering
  }
}
```
