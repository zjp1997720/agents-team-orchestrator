# Optional Plan Schema

Use this schema only when a machine-readable packet plan helps coordination. Keep `00_shared_context.md` as the human source of truth and `state.json` as the status ledger.

```json
{
  "goal": "string",
  "success_criteria": ["string"],
  "constraints": ["string"],
  "risks": [
    {
      "risk": "string",
      "approval_required": true,
      "mitigation": "string"
    }
  ],
  "max_concurrent_agents": 4,
  "max_total_agents": 12,
  "packets": [
    {
      "id": "P1-source-audit",
      "objective": "string",
      "context": "string",
      "files_or_sources": ["string"],
      "owned_scope": "string",
      "excluded_scope": "string",
      "do": ["string"],
      "do_not": ["string"],
      "expected_output": "handoffs/source-audit.md",
      "verification": ["string"],
      "status": "pending"
    }
  ],
  "integration_policy": {
    "owner": "main-thread",
    "conflict_resolution": "Inspect authoritative sources before choosing.",
    "final_output": "string"
  },
  "verification": [
    {
      "check": "string",
      "command": "string or null",
      "required": true,
      "status": "pending"
    }
  ],
  "reusable_artifacts": ["recipes/example.md"]
}
```

Suggested defaults:

- `max_concurrent_agents`: 2-4 for normal work.
- `max_total_agents`: 6-12 unless the user approves a larger run.
- Packet IDs: prefix with `P<N>-` so they match packet files and `state.json`.
- Status values: `pending`, `in_progress`, `review`, `blocked`, `complete`, `dropped`.

Do not let this schema create a second planning system. If a field conflicts with the actual run state, update `state.json`, the task board, and packet files first.
