# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""One governance scenario per module, exposed as run_* callables."""

from __future__ import annotations

from .adtech import run_adtech
from .filesystem_escape import run_filesystem_escape
from .healthcare import run_healthcare
from .pii_redaction import run_pii_redaction
from .prompt_injection import run_prompt_injection

__all__ = [
    "run_adtech",
    "run_filesystem_escape",
    "run_healthcare",
    "run_pii_redaction",
    "run_prompt_injection",
]
