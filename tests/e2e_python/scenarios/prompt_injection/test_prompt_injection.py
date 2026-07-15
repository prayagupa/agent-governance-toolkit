# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Test: poisoned retrieved content is detected and the export is blocked."""

from __future__ import annotations

from pathlib import Path

from support import write_artifact

from .scenario import run_prompt_injection


def test_retrieved_prompt_injection_is_blocked(artifact_dir: Path) -> None:
    result = run_prompt_injection()

    assert result.decision == "deny"
    assert result.executed_tools == []
    assert result.audit_events[0].details["document_id"] == "poisoned-campaign-report"
    assert result.audit_events[0].details["threat_level"] in {"medium", "high", "critical"}

    write_artifact(result, artifact_dir, "prompt-injection")
