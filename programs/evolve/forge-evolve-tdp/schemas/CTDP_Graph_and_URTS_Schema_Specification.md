# Canonical Technical Data Package Graph (CTDP-G) & Unified Robotic Task Specification (URTS)

> **Unimplemented design draft (2026-10-13). Nothing in this document is implemented or measured.** Identifiers, markings and numeric values in the examples below are synthetic placeholders.

**Document ID:** FORGE-EVOLVE-SPEC-2026-001  
**Version:** 2.4.0 (design draft, unimplemented)  
**Applicable Solicitations:** DAF27BZ01-DV008 (TDP Modernization & Zero Trust Exchange) & DAF27BZ01-DV012 (Autonomous TDP-to-Path Robotic Task Specification)  
**Referenced Standards (design intent, no compliance claimed):** MIL-STD-31000B, ISO 10303-242 (STEP AP242), ASME Y14.5-2018, ASME Y14.41, NIST SP 800-207 (Zero Trust Architecture), DoDI 8500.01, CMMC Level 2

---

## 1. Architectural Overview & First-Principles Data Model

The **Evolve Canonical Technical Data Package Graph (CTDP-G)** eliminates the historical divide between enterprise Product Lifecycle Management (PLM) repositories and shop-floor offline robotic programming (OLP) utilities. Rather than treating 3D CAD geometry, 2D PDF drawings, Bills of Materials (BOMs), Information Assurance (IA) markings, and robotic motion paths as disconnected files, CTDP-G models the entire physical-digital lifecycle as a **cryptographically verifiable, spatially indexed property graph**.

Every entity in the graph is governed by four design invariants:

1. **Topological Binding of Engineering Intent:** Every Geometric Dimensioning and Tolerancing (GD&T) feature control frame, fastener torque/flushness tolerance, surface finish requirement, and non-destructive inspection (NDI) callout extracted from 3D PMI or 2D drawings is bound via a directed edge (`HAS_TOLERANCE`, `REQUIRES_INSPECTION`, `REFERENCED_TO_DATUM`) to an explicit 3D Boundary Representation (B-Rep) topological face, edge, or vertex ID.
2. **Node-Level Zero Trust Envelope Encryption (NIST SP 800-207):** Each graph node and geometric sub-mesh is wrapped in an independent cryptographic envelope with its own Data Encryption Key (DEK) governed by Attribute-Based Access Control (ABAC) policies. An external supplier or shop-floor robotic controller only receives decryption keys for the specific topological faces and tolerance bounds required for its authorized workcell task.
3. **Immutable Merkle-DAG Configuration Lineage ("As-Sustained" State):** Every state transition across an asset's lifecycle—from *As-Designed* (`DESIGN_BASELINE`) to *As-Built* (`MANUFACTURING_QA`) to *As-Sustained* (`DEPOT_SUSTAINMENT`)—would be recorded as a content-addressable Merkle-DAG commit. Signing by hardware security modules (HSMs) and edge inspection sensors is a design goal and is not implemented.
4. **Hardware-Agnostic Kinematic & Trajectory Abstraction:** Robotic inspection tasks are derived directly from topological surface normals and sensor frustum constraints, serialized into the **Unified Robotic Task Specification (URTS)**, and post-processed deterministically into vendor-specific robot controller code (FANUC TP/LS, KUKA KRL, ABB RAPID, or SROS2 DDS `JointTrajectory` messages).

