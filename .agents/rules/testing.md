# Testing Requirements

## Common
### Minimum Test Coverage: 80%

Test Types (ALL required):
1. **Unit Tests** - Individual functions, utilities, components
2. **Integration Tests** - API endpoints, database operations
3. **E2E Tests** - Critical user flows (framework chosen per language)

### Test-Driven Development

MANDATORY workflow:
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify coverage (80%+)

### Troubleshooting Test Failures

1. Use **tdd-guide** agent
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)

### Agent Support

- **tdd-guide** - Use PROACTIVELY for new features, enforces write-tests-first


## Python

### Framework

Use **pytest** as the testing framework.

### Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Test Organization

Use `pytest.mark` for test categorization:

```python
import pytest

@pytest.mark.unit
def test_calculate_total():
    ...

@pytest.mark.integration
def test_database_connection():
    ...
```

### Reference

See skill: `python-testing` for detailed pytest patterns and fixtures.

## TypeScript/JavaScript Testing

### Framework

- **Unit / Component tests**: Vitest + React Testing Library
- **E2E tests**: Playwright
- **API Mocking**: MSW (Mock Service Worker)

### Coverage

```bash
vitest run --coverage
```

### Unit & Component Testing

Test user-visible behavior with React Testing Library, NOT implementation details:

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UserCard } from './UserCard'

describe('UserCard', () => {
  it('should call onSelect when clicked', async () => {
    const user = userEvent.setup()
    const onSelect = vi.fn()

    render(<UserCard user={{ id: '1', name: 'Alice' }} onSelect={onSelect} />)

    await user.click(screen.getByRole('button'))
    expect(onSelect).toHaveBeenCalledWith('1')
  })
})
```

#### Selector Priority

Use selectors in this order of preference:

1. `getByRole` — semantic roles (preferred)
2. `getByLabelText` — form elements
3. `getByText` — visible text
4. `getByTestId` — last resort

**NEVER** use CSS class names or DOM hierarchy as selectors.

#### Hooks Testing

```typescript
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

it('should increment counter', () => {
  const { result } = renderHook(() => useCounter())

  act(() => result.current.increment())

  expect(result.current.count).toBe(1)
})
```

### API Mocking with MSW

Intercept network requests with MSW instead of mocking fetch/axios implementations:

```typescript
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Alice' })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### E2E Testing

Use **Playwright** as the E2E testing framework for critical user flows.

```typescript
import { test, expect } from '@playwright/test'

test('user login flow', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('user@example.com')
  await page.getByLabel('Password').fill('password')
  await page.getByRole('button', { name: 'Sign in' }).click()

  await expect(page).toHaveURL('/dashboard')
})
```

### Visual Regression Testing

Use Playwright's built-in screenshot comparison to catch unintended visual changes:

```typescript
import { test, expect } from '@playwright/test'

test('dashboard visual regression', async ({ page }) => {
  await page.goto('/dashboard')
  await expect(page).toHaveScreenshot('dashboard-full.png', {
    maxDiffPixelRatio: 0.01,
  })
})

test('alert card component states', async ({ page }) => {
  for (const variant of ['default', 'critical', 'warning']) {
    await page.goto(`/components/alert-card?variant=${variant}`)
    await expect(page.getByTestId('alert-card')).toHaveScreenshot(
      `alertcard-${variant}.png`,
      { maxDiffPixelRatio: 0.01 }
    )
  }
})
```

Baseline screenshots are committed to the repository. On failure, Playwright generates a diff image for review.

### Accessibility Testing

Use **axe-core** via `@axe-core/playwright` for automated WCAG 2.1 AA compliance checks:

```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('dashboard accessibility', async ({ page }) => {
  await page.goto('/dashboard')
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()
  expect(results.violations).toEqual([])
})
```

Automated checks cover: color contrast, ARIA attributes, semantic HTML, keyboard focus order, form labels. Manual review is still needed for: keyboard navigation flow, screen reader announcements, focus trap in modals.

Dependencies:

```bash
npm install --save-dev @axe-core/playwright
```

### Test Organization

Group tests with `describe` by feature, co-locate test files with source:

```
src/
├── components/
│   ├── UserCard.tsx
│   └── UserCard.test.tsx      # Component tests
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts        # Hook tests
├── lib/
│   ├── api.ts
│   └── api.test.ts            # Utility tests
└── __mocks__/
    └── handlers.ts            # MSW handlers
```

### Testing Anti-Patterns

**NEVER:**

- **Test mock behavior instead of real functionality** — asserting what the mock returns proves nothing
- **Add test-only methods to production code** — tests must not intrude on production code
- **Use async assertions inside `.forEach`** — use `for...of` or `Promise.all` + `.map` instead
- **Replace behavioral assertions with snapshots** — snapshots capture structural changes, not functional correctness
- **Depend on test execution order** — each test must be independent with no shared side effects
- **Test framework internals** — never assert React state values directly or call internal component methods

### Agent Support

- **tdd-guide** — TDD 红绿重构循环
- **e2e-runner** — Playwright E2E 测试执行