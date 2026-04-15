# Design Workflow

> This file defines the independent design workflow using Pencil MCP and Style Dictionary.
> The design workflow runs in parallel to the [development workflow](./development-workflow.md)
> and produces artifacts that feed into the dev workflow at the handoff point.

## When to Activate

**Activate when:**

- New UI feature or significant UI change
- Design system creation or update
- Component library work
- Visual or layout decisions needed
- Frontend implementation involving Next.js + TypeScript

**Skip when:**

- Backend-only work
- Configuration changes without visual impact
- Documentation-only changes
- Refactoring without visual changes
- No UI involved

## Prerequisites

- Pencil MCP server running locally (desktop client or IDE extension)
- [pencil-design skill](../.agents/skills/pencil-design/SKILL.md) installed (built-in, self-managed)
- `style-dictionary` and `style-dictionary-utils` available for token pipeline

---

## Design Implementation Workflow

### D1. Design Discovery

Investigate requirements and gather references before creating any design.

**Actions:**

- Analyze the UI scope: which pages, components, and interactions are involved
- Search project for existing `designs/` directory and reusable `.pen` files
- Use `pencil_batch_get` with `patterns: [{ reusable: true }]` to discover existing design system components
- Use `pencil_get_variables` to read existing design tokens
- Use Context7 to review Next.js / React component patterns
- Search for open-source implementations that solve similar UI problems
- Document design intent, reference sources, and design direction

**Output:**

- `docs/plans/<feature>-design.md` — design intent document (requirements interpretation, references, direction)

**Completion gate:** User confirms the design direction is aligned with intent.

---

### D2. Wireframe & Layout

Build page structure and layout on the Pencil canvas.

**Actions:**

Follow the **pencil-design skill** workflow and its 6 critical rules:

1. Follow shadcn/ui aesthetic direction (see pencil-design skill Rule 6)
2. Use `pencil_get_editor_state` to understand file state
3. Use `pencil_batch_get` to discover reusable components
4. Use `pencil_batch_design` to create page structure (header, sidebar, main content, footer)
5. Use `pencil_get_screenshot` to render previews for review
6. Use `pencil_snapshot_layout` with `problemsOnly: true` to verify layout correctness
7. Iterate: user feedback → modify → re-screenshot → confirm

**Enforced rules from pencil-design skill:**

- Rule 1: Always reuse design system components (never recreate from scratch)
- Rule 3: Prevent text and content overflow
- Rule 4: Visually verify every section (screenshot after each section)
- Rule 5: Reuse existing assets (logos, icons, images)

**Output:**

- `designs/<feature>/wireframes.pen` — wireframe design file
- `designs/<feature>/screenshots/wireframe-v1.png` — wireframe screenshot for documentation

**Completion gate:** User confirms page layout and region划分 matches expectations.

---

### D3. Design Tokens

Define the visual foundation through a standardized token pipeline.

**Actions:**

1. **Define variables in Pencil** using `pencil_set_variables`:
   - Colors: primary, secondary, semantic (success/error/warning), neutral scale, surface colors
   - Typography: font families, size scale, weights, line heights
   - Spacing: scale values (xs/sm/md/lg/xl)
   - Borders: radii (sm/md/lg/xl), widths
   - Shadows: elevation levels (sm/md/lg)
   - Breakpoints: responsive thresholds (sm/md/lg/xl)
   - Follow the naming convention from pencil-design skill: `primary`, `radius-md`, `muted-foreground`, etc.

2. **Run token pipeline:**
   ```
   Pencil flat variables → scripts/tokens-convert.ts → W3C DTCG JSON → Style Dictionary → code outputs
   ```

3. **Verify generated outputs:**
   - `tokens.css` contains valid CSS custom properties
   - `tokens.ts` contains typed constant references
   - `tailwind-preset.ts` maps tokens to Tailwind v4 `@theme` declarations

**Output:**

```
designs/<feature>/tokens/
├── w3c.json                # W3C DTCG standard format (intermediate)
├── tokens.css              # CSS custom properties
├── tokens.ts               # TypeScript typed constants
└── tailwind-preset.ts      # Tailwind v4 preset plugin
```

**Token pipeline detail:**

| Stage | Input | Output | Tool |
|-------|-------|--------|------|
| Pencil variables | Key-value pairs (e.g., `"primary": "#3b82f6"`) | Flat JSON | `pencil_get_variables` |
| W3C DTCG conversion | Flat JSON | Nested `$value`/`$type` JSON | `scripts/tokens-convert.ts` |
| Style Dictionary build | W3C DTCG JSON | CSS + TS + Tailwind preset | `style-dictionary` + `style-dictionary-utils` |

**Enforced rules from pencil-design skill:**

- Rule 2: Always use variables instead of hardcoded values (no `bg-[#3b82f6]`, use `bg-primary`)
- Rule 6: Follow shadcn/ui aesthetic direction

**Completion gate:** User confirms the token system covers all visual requirements.

---

### D4. Component Specification

