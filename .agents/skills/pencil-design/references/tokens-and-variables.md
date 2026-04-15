# Variables and Design Tokens

> Workflow step: **D3. Design Tokens**

Covers reading, creating, and mapping Pencil variables to the Style Dictionary token pipeline.

## Reading Variables

Always read tokens at the start of any design task:

```javascript
pencil_get_variables({ filePath: "path/to/file.pen" })
```

Returns flat key-value pairs:

```json
{
  "variables": {
    "primary": { "value": "#3b82f6" },
    "primary-foreground": { "value": "#ffffff" },
    "background": { "value": "#ffffff" },
    "foreground": { "value": "#0a0a0a" },
    "border": { "value": "#e2e8f0" },
    "radius-sm": { "value": 4 },
    "radius-md": { "value": 6 },
    "radius-lg": { "value": 8 }
  }
}
```

## Creating Variables

Define the visual foundation for the design:

```javascript
pencil_set_variables({
  filePath: "path/to/file.pen",
  variables: {
    "primary": { "value": "#3b82f6" },
    "primary-foreground": { "value": "#ffffff" },
    "secondary": { "value": "#64748b" },
    "accent": { "value": "#f59e0b" },
    "radius-md": { "value": 6 },
    "radius-lg": { "value": 8 }
  }
})
```

### Required Token Categories

| Category | Variables | Example Values |
|----------|-----------|----------------|
| Brand colors | `primary`, `secondary`, `accent` | `#3b82f6`, `#64748b`, `#f59e0b` |
| Semantic colors | `destructive`, `success`, `warning` | `#ef4444`, `#22c55e`, `#f59e0b` |
| Surface colors | `background`, `foreground`, `card`, `card-foreground` | `#ffffff`, `#0a0a0a` |
| UI colors | `border`, `ring`, `muted`, `muted-foreground` | `#e2e8f0`, `#94a3b8` |
| Border radius | `radius-sm`, `radius-md`, `radius-lg`, `radius-xl` | `4`, `6`, `8`, `12` |
| Typography | `font-sans`, `font-mono`, `font-heading` | `Inter, sans-serif` |
| Spacing | `spacing-xs`, `spacing-sm`, `spacing-md`, `spacing-lg` | `4`, `8`, `16`, `24` |

## Theme Support

Variables can have different values per theme (light/dark):

```json
{
  "primary": {
    "themes": {
      "light": "#3b82f6",
      "dark": "#60a5fa"
    }
  }
}
```

## Style Dictionary Token Pipeline

Pencil exports flat key-value pairs. The design-workflow.md token pipeline converts them:

```
pencil_get_variables
        | flat key-value (e.g., "primary": "#3b82f6")
scripts/tokens-convert.ts
        | Pencil flat -> W3C DTCG JSON
designs/<feature>/tokens/w3c.json
        |
Style Dictionary + style-dictionary-utils
        | build
  +-- tokens.css              (--color-primary: #3b82f6; ...)
  +-- tokens.ts               (typed constant references)
  +-- tailwind-preset.ts      (Tailwind v4 plugin with @theme declarations)
```

### W3C DTCG Intermediate Format

The conversion script produces W3C DTCG standard format:

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
| Hex color values (`#...`) | `color` | `"primary": "#3b82f6"` -> `$type: "color"` |
| Values with rem/px units | `dimension` | `"radius-md": "0.375rem"` -> `$type: "dimension"` |
| Font family values | `fontFamily` | `"font-sans": "Inter, sans-serif"` -> `$type: "fontFamily"` |
| Numeric-only values | `number` | `"font-weight-normal": "400"` -> `$type: "number"` |

## Tailwind v4 Mapping

Pencil variables map 1:1 to Tailwind v4 semantic utilities. Never use arbitrary values.

### Color Mapping

| Pencil Variable | `@theme` Declaration | Tailwind Utility |
|----------------|---------------------|------------------|
| `primary` | `--color-primary` | `bg-primary`, `text-primary`, `border-primary` |
| `primary-foreground` | `--color-primary-foreground` | `text-primary-foreground` |
| `background` | `--color-background` | `bg-background` |
| `foreground` | `--color-foreground` | `text-foreground` |
| `border` | `--color-border` | `border-border` |
| `muted` | `--color-muted` | `bg-muted` |
| `muted-foreground` | `--color-muted-foreground` | `text-muted-foreground` |
| `destructive` | `--color-destructive` | `bg-destructive`, `text-destructive` |

### Radius Mapping

| Pencil Variable | `@theme` Declaration | Tailwind Utility |
|----------------|---------------------|------------------|
| `radius-sm` | `--radius-sm: 0.25rem` | `rounded-sm` |
| `radius-md` | `--radius-md: 0.375rem` | `rounded-md` |
| `radius-lg` | `--radius-lg: 0.5rem` | `rounded-lg` |
| `radius-xl` | `--radius-xl: 0.75rem` | `rounded-xl` |

## What NEVER to Generate

| Bad (arbitrary values) | Good (semantic utilities) |
|----------------------|--------------------------|
| `bg-[#3b82f6]` | `bg-primary` |
| `text-[#ffffff]` | `text-primary-foreground` |
| `text-[var(--primary)]` | `text-primary` |
| `rounded-[6px]` | `rounded-md` |
| `rounded-[var(--radius-md)]` | `rounded-md` |
| `border-[#e2e8f0]` | `border-border` |

## Checklist

- [ ] Called `pencil_get_variables` to see available tokens?
- [ ] Using variable references instead of hardcoded values?
- [ ] If needed variable doesn't exist, created it with `pencil_set_variables`?
- [ ] For code generation: using semantic Tailwind classes, NOT arbitrary values?

## See Also

- [tailwind-shadcn-mapping.md](tailwind-shadcn-mapping.md) — Full mapping tables
- [design-to-code-workflow.md](design-to-code-workflow.md) — Code generation using tokens
