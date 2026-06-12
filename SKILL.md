---
name: agents-team-orchestrator
description: Orchestrate long, complex Codex tasks with coordinated sub-agents, shared local context, a machine-readable state ledger, task boards, packet specs, approval gates, handoff files, and final integration discipline. Use when the user explicitly asks for Agents Team, sub-agents, delegation, parallel agent work, expert simulation, or when a long-running task needs durable coordination across research, writing, coding, review, or document production.
metadata:
  version: "1.0.0"
  license: "MIT"
---

# Agents Team Orchestrator

## Overview

Use this skill to turn a long task into a small project team. The main Codex thread remains the integrator; sub-agents produce scoped handoffs through files, while the workspace keeps both human-readable context and machine-readable state.

## Decision Rule

Use full Agents Team orchestration when the user explicitly asks for Agents Team, sub-agents, delegation, parallel agent work, expert simulation, or when at least two of these signals are true:

- the task has independent research, writing, coding, review, migration, QA, docs, or design tracks
- the task is broad enough that a written success contract would reduce drift
- the task has meaningful risk: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, compliance, or large cross-file changes
- implementation and verification benefit from separate passes
- the workflow may become a reusable recipe for future work

If the task is small, do it directly and mention that full team orchestration was unnecessary. Creating `agent_team/` is useful only when the shared workspace will reduce coordination or recovery cost.

## Hard Rules

- Spawn sub-agents only when the user explicitly asks for Agents Team, sub-agents, delegation, parallel agent work, or expert simulation.
- Keep one main thread as final owner. Sub-agents do not own the final answer or final artifact unless the user explicitly requests that structure.
- Create shared local state before delegation. Do not rely on chat history as the only coordination layer.
- Keep `state.json` current enough that a paused task can resume without reconstructing the plan from chat history.
- Give each agent a disjoint scope, clear inputs, a single output path, and a definition of done.
- Define packet ownership before delegation. Each packet must say what to do, what not to do, expected output, and verification.
- Ask one clear approval question before destructive, external, expensive, or ambiguous-risk actions. Do not bury multiple risky actions in one ask.
- Tell agents they are not alone in the workspace and must not revert or overwrite others' work.
- Prefer handoff files over conversational summaries for anything that must survive context compaction.
- Close or stop using agents once their handoffs are integrated.
- Do not introduce `.workflow/` or another parallel coordination surface for this skill. Translate useful workflow ideas into the `agent_team/` structure.

## Workflow

1. Define the objective, deliverables, constraints, non-goals, and verification standard.
2. Create a shared workspace with `scripts/init_team_workspace.py`.
3. Fill `00_shared_context.md`, `01_task_board.md`, `02_working_contract.md`, `03_source_index.md`, and the initial `state.json` before spawning.
4. Review `references/risk-gates.md`. Mark which steps need approval and capture them in `state.json`.
5. Design the team: usually 2-5 agents, each covering an independent domain.
6. Write packet specs under `packets/` with clear ownership, exclusions, outputs, and verification. Use `references/plan-schema.md` only when a machine-readable packet plan adds value; `state.json` remains the status ledger.
7. Spawn agents with narrow prompts. Require output to `handoffs/<scope>.md` or a clearly owned file set.
8. Continue useful local work while agents run. Avoid duplicating their scopes.
9. Integrate handoffs into the final artifact. Use `scripts/collect_handoffs.py` when there are multiple handoff or review files. Resolve conflicts in the main thread and update `state.json`.
10. Run the verification checklist and `scripts/verify_team_workspace.py`. Record risks, unresolved inputs, and final file paths.
11. Update the task board and preserve a concise project log. If the run produced a reusable pattern, save a recipe under `recipes/` or another project-appropriate docs location.

## Goal Mode

If goal-mode tools are available and the user explicitly requests sustained execution, or the task clearly requires multi-turn completion, start goal mode with the full objective. Do not shrink the goal to the next step.

Do not enter goal mode for a small one-shot task, a purely advisory discussion, or when the user asks only for a plan. If goal-mode tools are unavailable, keep the objective durable through `state.json`, the task board, packet files, and handoffs.

## Workspace Setup

Run the initializer from the target project root:

```bash
python3 <path-to-this-skill>/scripts/init_team_workspace.py \
  --root . \
  --name agent_team \
  --objective "Rewrite the review report into a formal submission package"
```

