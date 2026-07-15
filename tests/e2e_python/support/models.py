# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Shared dataclasses and the JSON artifact writer for E2E scenarios."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ModelReply:
    tool_call: ToolCall | None = None
    content: str = ""


@dataclass
class AuditEvent:
    scenario_id: str
    decision: str
    reason: str
    agent_id: str
    tool_name: str | None = None
    rule_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioResult:
    decision: str
    executed_tools: list[str]
    audit_events: list[AuditEvent]
    model_inputs: list[str] = field(default_factory=list)
    tool_arguments: list[dict[str, Any]] = field(default_factory=list)
    participation_status: str = "exercised"
    sandbox_violations: list[str] = field(default_factory=list)

    def artifact(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "executed_tools": self.executed_tools,
            "audit_events": [asdict(event) for event in self.audit_events],
            "model_inputs": self.model_inputs,
            "tool_arguments": self.tool_arguments,
            "participation_status": self.participation_status,
            "sandbox_violations": self.sandbox_violations,
        }


def write_artifact(result: ScenarioResult, artifact_dir: Path, scenario_id: str) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / f"{scenario_id}.json").write_text(
        json.dumps(result.artifact(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
