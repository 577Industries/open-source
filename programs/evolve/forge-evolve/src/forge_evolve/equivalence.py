"""Differential behavioral and numerical equivalence verification oracle."""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import Callable, List, Dict, Any

@dataclass(frozen=True)
class BoundaryComparisonCase:
    input_value: float
    legacy_output: float
    candidate_output: float
    abs_diff: float
    matched: bool

@dataclass(frozen=True)
class EquivalenceReport:
    corpus_name: str
    total_cases: int
    passed_cases: int
    max_abs_error: float
    chernoff_confidence_99: float
    cases: List[BoundaryComparisonCase]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class DifferentialOracle:
    def __init__(self, rel_tol: float = 1e-12, abs_tol: float = 1e-12):
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def compare_corpus(
        self,
        corpus_name: str,
        inputs: List[float],
        legacy_fn: Callable[[float], float],
        candidate_fn: Callable[[float], float],
    ) -> EquivalenceReport:
        cases: List[BoundaryComparisonCase] = []
        max_err = 0.0
        passed = 0
        for x in inputs:
            y_leg = legacy_fn(x)
            y_cand = candidate_fn(x)
            diff = abs(y_leg - y_cand)
            max_err = max(max_err, diff)
            ok = math.isclose(y_leg, y_cand, rel_tol=self.rel_tol, abs_tol=self.abs_tol)
            if ok:
                passed += 1
            cases.append(BoundaryComparisonCase(x, y_leg, y_cand, diff, ok))
        n = max(len(inputs), 1)
        conf = 1.0 - math.exp(-2.0 * n * (passed / n) ** 2) if passed == n else passed / n
        return EquivalenceReport(
            corpus_name=corpus_name,
            total_cases=len(inputs),
            passed_cases=passed,
            max_abs_error=max_err,
            chernoff_confidence_99=round(min(conf, 0.999999), 6),
            cases=cases,
        )
