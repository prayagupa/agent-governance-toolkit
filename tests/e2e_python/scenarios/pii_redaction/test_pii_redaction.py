# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Test: PII is redacted before the model, tool, and audit boundaries."""

from __future__ import annotations

import json
from pathlib import Path

from support import RAW_SECRETS, assert_exercised, assert_no_raw_secrets, write_artifact

from .scenario import run_pii_redaction


def test_pii_is_redacted_before_model_tool_and_audit_boundaries(artifact_dir: Path) -> None:
    result = run_pii_redaction()
    assert_exercised(result)

    assert result.decision == "allow"
    assert result.executed_tools == ["process_intake"]
    serialized = json.dumps(result.artifact())
    for secret in RAW_SECRETS:
        assert secret not in serialized
    assert "[REDACTED]" in serialized

    write_artifact(result, artifact_dir, "pii-redaction")
    assert_no_raw_secrets(artifact_dir / "pii-redaction.json")
