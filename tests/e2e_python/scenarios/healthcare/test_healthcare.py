# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Test: a permitted non-diagnostic visit-note update is allowed and audited."""

from __future__ import annotations

from pathlib import Path

from support import assert_exercised, assert_no_raw_secrets, write_artifact

from .scenario import run_healthcare


def test_healthcare_note_update_is_allowed(artifact_dir: Path) -> None:
    result, records = run_healthcare()
    assert_exercised(result)

    assert result.decision == "allow"
    assert result.executed_tools == ["update_visit_notes"]
    assert len(records.note_updates) == 1
    assert result.audit_events[0].rule_id == "healthcare.allow-visit-note-update"

    write_artifact(result, artifact_dir, "healthcare")
    assert_no_raw_secrets(artifact_dir / "healthcare.json")