Define detailed implementation specifications for each UI component.

**Actions:**

1. Refine wireframes to high-fidelity designs on Pencil canvas using `pencil_batch_design`
2. Capture component screenshots for all states using `pencil_get_screenshot`:
   - Default, hover, active, disabled, error, loading
3. For each component, write a specification document containing:
   - **Props interface** — TypeScript type definition
   - **Variants** — visual variants (e.g., button: primary/secondary/ghost/destructive)
   - **States** — interaction states and their visual representation
   - **Responsive behavior** — layout changes at breakpoints
   - **Accessibility** — ARIA roles, keyboard navigation, focus management, screen reader considerations
   - **Animation** — transition specs (duration, easing) if applicable
4. Map Pencil components to shadcn/ui equivalents using the pencil-design skill mapping table

**Output:**

```
designs/<feature>/
├── design.pen                        # Final high-fidelity design
├── components/
│   ├── AlertCard.md                  # Component specification
│   ├── Dashboard.md
│   └── IncidentTimeline.md
└── screenshots/
    ├── alertcard-default.png
    ├── alertcard-critical.png
    ├── alertcard-warning.png
    ├── dashboard-full.png
    └── dashboard-mobile.png
```

**Component spec template:**

```markdown
# ComponentName

## Props
\`\`\`typescript
interface ComponentNameProps {
  // typed props
}
\`\`\`

## Variants
| Variant | Description | Visual |
|---------|-------------|--------|
| default | ... | [screenshot] |

## States
| State | Trigger | Visual Change |
|-------|---------|---------------|
| hover | mouse enter | ... |

## Responsive
| Breakpoint | Layout |
|-----------|--------|
| mobile (<640px) | stacked |
| desktop (>=1024px) | side-by-side |

## Accessibility
- ARIA role: ...
- Keyboard: ...
- Focus management: ...
```

**Completion gate:** All components have specs covering props, variants, states, responsive behavior, and accessibility.

---

### D5. Design Review [gate]

Adversarial review of all design artifacts before handoff. Three-phase execution:

**Phase 1 — Visual & Accessibility Checks (主对话执行)**

1. Use `pencil_get_screenshot` on the final design to capture full-page screenshot
2. Use `pencil_snapshot_layout({ problemsOnly: true })` on all screens
3. Run Playwright visual regression baseline (if frontend is deployed):
   ```bash
   npx playwright test --update-snapshots
   ```
4. Run axe-core accessibility audit (if frontend is deployed):
   ```bash
   npx playwright test --grep "accessibility"
   ```
5. Save results to filesystem:
   - Screenshots → `designs/<feature>/screenshots/`
   - Layout issues → `designs/<feature>/screenshots/layout-report.md`
   - Visual regression results → `designs/<feature>/screenshots/visual-regression-report.md`
   - Accessibility audit results → `designs/<feature>/screenshots/accessibility-report.md`

> Note: Steps 3-4 require the frontend to be deployed. If not yet deployed, these checks run during the development workflow at Step 3 (TDD). The agent will flag missing reports accordingly.

**Phase 2 — design-reviewer Agent (独立审查)**

Spawn the **design-reviewer** agent with the `designs/<feature>/` directory path. The agent reads all artifacts from filesystem and performs 5-dimension review:

| Dimension | What It Checks |
|-----------|---------------|
| Token Coverage | All component references backed by tokens, no hardcoded values, cross-file consistency |
| Spec Completeness | Props/Variants/States/Responsive/A11y sections present and well-typed |
| Layout & Visual Integrity | Layout report issues, token value consistency, visual evidence coverage, Playwright diff results |
| Accessibility | axe-core automated results + ARIA/keyboard/focus documentation in component specs |
| Responsive Coverage | Mobile + desktop breakpoints, no hardcoded widths, sensible layout changes |

> Note: The agent runs on a text-only model and cannot analyze PNG screenshots. Visual quality is verified by Playwright screenshot diff (automated) and human review (Phase 3).

**Phase 3 — User Approval**

1. Review the agent's report in conversation
2. **[Hard Gate]** Present all design artifacts + review report to user for approval
3. Delete `docs/plans/<feature>-design.md` after approval (process artifact, not long-term knowledge)

**Output:**

- Design review report (output in conversation, not written to file)
- Approval decision from user

**Completion gate:** User explicitly approves → proceed to handoff.

---

## Handoff to Development Workflow

After D5 approval, the following artifacts are available:

```
designs/<feature>/
├── design.pen                        # Pencil final design file
├── wireframes.pen                    # Wireframes (process artifact)
├── tokens/
│   ├── w3c.json                      # W3C DTCG standard format
│   ├── tokens.css                    # CSS custom properties
│   ├── tokens.ts                     # TypeScript typed constants
│   └── tailwind-preset.ts            # Tailwind v4 preset
├── components/
│   ├── AlertCard.md                  # Component specifications
│   ├── Dashboard.md
│   └── IncidentTimeline.md
└── screenshots/
    ├── layout-report.md              # Pencil layout check results
    ├── visual-regression-report.md   # Playwright screenshot diff results
    ├── accessibility-report.md       # axe-core audit results
    ├── wireframe-v1.png
    ├── alertcard-critical.png
    ├── alertcard-warning.png
    └── dashboard-full.png
```

