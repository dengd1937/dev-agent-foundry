# Design Workflow

> This file defines the optimized design workflow v2 for UI work using Pencil MCP and Style Dictionary.
> The design workflow runs alongside the [development workflow](./development-workflow.md)
> and hands approved artifacts to development at the final review gate.

## When to Activate

**Activate when:**

- New UI feature or significant UI change
- Design system creation or update
- Component library work
- Visual or layout decisions are required
- Frontend implementation involving Next.js + TypeScript

**Skip when:**

- Backend-only work
- Configuration changes without visual impact
- Documentation-only changes
- Refactoring without visual changes
- No UI is involved

## Prerequisites

- Pencil MCP server running locally (desktop client or IDE extension)
- [pencil-design skill](../skills/pencil-design/SKILL.md) installed
- `style-dictionary` and `style-dictionary-utils` available for the token pipeline

---

## Core Rules

The v2 workflow keeps the pipeline strict where it matters and lighter everywhere else.

1. **Route UI work up front.**
   - Small UI tweaks go through `L1`.
   - New pages, new components, new interactions, or new tokens go through `L2`.
2. **Only three design gates exist in the standard path.**
   - `Gate 1`: direction confirmation
   - `Gate 2`: layout confirmation
   - `Gate 3`: final approval before handoff
3. **Tokens remain the source of truth.**
   - Do not hardcode visual values.
   - Do not edit generated token files by hand.
4. **Design docs capture constraints, not duplicate implementation.**
   - Markdown component docs describe behavior, mapping, responsive rules, accessibility, and visual constraints.
   - Source code owns the final TypeScript props and implementation details.

---

## Directory Layout

All design artifacts live under a single feature directory. Do not spread design docs between `docs/plans/` and `designs/`.

```text
designs/<feature>/
├── intent.md                         # V2-1: design intent and decision log
├── wireframes.pen                    # V2-2: wireframe file
├── design.pen                        # V2-3: final high-fidelity design
├── tokens/
│   ├── w3c.json                      # Source of truth for design tokens
│   ├── tokens.css                    # Generated CSS custom properties
│   ├── tokens.ts                     # Generated TypeScript token constants
│   └── tailwind-preset.ts            # Generated Tailwind v4 preset
├── components/
│   └── *.md                          # V2-3: key component contracts
├── screenshots/
│   ├── *.png                         # Approved screenshots only
│   ├── layout-report.md              # V2-4: Pencil layout check results
│   ├── baselines/                    # Dev Step 3: Playwright visual baselines
│   ├── visual-regression-report.md   # Dev Step 3: Playwright diff results
│   ├── accessibility-report.md       # Dev Step 3: axe-core audit results
│   └── .tmp/                         # Intermediate screenshots (gitignored)
└── review-verdict.md                 # V2-4: design-reviewer verdict + approval
```

**Git rules:**

- Add `designs/**/screenshots/.tmp/` to `.gitignore`.
- Only promote screenshots from `.tmp/` to `screenshots/` after approval.
- `intent.md` is long-term knowledge. Keep it for the life of the feature.

---

## Workflow Levels

### L1. Lightweight UI Change

Use `L1` when all of the following are true:

- No new page or major layout pattern
- No new interaction model
- No new design-system component
- No new token is required

**Actions:**

1. Confirm the change is local and does not introduce new design primitives.
2. Capture before/after screenshots for the affected area.
3. Record a short note in `intent.md` or the PR description:
   - what changed
   - why it changed
   - which existing tokens/components were reused
4. Proceed directly to the development workflow Step 2 and Step 3.

**Outputs:**

- Updated screenshot(s) for the affected surface
- A short design note in `intent.md` or the PR

**Escalation rule:** If the change grows into a new page, new interaction, or new token, upgrade immediately to `L2`.

### L2. Standard Design Workflow

Use `L2` for:

- New pages or substantial layout changes
- New reusable components
- Complex states or interaction flows
- Design-system updates
- Any change that introduces or expands tokens

The standard path has five stages and three gates.

---

## L2 Standard Workflow

### V2-1. Design Intent

Investigate requirements and establish design direction before editing the canvas.

