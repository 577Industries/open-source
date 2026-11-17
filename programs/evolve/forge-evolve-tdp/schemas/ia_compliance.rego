package forge_evolve.zerotrust.ia_compliance

import future.keywords.in

default allow_tdp_exchange := false
default mil_std_31000b_compliant := false

# Gate 1: MIL_STD_31000B_TOPOLOGY_WATERTIGHT
topology_watertight {
    count(input.canonical_tdp_graph.topological_faces) > 0
    every face in input.canonical_tdp_graph.topological_faces {
        face.area_mm2 > 0.0
        count(face.normal_unit) == 3
    }
}

# Gate 2: ASME_Y14_5_DATUM_COMPLETENESS
asme_y14_5_datum_complete {
    count(input.canonical_tdp_graph.gdt_semantic_bindings) > 0
    every binding in input.canonical_tdp_graph.gdt_semantic_bindings {
        binding.tolerance_band_mm > 0.0
        count(binding.datum_system) >= 1
        binding.target_face_uid != ""
    }
}

# Gate 3: SEMANTIC_BINDING_CONFIDENCE_FLOOR_95PCT
semantic_binding_confidence_ok {
    every binding in input.canonical_tdp_graph.gdt_semantic_bindings {
        binding.ocr_confidence >= 0.95
    }
}

# Gate 4: EXPORT_CONTROL_ABAC_TAGGED
itar_abac_tagged {
    every face in input.canonical_tdp_graph.topological_faces {
        face.abac_scope != ""
    }
    input.subject.us_person_verified == true
    input.subject.cmmc_enclave_level >= input.zero_trust_envelope.cmmc_level
    input.subject.role in {"AFMC_SUSTAINMENT_ENG", "ALC_ROBOT_CELL_CONTROLLER", "QA_METROLOGIST"}
}

# Gate 5: FIPS_140_3_AES_256_GCM_ENVELOPE (with FIPS 203 ML-KEM-768 PQC Hybrid)
fips_crypto_envelope_ok {
    input.zero_trust_envelope.fips_encryption_metadata.cipher_suite == "TLS_AES_256_GCM_SHA384"
    input.zero_trust_envelope.fips_encryption_metadata.pqc_kem == "FIPS_203_ML_KEM_768"
    input.merkle_lineage.current_commit_hash != ""
}

# Gate 6: NIST_800_207_SPIFFE_MTLS_IDENTITY
spiffe_mtls_verified {
    input.subject.mtls_spiffe_verified == true
    startswith(input.zero_trust_envelope.spiffe_sender_id, "spiffe://")
}

mil_std_31000b_compliant {
    topology_watertight
    asme_y14_5_datum_complete
    semantic_binding_confidence_ok
}

allow_tdp_exchange {
    mil_std_31000b_compliant
    itar_abac_tagged
    fips_crypto_envelope_ok
    spiffe_mtls_verified
}
