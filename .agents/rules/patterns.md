# Code Patterns

## Common Patterns
### Skeleton Projects

When implementing new functionality:
1. Search for battle-tested skeleton projects
2. Use parallel agents to evaluate options:
   - Security assessment
   - Extensibility analysis
   - Relevance scoring
   - Implementation planning
3. Clone best match as foundation
4. Iterate within proven structure

### Design Patterns

#### Repository Pattern

Encapsulate data access behind a consistent interface:
- Define standard operations: findAll, findById, create, update, delete
- Concrete implementations handle storage details (database, API, file, etc.)
- Business logic depends on the abstract interface, not the storage mechanism
- Enables easy swapping of data sources and simplifies testing with mocks

#### API Response Format

Use a consistent envelope for all API responses:
- Include a success/status indicator
- Include the data payload (nullable on error)
- Include an error message field (nullable on success)
- Include metadata for paginated responses (total, page, limit)


## Python Patterns

### Protocol (Duck Typing)

```python
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: str) -> dict | None: ...
    def save(self, entity: dict) -> dict: ...
```

### Dataclasses as DTOs

```python
from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int | None = None
```

### Context Managers & Generators

- Use context managers (`with` statement) for resource management
- Use generators for lazy evaluation and memory-efficient iteration

### Reference

See skill: `python-patterns` for comprehensive patterns including decorators, concurrency, and package organization.

## TypeScript/JavaScript Patterns

### API Response Format

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}
```

### Custom Hooks Pattern

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```

### Repository Pattern

```typescript
interface Repository<T> {
  findAll(filters?: Filters): Promise<T[]>
  findById(id: string): Promise<T | null>
  create(data: CreateDto): Promise<T>
  update(id: string, data: UpdateDto): Promise<T>
  delete(id: string): Promise<void>
}
```

### shadcn/ui Component Composition

Compose shadcn/ui primitives into domain-specific components. Use `cn()` for class merging and CVA for variant management.

#### Typed Component with Variants

```typescript
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
import { AlertTriangle, Info } from "lucide-react"

const alertCardVariants = cva("", {
  variants: {
    severity: {
      critical: "border-destructive",
      warning: "border-yellow-500",
      info: "border-primary",
    },
  },
  defaultVariants: {
    severity: "info",
  },
})

interface AlertCardProps extends VariantProps<typeof alertCardVariants> {
  title: string
  description: string
  className?: string
}

function AlertCard({ title, description, severity, className }: AlertCardProps) {
  return (
    <Card className={cn(alertCardVariants({ severity }), className)}>
      <CardHeader className="flex flex-row items-center gap-2">
        {severity === "critical" ? (
          <AlertTriangle className="h-4 w-4 text-destructive" />
        ) : (
          <Info className="h-4 w-4 text-primary" />
        )}
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  )
}
```

#### Component Extension Pattern

Wrap shadcn/ui components to add domain behavior while keeping the base component swappable:

```typescript
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

interface ActionButtonProps {
  loading?: boolean
  children: React.ReactNode
  onClick: () => void
}

function ActionButton({ loading, children, onClick }: ActionButtonProps) {
  return (
    <Button onClick={onClick} disabled={loading}>
      {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </Button>
  )
}
```

#### Design Token Usage in Components

Reference tokens through semantic Tailwind classes, never through hardcoded values. Tokens are defined in the CSS `@theme` block (from design-workflow token pipeline).

```typescript
// Tokens flow: Pencil variables → w3c.json → Style Dictionary → @theme → Tailwind classes

// CORRECT: Semantic classes that reference tokens
<div className="bg-card text-card-foreground rounded-lg p-6 shadow-md">
  <h2 className="text-lg font-semibold text-foreground">{title}</h2>
  <p className="text-sm text-muted-foreground">{description}</p>
</div>

// WRONG: Hardcoded values that bypass the design system
<div className="bg-white text-gray-900 rounded-lg p-6 shadow-md">
  <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
  <p className="text-sm text-gray-500">{description}</p>
</div>
```