**Actions:**

- Analyze the UI scope: pages, components, interactions, and constraints
- Search the project for reusable design assets and existing `designs/` directories
- Use `pencil_batch_get` with `patterns: [{ reusable: true }]` to discover reusable components
- Use `pencil_get_variables` to inspect the existing token system
- Review relevant frontend patterns and references
- Write the design intent, references, direction, and decision rationale

**Output:**

- `designs/<feature>/intent.md`

**Gate 1:** User confirms the design direction.

---

### V2-2. Wireframe + Baseline Tokens

Create the page structure and establish the minimum token set needed to support it. This stage merges the old token-baseline step and wireframing step so the team does not stop twice before layout approval.

**Actions:**

1. Define or confirm the baseline tokens in Pencil:
   - brand colors: `primary`, `secondary`, `accent`
   - semantic colors: `destructive`, `success`, `warning`, `muted`
   - surface and UI colors: `background`, `foreground`, `card`, `card-foreground`, `popover`, `popover-foreground`, `border`, `input`, `ring`, `muted-foreground`
   - typography: `font-sans`, `font-mono`, `font-heading`, `text-xs/sm/base/lg/xl`
   - radius: `radius-sm/md/lg/xl`
2. Verify tokens with `pencil_get_variables`.
3. Build the wireframe and page regions using reusable components and tokenized values only.
4. Capture review screenshots to `screenshots/.tmp/`.
5. Run `pencil_snapshot_layout({ problemsOnly: true })` on the affected screens.
6. Iterate until the page structure and regions are stable.

**Outputs:**

- `designs/<feature>/wireframes.pen`
- Final approved wireframe screenshot(s) in `designs/<feature>/screenshots/`

**Gate 2:** User confirms layout, page regions, and overall structure.

---

### V2-3. High-Fidelity Design + Token Expansion + Key Component Contracts

Refine the wireframe into the final design, expand the token system, and document only the component constraints that development genuinely needs.

**Actions:**

1. Refine the design to high fidelity in `design.pen`.
2. Expand the token set with context-dependent values:
   - spacing scale: `spacing-xs/sm/md/lg/xl/2xl`
   - shadow levels: `shadow-sm/md/lg/xl`
   - breakpoints: `breakpoint-sm/md/lg/xl`
   - theme variants for relevant tokens
3. Run the token pipeline:

   ```text
   Pencil variables -> scripts/tokens-convert.ts -> W3C DTCG JSON -> Style Dictionary -> code outputs
   ```

4. Verify generated outputs:
   - `tokens.css`
   - `tokens.ts`
   - `tailwind-preset.ts`
5. Capture final component and screen screenshots to `screenshots/.tmp/`, then promote approved results.
6. Write component contracts only for key components or screens that need implementation guidance.

**Required sections for each `components/*.md`:**

- `## Variants`
- `## States`
- `## Responsive`
- `## Accessibility`
- `## Implementation Mapping`
- `## Design Constraints`

**Optional sections:**

- `## API Notes`
- `## Animation`

**Rule:** Do not duplicate full TypeScript props interfaces in markdown unless design decisions directly constrain the public API. Source code remains the authority for props.

**Outputs:**

```text
designs/<feature>/
├── design.pen
├── tokens/
│   ├── w3c.json
│   ├── tokens.css
│   ├── tokens.ts
│   └── tailwind-preset.ts
├── components/
│   └── *.md
└── screenshots/
    ├── <component>-<variant>.png
    ├── <screen>-desktop.png
    └── <screen>-mobile.png
```

**Completion standard:** Key components are covered, and generated token outputs are consistent with `w3c.json`.

---

### V2-4. Design Review [hard gate]

Review all design artifacts before handoff. This is the single hard approval gate in the standard path.

> Playwright visual regression and axe-core accessibility audits still belong to the development workflow Step 3. `V2-4` reviews design-time artifacts only.

**Phase 1 - Design-time visual checks**

1. Capture final screenshots for each documented breakpoint.
2. Run `pencil_snapshot_layout({ problemsOnly: true })` on relevant screens.
3. Save results:
   - approved screenshots -> `designs/<feature>/screenshots/`
   - layout issues -> `designs/<feature>/screenshots/layout-report.md`

