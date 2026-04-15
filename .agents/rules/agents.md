# Agent Orchestration

## Available Agents

Located in `~/.claude/agents/`:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| planner | Implementation planning | Complex features, refactoring |
| tdd-guide | Test-driven development | New features, bug fixes |
| code-reviewer | Code review | After writing code |
| security-reviewer | Security analysis | Before commits |
| refactor-cleaner | Dead code cleanup | Code maintenance |
| docs-lookup | Documentation lookup via Context7| API/docs questions |
| doc-updater | Documentation | Updating docs |
| python-reviewer | Python code review | Python projects |
| typescript-reviewer | TypeScript/React code review | TypeScript/Next.js projects |
| e2e-runner | Browser E2E testing | Critical user flow changes |
| design-reviewer | Design artifact review | Before design handoff (V2-4 final gate) |

## Immediate Agent Usage

No user prompt needed:
1. Complex feature requests - Use **planner** agent
2. Code just written/modified - Use **code-reviewer** agent
3. Bug fix or new feature - Use **tdd-guide** agent
4. Critical user flow changes - Use **e2e-runner** agent
5. Design artifacts ready for review - Use **design-reviewer** agent
6. Bug reported or unexpected behavior - Use **investigate** skill first
7. Vague product idea needs refinement - Use **ideate** skill (`/ideate`)

## Key Skills

Located in `.agents/skills/`:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| ideate | Product idea refinement | Vague idea → structured product definition |
| investigate | Root-cause analysis | Before any bug fix |
| design-review | Plan adversarial review | Before implementation, after planner |
| retro | Post-task retrospective | After feature/fix completion |

## Parallel Task Execution

ALWAYS use parallel Task execution for independent operations:

```markdown
# GOOD: Parallel execution
Launch 3 agents in parallel:
1. Agent 1: Security analysis of auth module
2. Agent 2: Performance review of cache system
3. Agent 3: Type checking of utilities

# BAD: Sequential when unnecessary
First agent 1, then agent 2, then agent 3
```

## Multi-Perspective Analysis

For complex problems, use split role sub-agents:
- Factual reviewer
- Senior engineer
- Security expert
- Consistency reviewer
- Redundancy checker
