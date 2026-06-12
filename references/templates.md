# Templates

## State Ledger Template

```json
{
  "objective": "Rewrite the review report into a formal submission package",
  "workspace_name": "agent_team",
  "created_at": "2026-06-03T09:00:00+00:00",
  "status": "in_progress",
  "approval": {
    "pending": [
      "Approve sending the final submission email"
    ],
    "granted": [],
    "denied": []
  },
  "packets": [
    {
      "id": "P1-source-audit",
      "title": "Audit source pack and citation gaps",
      "owner": "agent-source",
      "status": "review",
      "output": "handoffs/source-audit.md",
      "verification": [
        "cross-check official sources"
      ]
    }
  ],
  "verification": {
    "status": "in_progress",
    "checks": [
      {
        "name": "render final PDF",
        "status": "pending"
      }
    ]
  },
  "integration": {
    "status": "in_progress",
    "accepted": [],
    "rejected": [],
    "conflicts": []
  }
}
```

## Shared Context Fill-In

```markdown
# Shared Context

## Objective
One concrete sentence describing the outcome.

## Deliverables
- Final artifact path or expected output
- Supporting artifacts

## Known Facts
- Stable facts the whole team must use

## Constraints
- Scope, policy, budget, style, technical, or safety constraints

## Non-Goals
- Things agents must not spend time on

## Open Questions
- Missing facts and how to handle them

## Verification Standard
- Commands, render checks, review gates, or acceptance criteria
```

## Handoff Template

```markdown
# <Scope> Handoff

## Scope Handled

## Key Findings

## Recommended Changes

## Draft Text / Patch Notes

## Risks

## Unresolved Questions

## Sources / Evidence

## Files Changed
```

## Packet Template

```markdown
# Packet <NN>: <Scope>

## Packet ID
P1-<slug>

## Objective

## Context

## Owned Scope

## Excluded Scope

## Input Files / Sources

## Do

- TODO

## Do Not

- TODO

## Expected Output

## Verification

- TODO
```

## Reusable Recipe Template

Use this only when a completed run produced a pattern worth reusing.

```markdown
# Recipe: <Name>

## Trigger

When to use this recipe.

## Plan Shape

How the main thread should structure the run.

## Packet List

- P1-<scope>: <objective>
- P2-<scope>: <objective>

## Verification Checklist

- TODO

## Known Risks

- TODO

## Source Run

- Workspace: `agent_team/`
- Date: YYYY-MM-DD
```

## Task Board Statuses

Use these statuses consistently:

- `Todo`: planned and unstarted
- `Doing`: actively owned now
- `Blocked`: waiting on missing input or external result
- `Review`: produced and awaiting integration
- `Done`: integrated or explicitly accepted
- `Dropped`: deliberately not used

## Agent Scope Examples

Research report:

- Policy/source agent: official sources, legal basis, citation ledger
- Domain agent: business logic, stakeholder needs, field assumptions
- Technical agent: architecture, security, implementation realism
- Reviewer agent: expert objections, missing evidence, internal consistency

Codebase task:

- Explorer: map relevant modules and risks
- Worker A: own backend module
- Worker B: own UI module
- Verifier: run tests and inspect edge cases while workers continue

## Integration Notes

When two handoffs conflict, do not average them. Pick the version that is better supported by source evidence, project constraints, and final acceptance criteria. Record the decision in `03_source_index.md` or a review note when it affects future work.

For runs with multiple handoffs or review notes, run `scripts/collect_handoffs.py` to create an integration checklist before final synthesis. The script helps gather findings; it does not replace reading the handoffs.

## Approval Question Template

Use one clear question per risky bundle:

```text
Approve <exact risky action>?

Scope:
- <file/system/account set>

Likely effect:
- <what changes if approved>

Rollback:
- <how we recover if wrong>
```
