# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Test: an out-of-scope live budget mutation is denied by policy."""

from __future__ import annotations

from pathlib import Path

from support import assert_exercised, write_artifact

from .scenario import run_adtech


def test_adtech_budget_mutation_is_denied(artifact_dir: Path) -> None:
    result, platform = run_adtech()
    assert_exercised(result)

    assert result.decision == "deny"
    assert result.executed_tools == []
    assert platform.budget_changes == []
    assert result.audit_events[0].rule_id == "adtech.deny-live-budget-mutation"

    write_artifact(result, artifact_dir, "adtech")
