# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Test: a write outside the workspace is blocked by the sandbox."""

from __future__ import annotations

from pathlib import Path

from support import assert_exercised, write_artifact

from .scenario import run_filesystem_escape


def test_filesystem_escape_is_blocked(artifact_dir: Path, tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    forbidden_path = tmp_path / "outside" / "escaped.txt"
    result = run_filesystem_escape(workspace, forbidden_path)
    assert_exercised(result)

    assert result.decision == "deny"
    assert result.executed_tools == []
    assert not forbidden_path.exists()
    assert result.sandbox_violations or result.audit_events[0].decision == "deny"

    write_artifact(result, artifact_dir, "filesystem-escape")
