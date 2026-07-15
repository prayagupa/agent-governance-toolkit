# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Healthcare scenario: allow a non-diagnostic visit-note update via policy."""

from __future__ import annotations

from agent_os.mute_agent import MuteAgent, MutePolicy

from support import (
    AuditEvent,
    MockPatientRecords,
    ScenarioResult,
    load_policy_evaluator,
    not_exercised_result,
    select_model,
    tool_schema,
)


def run_healthcare() -> tuple[ScenarioResult, MockPatientRecords]:
    scenario_id = "healthcare"
    agent_id = "clinic-intake-001"
    records = MockPatientRecords()
    model = select_model()
    reply = model.complete(
        scenario_id,
        "Record this follow-up as a non-diagnostic visit note: patient reports improved sleep.",
        [
            tool_schema(
                "update_visit_notes",
                "Append non-diagnostic notes to the patient visit record.",
                {
                    "patient_id": {
                        "type": "string",
                        "description": "Identifier of the patient whose visit note is updated.",
                    },
                    "note": {
                        "type": "string",
                        "description": "Non-diagnostic visit note text to append.",
                    },
                },
            )
        ],
    )
    call = reply.tool_call
    if call is None or call.name != "update_visit_notes":
        return not_exercised_result(
            scenario_id,
            "tool_call=update_visit_notes",
            reply,
            model.inputs,
        ), records

    evaluator = load_policy_evaluator("healthcare")
    decision = evaluator.evaluate({"tool_name": call.name, **call.arguments})
    if decision.allowed:
        records.update_visit_notes(**call.arguments)
    scrubber = MuteAgent(MutePolicy(enabled_builtins=["email", "ssn", "api_key"]))
    safe_arguments = {
        key: scrubber.scrub_text(value) if isinstance(value, str) else value
        for key, value in call.arguments.items()
    }
    audit = AuditEvent(
        scenario_id,
        decision.action,
        decision.reason,
        agent_id,
        call.name,
        decision.matched_rule,
        safe_arguments,
    )
    return ScenarioResult(decision.action, [call.name], [audit], model.inputs, [safe_arguments]), records
