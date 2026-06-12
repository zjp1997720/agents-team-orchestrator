# Agents Team Orchestrator

Turn long, complex agent work into a coordinated project team with durable local state, scoped work packets, handoff files, risk gates, and final integration discipline.

[![skills.sh](https://skills.sh/b/zjp1997720/agents-team-orchestrator)](https://skills.sh/zjp1997720/agents-team-orchestrator)

## Install

```bash
npx skills add zjp1997720/agents-team-orchestrator
```

Install globally:

```bash
npx skills add zjp1997720/agents-team-orchestrator -g
```

Use without installing:

```bash
npx skills use zjp1997720/agents-team-orchestrator@agents-team-orchestrator
```

List available skills:

```bash
npx skills add zjp1997720/agents-team-orchestrator --list
```

## When To Use

Use this skill when a task benefits from a real coordination layer:

- independent research, coding, review, writing, QA, docs, or design tracks
- complex or risky work where a written success contract reduces drift
- multiple sub-agents or simulated work packets
- long-running work that must survive context compaction
- final deliverables that need explicit integration and verification

For small one-shot tasks, skip full orchestration and do the work directly.

## What It Creates

The workspace initializer creates an `agent_team/` directory:

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

`state.json` is the resumable machine-readable ledger. The Markdown files are the human coordination layer. Sub-agents write handoffs; the main thread owns final integration.

## Scripts

```bash
python3 scripts/init_team_workspace.py --root . --name agent_team --objective "Your objective"
python3 scripts/verify_team_workspace.py agent_team
python3 scripts/collect_handoffs.py agent_team --output agent_team/reviews/integration-checklist.md
```

## Skill Structure

- `SKILL.md` - main operating protocol
- `references/` - packet, schema, risk gate, template, and validation references
- `scripts/` - workspace initialization, verification, and handoff aggregation helpers
- `agents/` - optional agent metadata

## License

MIT
