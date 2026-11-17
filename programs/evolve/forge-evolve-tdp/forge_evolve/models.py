"""Pydantic v2 schema validation models for Canonical TDP Property Graph (CTDP-G v2.4) & URTS."""

from typing import Dict, List, Tuple
from pydantic import BaseModel, Field


class BRepFaceSchema(BaseModel):
    face_uid: str
    step_entity_id: str
    feature_name: str
    surface_type: str
    centroid_mm: Tuple[float, float, float]
    normal_unit: Tuple[float, float, float]
    area_mm2: float = Field(gt=0.0)
    abac_scope: str = Field(min_length=1)
    lod0_triangles: int = Field(gt=0)


class GDTCalloutSchema(BaseModel):
    callout_uid: str
    target_face_uid: str
    characteristic: str
    asme_symbol: str
    nominal_mm: float
    tolerance_mm: float = Field(gt=0.0)
    datum_system: List[str] = Field(min_length=1)
    source_modality: str
    ocr_confidence: float = Field(ge=0.0, le=1.0)
    ndi_modality: str
    standoff_mm: float = Field(gt=0.0)
    max_incidence_deg: float = Field(gt=0.0, le=45.0)


class IAComplianceVerdictSchema(BaseModel):
    passed: bool
    mil_std_31000b_score: float = Field(ge=0.0, le=100.0)
    rules_evaluated: int = Field(ge=6)
    rule_results: Dict[str, bool]
    min_extraction_confidence: float
    bound_feature_coverage_pct: float


class MerkleCommitSchema(BaseModel):
    commit_index: int
    commit_hash: str = Field(min_length=64, max_length=64)
    parent_commit_hash: str = Field(min_length=64, max_length=64)
    package_id: str
    lifecycle_state: str
    tail_number: str
    merkle_root: str = Field(min_length=64, max_length=64)
    author_spiffe_id: str
    hsm_signature_sha384: str
    leaf_count: int = Field(gt=0)
    timestamp_utc: str


class CanonicalTDPPayloadSchema(BaseModel):
    schema_version: str = "2.4.0"
    package_id: str
    ia_compliance_verdict: IAComplianceVerdictSchema
    merkle_commits: List[MerkleCommitSchema]
    faces: List[BRepFaceSchema]
    callouts: List[GDTCalloutSchema]