**Phase 2 - `design-reviewer` agent**

Run the `design-reviewer` agent against `designs/<feature>/`. The agent checks:

| Dimension | What It Checks |
|-----------|----------------|
| Token Coverage | All referenced visual values are backed by tokens; no drift between `w3c.json`, `tokens.css`, and `tailwind-preset.ts` |
| Contract Completeness | Each component contract includes Variants, States, Responsive, Accessibility, Implementation Mapping, and Design Constraints |
| Artifact Consistency | Filesystem layout is correct; required screenshots exist; layout-report issues are resolved |
| Accessibility Documentation | Interactive components describe ARIA roles, keyboard behavior, and focus management |
| Responsive Coverage | Contracts cover mobile and desktop behavior; no hardcoded pixel assumptions in the contract docs |

**Visual quality is still reviewed by humans, not the agent.**

**Phase 3 - User approval**

1. Review the artifact report in conversation.
2. Present final screenshots and review findings.
3. On approval, write the verdict and approval decision to `designs/<feature>/review-verdict.md`.

**Outputs:**

- `designs/<feature>/screenshots/layout-report.md`
- `designs/<feature>/review-verdict.md`
- Design review report in conversation

**Gate 3:** User explicitly approves. Only then does the workflow hand off to development.

---

### V2-5. Handoff to Development Workflow

After `Gate 3`, the design artifacts become inputs to the development workflow.

| Dev Step | Consumes | How |
|----------|----------|-----|
| Step 1 (Research & Reuse) | `intent.md`, `design.pen`, screenshots | Confirm direction, inspect final design, and understand the visual target |
| Step 2 (Plan First) | `components/*.md`, `review-verdict.md` | Reference component contracts and review findings in the implementation plan |
| Step 3 (TDD) | `tokens/*`, `components/*.md` | Validate token usage, run Playwright visual regression, run axe-core accessibility audit |

**Implementation-side rule:** If implementation changes the visual contract or reveals a missing token, update `designs/<feature>/` in the same PR. Do not patch around the gap with hardcoded values.

---

## Iteration Loops

The workflow remains iterative, but the loops are now simpler.

### L1 -> L2 (scope expansion)

If a lightweight change grows into a new page, interaction, or token, stop and switch to `L2`.

### V2-2 / V2-3 -> V2-3 (missing token)

If design work or implementation reveals a missing token:

1. Add it in Pencil with `pencil_set_variables`
2. Re-run the token pipeline
3. Update `designs/<feature>/tokens/` in the same change
4. Resume the interrupted step

Never edit `w3c.json`, `tokens.css`, `tokens.ts`, or `tailwind-preset.ts` by hand as a shortcut.

### V2-4 -> V2-3 (review findings)

If review finds incomplete contracts, unresolved layout issues, or mapping gaps:

1. Return to `V2-3`
2. Update the design, screenshots, or contracts
3. Re-run `V2-4`

### Dev Step 3 -> V2-3 (implementation discovered a design gap)

If development uncovers a missing contract detail, token gap, or responsive mismatch:

1. Update the design artifact in the same PR
2. Re-run the relevant token or screenshot steps
3. Keep code and design artifacts aligned before merge

### Full rebuild

If the design direction changes fundamentally:

1. Update `intent.md` with the new rationale and keep the old rationale in the decision log
2. Restart from `V2-1`

---

## Version Control Strategy

`.pen` files are binary. They cannot be diffed or merged reliably by git.

### File Ownership

- One `.pen` file pair per feature: `wireframes.pen` and `design.pen`
- Keep `wireframes.pen` and `design.pen` separate
- Do not edit the same `.pen` file in parallel on multiple branches

### What to Commit

| Artifact | Commit? | Reviewable? |
|----------|---------|-------------|
| `intent.md` | Yes | Text diff |
| `wireframes.pen` / `design.pen` | Yes | Screenshots only |
| `tokens/w3c.json` | Yes | Text diff |
| `tokens/tokens.css` / `tokens.ts` / `tailwind-preset.ts` | Yes | Text diff |
| `components/*.md` | Yes | Text diff |
| `screenshots/*.png` | Yes | Visual review in PR |
| `screenshots/.tmp/*.png` | No | N/A |
| `review-verdict.md` | Yes | Text diff |

