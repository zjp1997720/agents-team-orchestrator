#!/usr/bin/env python3
"""Create a shared workspace for coordinated Codex sub-agent tasks."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path


def write_once(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an agent team workspace.")
    parser.add_argument("--root", default=".", help="Project root or output parent directory.")
    parser.add_argument("--name", default="agent_team", help="Workspace folder name.")
    parser.add_argument("--objective", default="", help="One-sentence task objective.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    workspace = root / args.name
    workspace.mkdir(parents=True, exist_ok=True)

    for folder in ("drafts", "handoffs", "packets", "recipes", "reviews", "sources"):
        (workspace / folder).mkdir(exist_ok=True)

    today = date.today().isoformat()
    objective = args.objective or "TODO: define the task objective."
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    state = {
        "objective": objective,
        "workspace_name": args.name,
        "created_at": created_at,
        "status": "planned",
        "approval": {
            "pending": [],
            "granted": [],
            "denied": [],
        },
        "packets": [
            {
                "id": "P0-main-setup",
                "title": "Define shared context and team split",
                "owner": "main-thread",
                "status": "in_progress",
                "output": "packets/00-main-setup.md",
                "verification": [],
            }
        ],
        "verification": {
            "status": "not_started",
            "checks": [],
        },
        "integration": {
            "status": "not_started",
            "accepted": [],
            "rejected": [],
            "conflicts": [],
        },
    }

    files = {
        "README.md": f"""# Agent Team Workspace

Created: {today}

Objective: {objective}

Use this folder as the durable coordination layer for a long Codex task. The main thread owns final integration. Agents write scoped handoffs. Keep `state.json` current enough that a resumed thread can continue without rereading old chat.
""",
        "00_shared_context.md": f"""# Shared Context

Updated: {today}

## Objective

{objective}

## Deliverables

- TODO

## Known Facts

- TODO

## Constraints

- TODO

## Non-Goals

- TODO

## Open Questions

- TODO

## Verification Standard

- TODO
""",
        "01_task_board.md": f"""# Task Board

Updated: {today}

## Doing

| ID | Task | Owner | Status | Output | Packet |
| --- | --- | --- | --- | --- | --- |
| T1 | Define shared context | Main thread | Doing | `00_shared_context.md` | `P0-main-setup` |

## Todo

| ID | Task | Owner | Status | Output | Packet |
| --- | --- | --- | --- | --- | --- |
| T2 | Review risk gates and assign agent scopes | Main thread | Todo | `04_agent_prompts.md` | `P1-risk-and-team-shape` |

## Done

| ID | Task | Owner | Status | Output | Packet |
| --- | --- | --- | --- | --- | --- |

## Blockers

| Item | Current Handling |
| --- | --- |
| TODO | TODO |

## Approval Status

| Risky Action | Status | Decision Owner | Notes |
| --- | --- | --- | --- |
| TODO | Pending | User | TODO |
""",
        "02_working_contract.md": """# Working Contract

## Main Thread

- Own final artifact, final claims, final verification, and user communication.
- Resolve conflicts between agent handoffs.
- Update this workspace when scope or facts change.
- Keep `state.json` and `01_task_board.md` aligned enough for task resumption.
- Ask one clear approval question before destructive, external, expensive, or ambiguous-risk actions.

## Agents

- Read shared context before work.
- Own only the assigned scope.
- Write handoff files instead of editing the final artifact unless explicitly assigned.
- Do not revert or overwrite others' work.
- Mark uncertainty and missing evidence.

## Packet Contract

Before work starts, every delegated scope needs a packet file under `packets/`.

Required fields:

1. Packet ID
2. Objective
3. Context
4. Owned scope
5. Excluded scope
6. Input files / sources
7. Do
8. Do not
9. Expected output
10. Verification

## Handoff Format

Use this shape:

1. Scope handled
2. Key findings
3. Recommended changes or draft text
4. Risks and unresolved questions
5. Files changed or output files
6. Sources or evidence
""",
        "03_source_index.md": """# Source Index

## Local Files

| Path | Purpose | Notes |
| --- | --- | --- |
| TODO | TODO | TODO |

## Web / External Sources

| URL | Purpose | Notes |
| --- | --- | --- |
| TODO | TODO | TODO |

## Decisions

| Decision | Rationale | Date |
| --- | --- | --- |
| TODO | TODO | TODO |
""",
        "04_agent_prompts.md": """# Agent Prompts

Copy and customize one prompt per agent.

## Template

You are Agent <role> for this project.

Read these files first:
- <shared context path>
- <working contract path>
- <source index path>

Objective:
- <objective>

Owned scope:
- <scope>

Excluded scope:
- <scope not owned>

Output:
- Write your handoff to `<handoffs/file.md>`.
- Follow a packet spec from `packets/<nn>-<scope>.md`.

Required contents:
- Findings
- Recommended text, patches, or decisions
- Risks and unresolved questions
- Evidence and source references

Rules:
- Do not edit the final artifact unless explicitly assigned.
- You are not alone in the workspace. Do not revert or overwrite others' changes.
- If facts conflict, report the conflict instead of guessing.
""",
        "packets/00-main-setup.md": f"""# Packet 00: Main Setup

## Packet ID
P0-main-setup

## Objective
Turn the request into a stable team workspace with shared context, risk gates, and initial scope split.

## Context
Objective: {objective}

## Owned Scope

- create or refine the shared context
- review risk gates
- define the first team split
- update `state.json` and `01_task_board.md`

## Excluded Scope

- final artifact production
- destructive edits outside the requested task

## Input Files / Sources

- `README.md`
- `00_shared_context.md`
- `01_task_board.md`
- `02_working_contract.md`
- `03_source_index.md`
- `state.json`

## Do

- fill missing objective details
- mark likely approval gates
- define the next packets before delegation

## Do Not

- spawn agents before shared context and ownership are clear
- hide risky actions inside broad prompts

## Expected Output

- updated shared context
- updated task board
- updated state ledger
- packet specs for delegated work

## Verification

- objective and deliverables are explicit
- at least one next packet is defined before delegation
- risky steps are visible in `state.json` or the task board
""",
    }

    for name, content in files.items():
        write_once(workspace / name, content, args.overwrite)

    state_path = workspace / "state.json"
    if not state_path.exists() or args.overwrite:
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
