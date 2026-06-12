#!/usr/bin/env python3
"""Validate that an Agents Team workspace is complete enough to resume and audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "state.json",
    "00_shared_context.md",
    "01_task_board.md",
    "02_working_contract.md",
    "03_source_index.md",
    "04_agent_prompts.md",
)
REQUIRED_DIRS = ("drafts", "handoffs", "packets", "reviews", "sources")
REQUIRED_STATE_KEYS = (
    "objective",
    "workspace_name",
    "created_at",
    "status",
    "approval",
    "packets",
    "verification",
    "integration",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace_dir", help="Path to the agent_team workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace_dir)
    failures: list[str] = []
    warnings: list[str] = []

    if not workspace.is_dir():
        failures.append(f"Missing workspace directory: {workspace}")

    for name in REQUIRED_FILES:
        path = workspace / name
        if not path.is_file():
            failures.append(f"Missing file: {path}")
        elif not path.read_text(encoding="utf-8").strip():
            failures.append(f"Empty file: {path}")

    for name in REQUIRED_DIRS:
        path = workspace / name
        if not path.is_dir():
            failures.append(f"Missing directory: {path}")

    state_path = workspace / "state.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"Invalid JSON in {state_path}: {exc}")
        else:
            for key in REQUIRED_STATE_KEYS:
                if key not in state:
                    failures.append(f"Missing state key: {key}")
            if "packets" in state and not isinstance(state["packets"], list):
                failures.append("State key `packets` must be a list")
            if "approval" in state and not isinstance(state["approval"], dict):
                failures.append("State key `approval` must be an object")
            if "verification" in state and not isinstance(state["verification"], dict):
                failures.append("State key `verification` must be an object")
            if "integration" in state and not isinstance(state["integration"], dict):
                failures.append("State key `integration` must be an object")

    packet_files = sorted((workspace / "packets").glob("*.md")) if (workspace / "packets").is_dir() else []
    handoff_files = sorted((workspace / "handoffs").glob("*.md")) if (workspace / "handoffs").is_dir() else []
    if not packet_files:
        warnings.append("No packet files found under packets/")
    if not handoff_files:
        warnings.append("No handoff files found under handoffs/")

    if failures:
        print("Agents Team workspace verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Agents Team workspace verification passed: {workspace}")
    for warning in warnings:
        print(f"Warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