| Graph Domain | Primary Node Labels | Primary Edge Types | Governing Standard |
| :--- | :--- | :--- | :--- |
| **Enterprise & Security Envelope** | `TDPPackage`, `SecurityPolicy`, `ComplianceAudit`, `MerkleCommit` | `GOVERNED_BY`, `AUDITED_BY`, `PARENT_COMMIT`, `SIGNED_BY` | MIL-STD-31000B, NIST SP 800-207, FIPS 140-3 |
| **Topological & Spatial B-Rep** | `AssemblyNode`, `PartBody`, `BRepFace`, `BRepEdge`, `DatumSystem`, `BVHChunk` | `CONTAINS_PART`, `HAS_FACE`, `ADJACENT_TO`, `ESTABLISHES_DATUM`, `STREAMS_LOD` | ISO 10303-242 (STEP AP242), WebGPU glTF 2.0 |
| **Semantic Engineering Intent** | `GDTCallout`, `FastenerSpec`, `ProcessNote`, `SourceAnnotation2D` | `APPLIES_TO_FACE`, `EXTRACTED_FROM_DOC`, `CONSTRAINED_BY_DATUM` | ASME Y14.5-2018, ASME Y14.41 |
| **Autonomous Robotic Execution** | `InspectionTask`, `SensorFrustumPose`, `MobileBaseStation`, `JointTrajectorySegment` | `INSPECTS_FEATURE`, `REACHABLE_FROM_BASE`, `TRANSITIONS_TO`, `TRIGGERS_SENSOR` | ROS 2 / MoveIt 2, ISO 9283 |
| **Closed-Loop Sustainment & AI** | `NDIScanResult`, `AnomalyDetection`, `SustainmentDisposition` | `MEASURED_ON_FACE`, `DETECTED_DEFECT`, `MUTATES_STATE_TO` | AFMC Digital Thread, MIL-HDBK-1823A |

---

## 2. Property Graph & Relational Hybrid DDL (Neo4j Cypher & PostgreSQL/PostGIS)

### 2.1 Neo4j / Memgraph Property Graph Constraints & Schema

```cypher
// 1. Uniqueness & Node Key Constraints
CREATE CONSTRAINT tdp_pkg_id IF NOT EXISTS FOR (p:TDPPackage) REQUIRE p.package_id IS UNIQUE;
CREATE CONSTRAINT brep_face_uid IF NOT EXISTS FOR (f:BRepFace) REQUIRE f.face_uid IS UNIQUE;
CREATE CONSTRAINT gdt_callout_uid IF NOT EXISTS FOR (g:GDTCallout) REQUIRE g.callout_uid IS UNIQUE;
CREATE CONSTRAINT merkle_hash_unique IF NOT EXISTS FOR (m:MerkleCommit) REQUIRE m.commit_hash IS UNIQUE;
CREATE CONSTRAINT urts_task_uid IF NOT EXISTS FOR (t:InspectionTask) REQUIRE t.task_uid IS UNIQUE;

// 2. Canonical Graph Pattern (Cypher Instantiation Template)
MERGE (pkg:TDPPackage {
  package_id: "TDP-DAF-ACP-7740-REV-C",
  nsn: "SYNTHETIC-PART-001",
  platform_designator: "SYNTHETIC-PLATFORM / synthetic wing carry-through bulkhead",
  tdp_level: "Level 3 - Developmental & Production MBD",
  itar_category: "SYNTHETIC-EXPORT-CATEGORY",
  cui_marking: "SYNTHETIC-MARKING",
  merkle_root_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
})

MERGE (pol:SecurityPolicy {
  policy_id: "ABAC-POL-AFMC-DEPOT-09",
  min_clearance: "SECRET_OR_CUI_AUTHORIZED",
  allowed_citizenship: ["US"],
  allowed_roles: ["AFMC_SUSTAINMENT_ENG", "ALC_ROBOT_CELL_CONTROLLER", "QA_METROLOGIST"],
  encryption_algorithm: "AES-256-GCM (design, not implemented)",
  kms_key_uri: "https://example.invalid/kms/keys/synthetic-key-001"
})
MERGE (pkg)-[:GOVERNED_BY]->(pol)

MERGE (face:BRepFace {
  face_uid: "STEP-AP242-FACE-1042",
  step_entity_id: "#1042",
  surface_type: "BSPLINE_SURFACE_WITH_KNOTS",
  area_mm2: 14820.5,
  centroid_xyz_mm: [412.50, -185.20, 88.00],
  unit_normal_ijk: [0.0000, 0.1736, 0.9848],
  mean_curvature: 0.0012,
  bvh_octree_chunk_id: "LOD0-CHUNK-004",
  encrypted_mesh_blob_sha256: "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"
})
MERGE (pkg)-[:CONTAINS_FACE]->(face)

// Example metric values below are placeholders, not measured.
MERGE (gdt:GDTCallout {
  callout_uid: "GDT-7740-FCF-019",
  characteristic: "SURFACE_PROFILE",
  asme_symbol: "⏤",
  tolerance_zone_mm: 0.050,
  bilateral_equal: true,
  material_condition: "RFS",
  datum_precedence: ["A", "B", "C"],
  extraction_source: "HYBRID_AP242_AND_2D_DRAWING_OCR",
  ocr_confidence: 0.0,
  required_ndi_modality: "LASER_PROFILOMETRY_AND_EDDY_CURRENT",
  critical_safety_item: true
})
MERGE (gdt)-[:APPLIES_TO_FACE {binding_confidence: 0.0, projection_residual_mm: 0.0}]->(face);
```

