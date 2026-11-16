"""Placeholder for the HELIOS fusion-engine kill-gate. Nothing here runs an evaluation.

Per the pre-registration text (`osf_preregistration.template.md`, §4, §5 and §9),
the kill-gate is:

  1. Fused all-clear-revocation HSS on the 3-event hold-out beats the
     best-component-model HSS by >= 15%.
     Hold-out events (frozen):
       - 2022-01-20  Cycle 25 onset (M5.5)
       - 2023-02-17  Mid-cycle 25 (X2.2)
       - 2024-05-11  Gannon (G5)
  2. Reliability-diagram slope is within 0.15 of 1.0 across all three
     Kp severity strata (quiet / moderate / extreme).

Outcomes:
  - PASS both          -> full arXiv paper
  - PASS one, FAIL one -> ablation paper (honest negative result)
  - FAIL both          -> no paper; framework ships with a notebook
                          documenting the negative result

The OSF pre-registration MUST be timestamped before this script runs on
the hold-out events. Nothing enforces that yet: the text has not been filed,
and no code reads `orchestration/osf_preregistration.url`, the file the
template names for the registration's address.

Implementation deferred to the helios-fusion-engine build phase. This file
is a placeholder so consumers can `from orchestration.kill_gate import run`.
"""
from __future__ import annotations

from pathlib import Path

HOLDOUT_EVENTS = [
    "2022-01-20",  # Cycle 25 onset (M5.5)
    "2023-02-17",  # Mid-cycle 25 (X2.2)
    "2024-05-11",  # Gannon (G5)
]

SEVERITY_STRATA = ["quiet", "moderate", "extreme"]

HSS_RELATIVE_IMPROVEMENT_THRESHOLD = 0.15  # 15% relative improvement required
RELIABILITY_SLOPE_TOLERANCE = 0.15         # |slope - 1| <= 0.15 in every stratum


def run() -> dict[str, object]:
    """Would run the kill-gate evaluation and return a structured result.

    Not implemented. Raises, to make accidental early invocation loud.
    """
    raise NotImplementedError(
        "Kill-gate execution is not implemented. "
        "Filing OSF pre-registration must happen first; see "
        "orchestration/osf_preregistration.template.md."
    )


if __name__ == "__main__":
    result = run()
    print(result)