When installed through `npx skills`, resolve `<path-to-this-skill>` to this skill's installed directory. Agents should resolve `scripts/` and `references/` relative to this `SKILL.md`.

It creates:

```text
agent_team/
├── README.md
├── state.json
├── 00_shared_context.md
├── 01_task_board.md
├── 02_working_contract.md
├── 03_source_index.md
├── 04_agent_prompts.md
├── drafts/
├── handoffs/
├── packets/
├── recipes/
├── reviews/
└── sources/
```

## Machine-Readable State

`state.json` is the compact status ledger for long tasks. Keep it lightweight and current. It exists so a resumed Codex thread can answer these questions immediately:

- what is the exact objective
- what approvals are pending or granted
- which packets are `pending`, `in_progress`, `review`, `blocked`, or `complete`
- what verification remains
- whether integration is still open

Minimum keys:

- `objective`
- `workspace_name`
- `created_at`
- `status`
- `approval`
- `packets`
- `verification`
- `integration`

Read `references/templates.md` for the recommended shape.

## Risk Gates

Before any destructive, external, or expensive step, review `references/risk-gates.md`.

Use one approval question per risky bundle. Good examples:

- "Approve renaming these 42 files and updating imports afterward?"
- "Approve sending these two emails from your account?"
- "Approve running this migration against the staging database?"

If approval is not available, continue only with safe planning, inspection, draft outputs, or dry runs.

## Work Packet Contract

Each packet should live in `packets/<nn>-<scope>.md` and include:

- `Packet ID`
- `Objective`
- `Context`
- `Owned scope`
- `Excluded scope`
- `Input files / sources`
- `Do`
- `Do not`
- `Expected output`
- `Verification`

Use the packet template in `references/templates.md`. Keep packet scopes disjoint. If two packets need the same file, the split is wrong.

## Agent Prompt Contract

Each delegated prompt should include:

- Role and decision boundary
- Shared context paths to read first
- Owned scope and excluded scope
- Exact output path
- Required evidence or source attribution
- Safety constraints and sensitive terms to avoid
- Definition of done
- Reminder not to revert or overwrite other work

Minimal shape:

```text
You are Agent <role> for <project>.
Read <shared context paths> first.
Own only <scope>. Do not edit the final artifact.
Write your handoff to <path>.
Include: findings, recommended text/patches, risks, unresolved questions, source references.
You are not alone in the workspace. Do not revert or overwrite others' changes.
```

## Team Patterns

- Research package: policy/source agent, domain expert agent, critic/reviewer agent.
- Long report: source extraction agent, technical chapter agent, risk/compliance agent, budget/data agent.
- Codebase refactor: explorer agent, worker per module, verification agent.
- Expert simulation: several reviewer agents with distinct lenses; main thread synthesizes questions and fixes.

Read `references/templates.md` when you need fuller templates for task boards, shared context, handoffs, or agent prompts.

## Reusable Recipes

Create a reusable recipe only when a run produces a pattern that should compound into future work. Good candidates include repeatable report pipelines, recurring review structures, migration playbooks, or successful multi-agent packet shapes.

Keep recipes concise:

- trigger: when to use the recipe
- plan shape: the coordination pattern
- packet list: reusable packet scopes
- verification checklist: evidence needed before delivery
- known risks: failure modes to watch

Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details. Store the recipe under `recipes/<name>.md` in the team workspace when it belongs to the run, or in a project docs folder when it should outlive the run.

## Forward Testing

When improving this skill, test its trigger discipline before calling it "better". Read `references/validation-examples.md`.

The key checks:

- a small task should bypass full team orchestration
- a risky task should force an approval gate
- a long task should create the workspace, packets, and state ledger
- a no-subagent environment should still produce packet files and handoffs without pretending automation exists

## Integration Checklist

Before final delivery:

- All handoffs are read and integrated or explicitly rejected.
- `scripts/collect_handoffs.py` has been run or deliberately skipped because there was only one simple handoff.
- `state.json` matches the real state of packets, approvals, and verification.
- The task board matches the real state.
- No agent-owned claim remains uncited when the deliverable needs evidence.
- Conflicting recommendations are resolved in the main thread.
- Generated documents, code, or data files are verified with the relevant renderer/test command.
- Final response names the deliverables, verification performed, and remaining fill-in items.
