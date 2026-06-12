# Risk Gates

Use this checklist before launching or continuing an Agents Team run.

## Ask For Approval

Ask one clear approval question before work that may:

- delete, overwrite, mass-rename, force-push, or rewrite history
- deploy, publish, email, post, create public resources, or mutate external systems
- run migrations, broad codemods, or dependency upgrades across many files
- touch credentials, secrets, billing, production data, user accounts, or private customer data
- spawn many agents, run expensive jobs, or consume unusual time or compute
- make changes outside the requested workspace or repository

Record pending or granted approvals in `state.json`.

## Usually Safe Without Extra Approval

Usually safe:

- reading local files in the requested workspace
- drafting plans, packet specs, prompts, reports, or review notes
- creating or updating local coordination artifacts such as `agent_team/`, `packets/`, `handoffs/`, or `state.json`
- running narrow tests, linters, typechecks, and dry runs
- spawning a small number of sub-agents when the user explicitly asked for delegation or Agents Team

## If Risk Is Ambiguous

Prefer a reversible next step:

1. do a read-only inspection
2. draft the exact command or action
3. explain the likely effect
4. ask for approval before execution

Do not bundle several unrelated risky actions into one vague approval ask.
