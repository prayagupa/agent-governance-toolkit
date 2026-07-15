# Python Governance E2E Tests

These tests exercise five governance scenarios through production `agent_os`
policy, prompt-injection, redaction, and sandbox APIs. External systems are
represented by in-memory adtech, healthcare, and intake resources. Each
policy-driven scenario keeps its YAML policy next to it (e.g.
`scenarios/adtech.py` + `scenarios/adtech.yaml`), parsed by the SDK the way a
customer would ship it. Every scenario runs against a real local Ollama model.

## Setup

Install Ollama if `ollama` is not already on your `PATH`:

```bash
sudo snap install ollama
```

Start its server in one terminal:

```bash
ollama serve
```

In another terminal, pull the configured model:

```bash
ollama pull llama3.1
```

## Run

From the control-plane workspace root:

```bash
cd agent-governance-toolkit
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install \
  -e agent-governance-python/agent-os \
  pytest pytest-timeout
AGT_E2E_MODEL=llama3.1 \
AGT_E2E_MODEL_ATTEMPTS=3 \
.venv/bin/python -m pytest tests/e2e_python/test_top5.py -q
```

Model output is variable. For scenarios that need a specific action, the test
tries up to `AGT_E2E_MODEL_ATTEMPTS` times and fails with `not_exercised` when the
model never produces the required tool call or code. That failure logs the
expected action and a summary of the unexpected response. A governance bypass
always fails regardless of the participation result.

The prompt-injection scenario intentionally blocks poisoned retrieval content
before it reaches the model adapter. The PII scenario calls the model only after
redaction and verifies that raw values are absent from model input, tool
arguments, audit events, and artifacts.

## Logging

By default, the tests emit live INFO logs for each model request and response.
PII-like values are redacted before log records are written. Configure logging
from the pytest command line:

```bash
.venv/bin/python -m pytest tests/e2e_python/test_top5.py \
  --agt-e2e-log-model-io=summary \
  --agt-e2e-log-format=pretty \
  --agt-e2e-log-text-limit=1000 \
  --agt-e2e-log-live=on \
  --agt-e2e-log-level=INFO -q
```

Set `--agt-e2e-log-model-io=off` to suppress model request/response logs, or
`--agt-e2e-log-model-io=full` to disable truncation while keeping redaction. Set
`--agt-e2e-log-format=compact` for single-line JSON logs, or
`--agt-e2e-log-live=off` to keep the pytest output quiet.

## Artifacts

Set `AGT_E2E_ARTIFACT_DIR` to preserve JSON results:

```bash
AGT_E2E_ARTIFACT_DIR=artifacts/e2e-python/ollama \
.venv/bin/python -m pytest tests/e2e_python/test_top5.py -q
```
