# Component Specification

> Workflow step: **D4. Component Specification**

Covers capturing high-fidelity designs and writing implementation specifications for each UI component.

## Design Refinement

### Refine Wireframes to High-Fidelity

```javascript
// Read the wireframe to understand current structure
pencil_batch_get({
  filePath: "designs/<feature>/design.pen",
  nodeIds: ["screenId"],
  readDepth: 5
})

// Update with final styles, content, and states
pencil_batch_design({ /* refine operations */ })
```

### Capture All States

Use `pencil_get_screenshot` for each component state:

| State | When to Capture |
|-------|----------------|
| Default | Base appearance |
| Hover | Mouse-over behavior |
| Active | Pressed/clicked state |
| Disabled | Non-interactive state |
| Error | Validation failure |
| Loading | Async operation in progress |

```javascript
pencil_get_screenshot({
  filePath: "designs/<feature>/design.pen",
  nodeId: "componentId"
})
```

## Specification Document

For each component, create a spec document at `designs/<feature>/components/<ComponentName>.md`.

### Template

```markdown
# ComponentName

## Props
\`\`\`typescript
interface ComponentNameProps {
  // typed props with descriptions
}
\`\`\`

## Variants
| Variant | Description | Visual |
|---------|-------------|--------|
| default | Base appearance | [screenshot] |

## States
| State | Trigger | Visual Change |
|-------|---------|---------------|
| hover | mouse enter | ... |
| active | mouse down | ... |
| disabled | prop: disabled | ... |
| error | validation fail | ... |
| loading | async operation | ... |

## Responsive
| Breakpoint | Layout |
|-----------|--------|
| mobile (<640px) | stacked |
| tablet (768-1023px) | 2-column |
| desktop (>=1024px) | side-by-side |

## Accessibility
- ARIA role: ...
- Keyboard navigation: ...
- Focus management: ...
- Screen reader: ...

## Animation
| Transition | Duration | Easing |
|-----------|----------|--------|
| hover scale | 150ms | ease-out |
| appear | 200ms | ease-in-out |
```

## Component-to-shadcn Mapping

Map each Pencil component to its shadcn/ui equivalent before writing the spec. See [tailwind-shadcn-mapping.md](tailwind-shadcn-mapping.md) for the full mapping table.

```javascript
// Discover reusable components in the design
pencil_batch_get({
  filePath: "designs/<feature>/design.pen",
  patterns: [{ reusable: true }],
  readDepth: 3
})
```

### Mapping Process

1. Identify each reusable Pencil component
2. Find the closest shadcn/ui component match
3. Document any customizations needed
4. Verify the shadcn/ui component covers all states

## Props Interface Guidelines

### Naming

- Use descriptive, specific names: `alertSeverity` not `type`
- Boolean props: `isDisabled`, `isLoading`, `hasError`
- Callback props: `onSelect`, `onClick`, `onChange`
- Optional props: use `?` with sensible defaults

### Common Prop Categories

| Category | Examples |
|----------|---------|
| Data | `title`, `description`, `items`, `value` |
| Appearance | `variant`, `size`, `className` |
| State | `isLoading`, `isDisabled`, `hasError` |
| Behavior | `onClick`, `onChange`, `onSubmit` |
| Accessibility | `ariaLabel`, `ariaDescribedBy` |
| Layout | `orientation`, `gap`, `columns` |

## Responsive Specification

For each component, define layout changes at breakpoints:

| Breakpoint | Width | What Changes |
|-----------|-------|-------------|
| sm | 640px | Side-by-side starts |
| md | 768px | Tablet layout |
| lg | 1024px | Desktop layout |
| xl | 1280px | Wide desktop |

See [responsive-breakpoints.md](responsive-breakpoints.md) for multi-artboard patterns.

## Accessibility Requirements

Every component spec must include:

1. **ARIA roles**: What semantic role does the component play?
2. **Keyboard navigation**: Can all interactions be performed via keyboard?
3. **Focus management**: Where does focus go when the component opens/closes?
4. **Screen reader**: What text is announced? Are there live regions?
5. **Color contrast**: Do color combinations meet WCAG 2.1 AA (4.5:1 for text)?

## Checklist

- [ ] High-fidelity design refined on Pencil canvas?
- [ ] Screenshots captured for all states (default, hover, active, disabled, error, loading)?
- [ ] Props interface defined with TypeScript types?
- [ ] Variants documented with visual references?
- [ ] States documented with triggers and visual changes?
- [ ] Responsive behavior specified at breakpoints?
- [ ] Accessibility requirements documented?
- [ ] Mapped to shadcn/ui equivalent?

## See Also

- [tailwind-shadcn-mapping.md](tailwind-shadcn-mapping.md) — Component mapping tables
- [design-to-code-workflow.md](design-to-code-workflow.md) — Code generation from specs
- [responsive-breakpoints.md](responsive-breakpoints.md) — Breakpoint patterns
