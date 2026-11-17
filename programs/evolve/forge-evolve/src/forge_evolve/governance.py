"""Tamper-evident SHA-256 hashchain provenance ledger for modernization slices."""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass(frozen=True)
class ProvenanceStep:
    step_index: int
    stage: str
    payload_sha256: str
    prev_hash: str
    chain_hash: str

class ProvenanceHashchain:
    def __init__(self):
        self.steps: List[ProvenanceStep] = []

    def append(self, stage: str, payload: Dict[str, Any]) -> ProvenanceStep:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        payload_sha = hashlib.sha256(canonical).hexdigest()
        prev = self.steps[-1].chain_hash if self.steps else "0" * 64
        chain = hashlib.sha256(f"{prev}:{stage}:{payload_sha}".encode("utf-8")).hexdigest()
        step = ProvenanceStep(len(self.steps) + 1, stage, payload_sha, prev, chain)
        self.steps.append(step)
        return step

    def verify(self) -> bool:
        prev = "0" * 64
        for step in self.steps:
            expected = hashlib.sha256(f"{prev}:{step.stage}:{step.payload_sha256}".encode("utf-8")).hexdigest()
            if step.chain_hash != expected or step.prev_hash != prev:
                return False
            prev = step.chain_hash
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verified": self.verify(),
            "head_hash": self.steps[-1].chain_hash if self.steps else None,
            "steps": [asdict(s) for s in self.steps],
        }