### PR Review Protocol

1. The PR description must include:
   - feature name
   - workflow level: `L1` or `L2`
   - current stage: `V2-1` to `V2-4` when applicable
   - one paragraph describing the change
2. Any `.pen` change must include updated screenshots in `designs/<feature>/screenshots/`.
3. Reviewers evaluate `intent.md`, screenshots, `tokens/*`, `components/*.md`, and `review-verdict.md`. Do not rely on `.pen` files as review artifacts.

### Merge Conflicts

If two branches touch the same `.pen` file:

1. Do not resolve the binary conflict manually.
2. Open the newer file in Pencil.
3. Re-apply the older branch changes by hand.
4. Capture fresh screenshots that reflect the merged state.

---

## shadcn/ui Fallback Priority

When the mapping table in [design-to-code-workflow.md](../skills/pencil-design/references/design-to-code-workflow.md) does not cover a component, use this priority:

1. `shadcn/ui` official
2. `shadcn/ui` registry
3. `tremor`, `magicui`, `aceternity-ui`
4. Radix UI primitives
5. Handrolled component as the last resort

Do not jump straight to handrolled components.

---

## Token Pipeline

The full Style Dictionary pipeline runs during `V2-3`.

```text
pencil_get_variables
        -> flat key-value variables
scripts/tokens-convert.ts
        -> W3C DTCG JSON
designs/<feature>/tokens/w3c.json
        -> Style Dictionary build
  ├── tokens.css
  ├── tokens.ts
  └── tailwind-preset.ts
```

### Dependencies

```bash
npm install --save-dev style-dictionary style-dictionary-utils
```

---

## CI Validation for Design Artifacts

Design artifacts are validated in development CI, not at `V2-4`.

1. **Token consistency**

   ```bash
   npm run tokens:build
   git diff --exit-code designs/*/tokens/
   ```

2. **Component contract structure**
   - Every `designs/*/components/*.md` must contain:
     - `## Variants`
     - `## States`
     - `## Responsive`
     - `## Accessibility`
     - `## Implementation Mapping`
     - `## Design Constraints`
3. **No arbitrary Tailwind values**
   - CI should reject arbitrary visual values such as `bg-[#hex]`, `w-[375px]`, `rounded-[6px]`
4. **`.tmp/` not committed**
   - CI rejects any `designs/**/screenshots/.tmp/` file
5. **Intent doc present**
   - Any PR touching `designs/<feature>/` must include a non-empty `intent.md`

---

## Execution Layer

This workflow delegates Pencil MCP operations to the built-in `pencil-design` skill.

### pencil-design skill

- **Source:** [`.agents/skills/pencil-design/`](../skills/pencil-design/SKILL.md)
- **Covers:**
  - component reuse
  - token usage
  - overflow prevention
  - visual verification
  - token pipeline integration
  - design-to-code mapping for `V2-2` and `V2-3`

### design-reviewer agent

- **Trigger:** `V2-4`
- **Execution:** isolated artifact review against `designs/<feature>/`
- **Scope:** token coverage, contract completeness, structural consistency, accessibility documentation, responsive coverage

> The `design-review` skill remains available for plan-level review in development workflow Step 2. The `design-reviewer` agent is specific to design artifact review at `V2-4`.

---

## Integration with Development Workflow

This design workflow is optional. If no UI work is involved, the development workflow runs unchanged.

When design artifacts exist in `designs/<feature>/`, the development workflow should:

- **Step 1 (Research & Reuse):** read `intent.md`, inspect screenshots, and confirm the visual target
- **Step 2 (Plan First):** reference component contracts and review findings in the plan
- **Step 3 (TDD):** validate token usage and generate runtime quality artifacts such as visual regression and accessibility reports

For `L1` changes, use the lighter artifacts:

- updated screenshots for the affected area
- a short design note in `intent.md` or the PR

Steps 4-8 of the development workflow remain unchanged.