### 2.2 PostgreSQL + PostGIS Spatial-Relational Backing Schema

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE lifecycle_state_enum AS ENUM ('AS_DESIGNED', 'AS_BUILT', 'AS_SUSTAINED', 'QUARANTINED');
CREATE TYPE gdt_characteristic_enum AS ENUM (
    'FLATNESS', 'STRAIGHTNESS', 'CIRCULARITY', 'CYLINDRICITY',
    'LINE_PROFILE', 'SURFACE_PROFILE', 'PERPENDICULARITY', 'PARALLELISM',
    'ANGULARITY', 'POSITION', 'CONCENTRICITY', 'SYMMETRY', 'CIRCULAR_RUNOUT', 'TOTAL_RUNOUT'
);

-- 1. Merkle-DAG Configuration Management Ledger (DV008)
CREATE TABLE tdp_merkle_commits (
    commit_hash CHAR(64) PRIMARY KEY,
    parent_commit_hash CHAR(64) REFERENCES tdp_merkle_commits(commit_hash),
    package_id VARCHAR(64) NOT NULL,
    tail_number VARCHAR(32) NOT NULL DEFAULT 'FLEET_BASELINE',
    lifecycle_state lifecycle_state_enum NOT NULL,
    author_spiffe_id VARCHAR(255) NOT NULL,
    hsm_signature BYTEA NOT NULL,
    ia_policy_verdict JSONB NOT NULL,
    committed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Spatial 3D B-Rep Topological Faces with Node-Level Encryption
CREATE TABLE ctdp_brep_faces (
    face_uid VARCHAR(64) PRIMARY KEY,
    package_id VARCHAR(64) NOT NULL,
    step_entity_ref VARCHAR(32) NOT NULL,
    surface_class VARCHAR(64) NOT NULL,
    area_mm2 DOUBLE PRECISION NOT NULL,
    centroid_3d GEOMETRY(PointZ, 0) NOT NULL,
    bounding_box_3d BOX3D NOT NULL,
    unit_normal DOUBLE PRECISION[3] NOT NULL,
    abac_policy_tag VARCHAR(64) NOT NULL,
    dek_wrapped_ciphertext BYTEA NOT NULL,
    bvh_lod0_uri TEXT NOT NULL,
    bvh_lod1_uri TEXT NOT NULL
);

CREATE INDEX idx_ctdp_faces_gist ON ctdp_brep_faces USING GIST (centroid_3d);

-- 3. Extracted Semantic GD&T & Process Specifications (DV012)
CREATE TABLE ctdp_gdt_callouts (
    callout_uid VARCHAR(64) PRIMARY KEY,
    face_uid VARCHAR(64) NOT NULL REFERENCES ctdp_brep_faces(face_uid),
    characteristic gdt_characteristic_enum NOT NULL,
    tolerance_value_mm DOUBLE PRECISION NOT NULL,
    plus_tolerance_mm DOUBLE PRECISION NOT NULL,
    minus_tolerance_mm DOUBLE PRECISION NOT NULL,
    datum_primary CHAR(2),
    datum_secondary CHAR(2),
    datum_tertiary CHAR(2),
    ndi_sensor_modality VARCHAR(64) NOT NULL,
    source_document_uri TEXT NOT NULL,
    extraction_method VARCHAR(32) NOT NULL,
    extraction_confidence DOUBLE PRECISION CHECK (extraction_confidence BETWEEN 0.0 AND 1.0)
);

-- 4. Closed-Loop Sustainment & AI Damage Detection Records (DV008 + DV012)
CREATE TABLE ctdp_sustainment_inspections (
    inspection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    commit_hash CHAR(64) NOT NULL REFERENCES tdp_merkle_commits(commit_hash),
    face_uid VARCHAR(64) NOT NULL REFERENCES ctdp_brep_faces(face_uid),
    callout_uid VARCHAR(64) NOT NULL REFERENCES ctdp_gdt_callouts(callout_uid),
    robot_cell_id VARCHAR(64) NOT NULL,
    measured_deviation_mm DOUBLE PRECISION NOT NULL,
    in_tolerance BOOLEAN NOT NULL,
    ai_defect_class VARCHAR(64) NOT NULL,
    ai_defect_probability DOUBLE PRECISION NOT NULL,
    point_cloud_s3_uri TEXT NOT NULL,
    disposition VARCHAR(32) NOT NULL CHECK (disposition IN ('ACCEPT', 'REWORK', 'MRB_REVIEW', 'SCRAP')),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 3. Canonical JSON Schema (Draft 2020-12) for CTDP-G & URTS Exchange

This JSON Schema defines the wire format for Zero-Trust TDP exchange packages (DV008) and Autonomous Robotic Task Specifications (DV012).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/schemas/v2.4/ctdp-urts-exchange.schema.json",
  "title": "Evolve Canonical TDP Graph & Unified Robotic Task Specification",
  "type": "object",
  "required": [
    "schema_version",
    "zero_trust_envelope",
    "merkle_lineage",
    "canonical_tdp_graph",
    "unified_robotic_task_spec",
    "sustainment_telemetry"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "2.4.0"
    },
    "zero_trust_envelope": {
      "type": "object",
      "required": [
        "package_id",
        "classification_marking",
        "export_control",
        "cmmc_level",
        "spiffe_sender_id",
        "abac_policy_rules",
        "fips_encryption_metadata",
        "opa_compliance_attestation"
      ],
      "properties": {
        "package_id": { "type": "string", "pattern": "^TDP-[A-Z0-9-]+$" },
        "classification_marking": { "type": "string", "enum": ["SYNTHETIC-MARKING-A", "SYNTHETIC-MARKING-B"] },
        "export_control": { "type": "string", "enum": ["SYNTHETIC-EXPORT-CATEGORY-A", "SYNTHETIC-EXPORT-CATEGORY-B"] },
        "cmmc_level": { "type": "integer", "minimum": 2, "maximum": 3 },
        "spiffe_sender_id": { "type": "string", "format": "uri" },
        "abac_policy_rules": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["rule_id", "allowed_roles", "allowed_enclaves", "accessible_node_scopes"],
            "properties": {
              "rule_id": { "type": "string" },
              "allowed_roles": { "type": "array", "items": { "type": "string" } },
              "allowed_enclaves": { "type": "array", "items": { "type": "string" } },
              "accessible_node_scopes": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "fips_encryption_metadata": {
          "type": "object",
          "required": ["cipher_suite", "key_derivation", "kms_master_key_id", "payload_hmac_sha384"],
          "properties": {
            "cipher_suite": { "type": "string", "const": "TLS_AES_256_GCM_SHA384" },
            "key_derivation": { "type": "string", "const": "HKDF-SHA384" },
            "kms_master_key_id": { "type": "string" },
            "payload_hmac_sha384": { "type": "string", "pattern": "^[a-f0-9]{96}$" }
          }
        },
        "opa_compliance_attestation": {
          "type": "object",
          "required": ["passed", "mil_std_31000b_score", "rules_evaluated", "timestamp_utc"],
          "properties": {
            "passed": { "type": "boolean" },
            "mil_std_31000b_score": { "type": "number", "minimum": 0, "maximum": 100 },
            "rules_evaluated": { "type": "integer" },
            "timestamp_utc": { "type": "string", "format": "date-time" }
          }
        }
      }
    },
    "merkle_lineage": {
      "type": "object",
      "required": ["current_commit_hash", "parent_commit_hash", "lifecycle_state", "tail_number", "merkle_root"],
      "properties": {
        "current_commit_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "parent_commit_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "lifecycle_state": { "type": "string", "enum": ["AS_DESIGNED", "AS_BUILT", "AS_SUSTAINED"] },
        "tail_number": { "type": "string" },
        "merkle_root": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
      }
    },
    "canonical_tdp_graph": {
      "type": "object",
      "required": ["part_metadata", "datum_reference_frames", "topological_faces", "gdt_semantic_bindings"],
      "properties": {
        "part_metadata": {
          "type": "object",
          "required": ["part_number", "revision", "material_spec", "bounding_box_mm"],
          "properties": {
            "part_number": { "type": "string" },
            "revision": { "type": "string" },
            "material_spec": { "type": "string" },
            "bounding_box_mm": {
              "type": "array",
              "items": { "type": "number" },
              "minItems": 6,
              "maxItems": 6
            }
          }
        },
        "datum_reference_frames": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["datum_label", "face_uid", "origin_xyz_mm", "rotation_matrix_3x3"],
            "properties": {
              "datum_label": { "type": "string" },
              "face_uid": { "type": "string" },
              "origin_xyz_mm": { "type": "array", "items": { "type": "number" }, "minItems": 3, "maxItems": 3 },
              "rotation_matrix_3x3": { "type": "array", "items": { "type": "number" }, "minItems": 9, "maxItems": 9 }
            }
          }
        },
        "topological_faces": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["face_uid", "step_id", "surface_type", "centroid_mm", "normal_unit", "area_mm2"],
            "properties": {
              "face_uid": { "type": "string" },
              "step_id": { "type": "string" },
              "surface_type": { "type": "string" },
              "centroid_mm": { "type": "array", "items": { "type": "number" }, "minItems": 3, "maxItems": 3 },
              "normal_unit": { "type": "array", "items": { "type": "number" }, "minItems": 3, "maxItems": 3 },
              "area_mm2": { "type": "number" }
            }
          }
        },
        "gdt_semantic_bindings": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "callout_uid",
              "target_face_uid",
              "gdt_type",
              "nominal_mm",
              "tolerance_band_mm",
              "datum_system",
              "source_modality",
              "sensor_requirement"
            ],
            "properties": {
              "callout_uid": { "type": "string" },
              "target_face_uid": { "type": "string" },
              "gdt_type": { "type": "string" },
              "nominal_mm": { "type": "number" },
              "tolerance_band_mm": { "type": "number" },
              "datum_system": { "type": "array", "items": { "type": "string" } },
              "source_modality": { "type": "string", "enum": ["STEP_AP242_PMI", "PDF_2D_OCR_VECTOR", "SPEC_DOC_NLP"] },
              "sensor_requirement": {
                "type": "object",
                "required": ["sensor_type", "standoff_distance_mm", "max_incidence_angle_deg", "point_density_pts_per_mm2"],
                "properties": {
                  "sensor_type": { "type": "string" },
                  "standoff_distance_mm": { "type": "number" },
                  "max_incidence_angle_deg": { "type": "number" },
                  "point_density_pts_per_mm2": { "type": "number" }
                }
              }
            }
          }
        }
      }
    },
    "unified_robotic_task_spec": {
      "type": "object",
      "required": ["urts_id", "kinematic_profile", "mobile_base_stations", "inspection_waypoints", "collision_verification"],
      "properties": {
        "urts_id": { "type": "string" },
        "kinematic_profile": {
          "type": "object",
          "required": ["platform_class", "mobile_base_dof", "manipulator_dof", "dh_parameters_hash"],
          "properties": {
            "platform_class": { "type": "string" },
            "mobile_base_dof": { "type": "integer" },
            "manipulator_dof": { "type": "integer" },
            "dh_parameters_hash": { "type": "string" }
          }
        },
        "mobile_base_stations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["station_id", "base_pose_xy_yaw", "assigned_waypoint_ids", "mean_manipulability_index"],
            "properties": {
              "station_id": { "type": "string" },
              "base_pose_xy_yaw": { "type": "array", "items": { "type": "number" }, "minItems": 3, "maxItems": 3 },
              "assigned_waypoint_ids": { "type": "array", "items": { "type": "string" } },
              "mean_manipulability_index": { "type": "number" }
            }
          }
        },
        "inspection_waypoints": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "waypoint_id",
              "callout_uid",
              "station_id",
              "tcp_position_xyz_mm",
              "tcp_orientation_quat_wxyz",
              "joint_angles_rad",
              "min_obstacle_clearance_mm",
              "sensor_trigger_cmd"
            ],
            "properties": {
              "waypoint_id": { "type": "string" },
              "callout_uid": { "type": "string" },
              "station_id": { "type": "string" },
              "tcp_position_xyz_mm": { "type": "array", "items": { "type": "number" }, "minItems": 3, "maxItems": 3 },
              "tcp_orientation_quat_wxyz": { "type": "array", "items": { "type": "number" }, "minItems": 4, "maxItems": 4 },
              "joint_angles_rad": { "type": "array", "items": { "type": "number" }, "minItems": 6, "maxItems": 7 },
              "min_obstacle_clearance_mm": { "type": "number" },
              "sensor_trigger_cmd": { "type": "string" }
            }
          }
        },
        "collision_verification": {
          "type": "object",
          "required": ["sdf_voxel_resolution_mm", "continuous_collision_free", "minimum_clearance_mm", "simulated_cycle_time_sec"],
          "properties": {
            "sdf_voxel_resolution_mm": { "type": "number" },
            "continuous_collision_free": { "type": "boolean" },
            "minimum_clearance_mm": { "type": "number" },
            "simulated_cycle_time_sec": { "type": "number" }
          }
        }
      }
    },
    "sustainment_telemetry": {
      "type": "object",
      "required": ["scan_campaign_id", "anomalies_detected", "overall_airframe_health_index"],
      "properties": {
        "scan_campaign_id": { "type": "string" },
        "overall_airframe_health_index": { "type": "number" },
        "anomalies_detected": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["anomaly_id", "face_uid", "defect_type", "measured_error_mm", "severity", "recommended_disposition"],
            "properties": {
              "anomaly_id": { "type": "string" },
              "face_uid": { "type": "string" },
              "defect_type": { "type": "string" },
              "measured_error_mm": { "type": "number" },
              "severity": { "type": "string" },
              "recommended_disposition": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

---

## 4. High-Performance gRPC / Protocol Buffers v3 Wire Definition (`ctdp_urts.proto`)

For sub-second WebGPU streaming of massive Model-Based Definition (MBD) assemblies (DV008) and real-time SROS2 robotic telemetry streaming (DV012), the Evolve design specifies the binary gRPC streams defined below (not implemented):

```protobuf
syntax = "proto3";
package forge_evolve.v2;

option go_package = "577industries.com/forge_evolve/api/v2;evolv2";

// 1. Sub-Second Progressive MBD Mesh & PMI Streaming Service (DV008)
service ZeroTrustMBDStreamService {
  rpc StreamProgressiveBVH (BVHStreamRequest) returns (stream EncryptedBVHChunk);
  rpc CommitAsSustainedState (SustainmentCommitRequest) returns (MerkleCommitReceipt);
}

// 2. Autonomous Robotic Pathing & Multi-Vendor Execution Service (DV012)
service AutonomousRoboticPathService {
  rpc CompileTDPToURTS (TDPCompileRequest) returns (URTSTaskPackage);
  rpc ExportVendorControllerCode (VendorExportRequest) returns (VendorControllerProgram);
}

message Vec3 {
  double x = 1;
  double y = 2;
  double z = 3;
}

message Quat {
  double w = 1;
  double x = 2;
  double y = 3;
  double z = 4;
}

message BVHStreamRequest {
  string package_id = 1;
  string spiffe_jwt_token = 2;
  repeated string requested_abac_scopes = 3;
  Vec3 camera_frustum_origin = 4;
  double max_screen_space_error = 5;
}

message EncryptedBVHChunk {
  string chunk_id = 1;
  uint32 lod_level = 2;
  bytes aes_gcm_iv = 3;
  bytes encrypted_draco_mesh_payload = 4;
  bytes encrypted_pmi_annotations = 5;
  bytes gcm_auth_tag = 6;
  string merkle_inclusion_proof = 7;
}

message WaypointPose {
  string waypoint_id = 1;
  string bound_gdt_callout_uid = 2;
  string mobile_station_id = 3;
  Vec3 tcp_xyz_mm = 4;
  Quat tcp_quat_wxyz = 5;
  repeated double joint_positions_rad = 6;
  repeated double joint_velocities_rad_s = 7;
  double min_sdf_clearance_mm = 8;
  string sensor_trigger_payload = 9;
}

message URTSTaskPackage {
  string urts_id = 1;
  string source_merkle_commit = 2;
  repeated WaypointPose ordered_trajectory = 3;
  double total_execution_time_sec = 4;
  bool collision_free_verified = 5;
}

message VendorExportRequest {
  string urts_id = 1;
  enum ControllerDialect {
    ROS2_MOVEIT_JSON = 0;
    FANUC_LS_TP = 1;
    KUKA_KRL_SRC = 2;
    ABB_RAPID_MOD = 3;
  }
  ControllerDialect target_dialect = 2;
}

message VendorControllerProgram {
  string filename = 1;
  string controller_dialect = 2;
  string program_source_code = 3;
  string sha256_checksum = 4;
}

message SustainmentCommitRequest {
  string package_id = 1;
  string parent_commit_hash = 2;
  string tail_number = 3;
  string robot_cell_spiffe_id = 4;
  bytes signed_point_cloud_digest = 5;
  repeated AnomalyRecord detected_anomalies = 6;
}

message AnomalyRecord {
  string face_uid = 1;
  string callout_uid = 2;
  string defect_classification = 3;
  double dimensional_deviation_mm = 4;
  double ai_confidence = 5;
  string disposition = 6;
}

message MerkleCommitReceipt {
  string new_commit_hash = 1;
  string merkle_root_hash = 2;
  string timestamp_utc = 3;
  bool plm_sync_dispatched = 4;
}
```

---

## 5. Open Policy Agent (OPA) Rego Policy for Automated IA Compliance Validation (DV008)

In the Evolve design, every Technical Data Package ingested or exchanged would be validated against this policy-as-code gate before any geometry or trajectory is rendered or transmitted. Target: `<50 ms` (not measured; the policy has not been evaluated by OPA):

```rego
package forge_evolve.zerotrust.ia_compliance

import future.keywords.in

default allow_tdp_exchange := false
default mil_std_31000b_compliant := false

# 1. Verify MIL-STD-31000B Structural & Semantic Completeness
mil_std_31000b_compliant {
    input.canonical_tdp_graph.part_metadata.part_number != ""
    count(input.canonical_tdp_graph.datum_reference_frames) >= 1
    count(input.canonical_tdp_graph.topological_faces) > 0
    count(input.canonical_tdp_graph.gdt_semantic_bindings) > 0
    every binding in input.canonical_tdp_graph.gdt_semantic_bindings {
        binding.tolerance_band_mm > 0.0
        binding.target_face_uid != ""
    }
}

# 2. Enforce ITAR (22 CFR 120-130) & DoDI 8500.01 Zero Trust ABAC Rules
itar_access_authorized {
    input.subject.us_person_verified == true
    input.subject.cmmc_enclave_level >= input.zero_trust_envelope.cmmc_level
    input.subject.role in {"AFMC_SUSTAINMENT_ENG", "ALC_ROBOT_CELL_CONTROLLER", "QA_METROLOGIST"}
    input.subject.mtls_spiffe_verified == true
}

# 3. Verify Cryptographic Merkle Integrity & FIPS 140-3 Cipher Suite
crypto_integrity_verified {
    input.zero_trust_envelope.fips_encryption_metadata.cipher_suite == "TLS_AES_256_GCM_SHA384"
    input.merkle_lineage.current_commit_hash != ""
    input.merkle_lineage.signature_valid == true
}

# 4. Final Composite Gate Decision
allow_tdp_exchange {
    mil_std_31000b_compliant
    itar_access_authorized
    crypto_integrity_verified
}
```