These artifacts are consumed by the development workflow at specific steps:

| Dev Step | Consumes | How |
|----------|----------|-----|
| Step 1 (Research & Reuse) | `design.pen`, `screenshots/` | Read design intent, confirm implementation direction |
| Step 2 (Plan First) | `components/*.md` | Reference component specs in implementation plan |
| Step 3 (TDD) | `tokens/tokens.css`, `tokens/tokens.ts`, `tokens/tailwind-preset.ts` | Validate components use token values, not hardcoded values |

Steps 4-8 of the development workflow remain unchanged.

---

## Token Pipeline

The full Style Dictionary pipeline for converting Pencil design tokens to code:

```
pencil_get_variables
        ↓ flat key-value (e.g., "primary": "#3b82f6")
scripts/tokens-convert.ts
        ↓ Pencil flat → W3C DTCG JSON
designs/<feature>/tokens/w3c.json
        ↓
Style Dictionary + style-dictionary-utils
        ↓ build
  ├── tokens.css              (--color-primary: #3b82f6; ...)
  ├── tokens.ts               (export const tokens = { color: { primary: "var(--color-primary)" } } as const)
  └── tailwind-preset.ts      (Tailwind v4 plugin with @theme declarations)
```

### W3C DTCG Format

Intermediate format following the [W3C Design Tokens Community Group](https://design-tokens.github.io/community-group/format/) specification:

```json
{
  "color": {
    "primary": { "$value": "#3b82f6", "$type": "color" },
    "success": { "$value": "#22c55e", "$type": "color" }
  },
  "spacing": {
    "md": { "$value": "1rem", "$type": "dimension" }
  },
  "border": {
    "radius": {
      "md": { "$value": "0.375rem", "$type": "dimension" }
    }
  }
}
```

### Conversion Rules

| Pencil variable pattern | W3C `$type` | Example |
|------------------------|-------------|---------|
| Hex color values (`#...`) | `color` | `"primary": "#3b82f6"` → `$type: "color"` |
| Values with rem/px units | `dimension` | `"radius-md": "0.375rem"` → `$type: "dimension"` |
| Font family values | `fontFamily` | `"font-sans": "Inter, sans-serif"` → `$type: "fontFamily"` |
| Numeric-only values | `number` | `"font-weight-normal": "400"` → `$type: "number"` |

### Dependencies

```bash
npm install --save-dev style-dictionary style-dictionary-utils
```

---

## Execution Layer

This workflow delegates Pencil MCP tool operations to the built-in pencil-design skill:

### pencil-design skill

- **Source:** Built-in ([`.agents/skills/pencil-design/`](../.agents/skills/pencil-design/SKILL.md))
- **Based on:** [chiroro-jr/pencil-design-skill](https://github.com/chiroro-jr/pencil-design-skill) (MIT), [partme-ai/pencil-skills](https://github.com/partme-ai/pencil-skills) (Apache 2.0)
- **Covers:**
  - 6 critical rules for working with Pencil MCP tools
  - MCP tool usage patterns (14 tools)
  - Tailwind v4 + shadcn/ui code generation mapping
  - Style Dictionary token pipeline integration
  - Component reuse, variable usage, overflow prevention, visual verification
  - 7 reference documents aligned with D2-D4 workflow steps

This workflow references the skill's rules at each step rather than duplicating them.

### design-reviewer agent

- **Source:** Built-in ([`.claude/agents/design-reviewer.md`](../../.claude/agents/design-reviewer.md))
- **Trigger:** D5 gate — before design handoff to development
- **Execution:** Spawned as sub-agent with isolated context; reads design artifacts from filesystem only
- **Covers:**
  - 5-dimension design artifact review (token coverage, spec completeness, visual quality, accessibility, responsive)
  - Cross-reference checks (token → component, component → screenshot, spec → Tailwind mapping)
  - Failure mode analysis
  - Approval/blocking criteria

> Note: The `design-review` *skill* (`.agents/skills/design-review/`) remains available for plan-level reviews in the development workflow Step 2. The `design-reviewer` *agent* is specific to design artifact review in D5.

---

## Integration with Development Workflow

This design workflow is **independent and optional**. When no UI work is involved, the development workflow (defined in [development-workflow.md](./development-workflow.md)) runs unchanged.

When design artifacts exist in `designs/<feature>/`, the development workflow steps 1-3 should:

- **Step 1 (Research & Reuse):** Check `designs/<feature>/` for `.pen` files, screenshots, and component specs. Use `pencil_batch_get` and `pencil_get_screenshot` to inspect designs.
- **Step 2 (Plan First):** Reference component specs in the implementation plan. Use design tokens for all visual values.
- **Step 3 (TDD):** Tests should validate components use token values (not hardcoded values).
