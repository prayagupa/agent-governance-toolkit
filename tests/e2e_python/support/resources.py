# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""In-memory resources that record attempted and executed tool calls."""

from __future__ import annotations

from typing import Any


class MockAdPlatform:
    def __init__(self) -> None:
        self.budget_changes: list[dict[str, Any]] = []

    def increase_daily_budget(self, **arguments: Any) -> None:
        self.budget_changes.append(arguments)


class MockPatientRecords:
    def __init__(self) -> None:
        self.note_updates: list[dict[str, Any]] = []

    def update_visit_notes(self, **arguments: Any) -> None:
        self.note_updates.append(arguments)


class MockIntakeProcessor:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def process_intake(self, **arguments: Any) -> None:
        self.calls.append(arguments)
