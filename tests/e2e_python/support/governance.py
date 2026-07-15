# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Policy/tool-schema helpers and shared not-exercised handling."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent_os.policies import PolicyDocument, PolicyEvaluator

from .logging_config import logger, redact_for_log, redact_log_text, truncate_log_text
from .models import ModelReply, ScenarioResult


POLICY_DIR = Path(__file__).resolve().parent.parent / "policies"


def tool_schema(name: str, description: str, properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": list(properties),
            },
        },
    }


def load_policy_evaluator(name: str) -> PolicyEvaluator:
    """Load a customer-authored YAML policy and let the SDK parse it."""
    document = PolicyDocument.from_yaml(POLICY_DIR / f"{name}.yaml")
    return PolicyEvaluator(policies=[document])



def not_exercised_result(
    scenario_id: str,
    expected: str,
    reply: ModelReply,
    model_inputs: list[str],
) -> ScenarioResult:
    logger.warning(
        "Model response did not exercise scenario %s; expected %s; got %s",
        scenario_id,
        expected,
        _describe_reply(reply),
    )
    return ScenarioResult(
        "not_exercised",
        [],
        [],
        model_inputs,
        participation_status="not_exercised",
    )


def _describe_reply(reply: ModelReply) -> str:
    if reply.tool_call is not None:
        return (
            f"tool_call={reply.tool_call.name} "
            f"arguments={redact_for_log(reply.tool_call.arguments)}"
        )
    content = truncate_log_text(redact_log_text(reply.content.replace("\n", " ").strip()))
    return f"content={content!r}"
