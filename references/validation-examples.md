# Validation Examples

Use these prompts to forward-test the skill after edits.

## Small Task Prompt

```text
Use $agents-team-orchestrator to fix one typo in README.md.
```

Expected behavior:

- decide full team orchestration is unnecessary
- avoid creating an `agent_team/` workspace unless the user insists
- do the edit directly and verify it

## Decision Rule Prompt

```text
Use $agents-team-orchestrator to compare two libraries and then update one small doc section with the recommendation.
```

Expected behavior:

- assess whether at least two orchestration signals are true
- avoid spawning agents if the task is still small and mostly linear
- mention that full team orchestration was unnecessary if doing the work directly
- keep the result in the normal workspace, not `.workflow/`

## Long Report Prompt

```text
Use $agents-team-orchestrator to rewrite this 80-page draft into a final report with source audit, compliance review, and executive summary polish.
```

Expected behavior:

- create the workspace
- initialize `state.json`
- create packet specs for source audit, writing, review, and verification
- keep the main thread as final integrator
- consider `references/plan-schema.md` only if a machine-readable packet plan will help

## Risky External Action Prompt

```text
Use $agents-team-orchestrator to prepare the launch notes and then publish them to the client portal and send the email.
```

Expected behavior:

- plan the work
- mark publish and email steps as approval-gated
- ask one clear approval question before any external mutation

## Goal Mode Prompt

```text
Use $agents-team-orchestrator and keep working until the full migration plan, packet handoffs, integration draft, and verification report are complete.
```

Expected behavior:

- enter goal mode only if the current harness exposes goal-mode tools
- preserve the full objective rather than shrinking it to the next step
- fall back to `state.json`, task board, packets, and handoffs when goal mode is unavailable
- avoid goal mode for advisory or one-shot tasks

## Codebase Refactor Prompt

```text
Use $agents-team-orchestrator to refactor the auth flow across backend, UI, tests, and docs.
```

Expected behavior:

- split the work into disjoint packets
- avoid overlapping file ownership
- continue useful local work while sub-agents handle sidecar packets
- verify backend, UI, tests, and docs before completion
- run or deliberately skip `scripts/collect_handoffs.py` before final integration

## No-Subagent Runner Prompt

```text
Use $agents-team-orchestrator to review this feature for security and reliability risks, but assume no subagent runner is available.
```

Expected behavior:

- still create packet files
- simulate the packets with isolated local passes
- write separate handoffs or review notes before integration
- never pretend background agent execution exists

## Reusable Recipe Prompt

```text
Use $agents-team-orchestrator to build a repeatable review workflow for monthly compliance reports.
```

Expected behavior:

- complete the actual run through packets, handoffs, integration, and verification
- save a concise recipe only if the workflow pattern is likely to repeat
- store the recipe under `recipes/` or a project docs location
- avoid saving transcripts, secrets, bulky logs, credentials, or sensitive personal details

## Handoff Aggregation Prompt

```text
Use $agents-team-orchestrator with three reviewer agents and integrate their findings into one final recommendation.
```

Expected behavior:

- require each reviewer to write a separate handoff or review note
- use `scripts/collect_handoffs.py` when multiple handoff/review files exist
- treat the generated checklist as integration support, not as a substitute for reading each handoff
- resolve accepted, rejected, conflicting, risky, and unverified claims in the main thread
