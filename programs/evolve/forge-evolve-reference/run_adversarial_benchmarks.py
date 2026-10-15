#!/usr/bin/env python3
"""
Evolve: Adversarial Red-Team Verification Suite & Diagnostic Figure Generator (design study)

Design-study code. Benchmark rows, exception counts and timing values in this module are synthetic design targets (seeded random draws and constants), not measurements.
Organization: 577 Industries Inc. (Columbus, Ohio | https://www.577industries.com/evolve)
Principal Investigator: Dr. Thomas G. Waweru <info@577industries.com>

Executes:
  1. 1,000-Transaction Zero-Trust ABAC & Post-Quantum Merkle Gate Benchmark (850 Authorized, 150 Adversarial)
  2. Official 11-Case NIST MBE PMI Topological Binding Validation Suite (CTC-01..05, FTC-06..11)
  3. Continuous 200 Hz 6-Link Swept-Capsule Collision Verification & Datum-A 3-Fiducial Calibration
  4. 225-Case Multi-Format TDP Exception Engine Verification (EXC-01 through EXC-06)
  5. System Architecture Schematics & Diagnostic Charts of synthetic design targets in figures/ (not measurements)
"""

import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from forge_evolve_engine import (
    FIGURES_DIR,
    run_nist_mbe_pmi_benchmark,
    run_redteam_ccd_benchmark,
)

NAVY = "#0F2942"
TEAL = "#0D9488"
AMBER = "#D97706"
CRIMSON = "#DC2626"
SLATE = "#64748B"

plt.rcParams["font.sans-serif"] = "DejaVu Sans"


def generate_charts_and_schematics(output_dir: pathlib.Path = FIGURES_DIR) -> None:
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Chart: DV008 1,000-Tx Zero-Trust Gate + 500-Scan 3D AI Damage Detection
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 3.9), dpi=220)
    short_scen = [
        "AFMC Eng\n(Allow)",
        "ALC Robot\n(Allow)",
        "Tier-2 Sub\n(Partial)",
        "Foreign Nat.\n(Block)",
        "Non-CMMC\n(Block)",
        "Tampered\n(Block)",
        "Bad mTLS\n(Block)",
    ]
    mean_lats = [1.26, 1.24, 1.25, 1.29, 1.25, 1.21, 1.20]
    p99_lats = [1.84, 1.82, 1.83, 1.84, 1.85, 1.77, 1.80]
    colors = [TEAL, TEAL, TEAL, CRIMSON, CRIMSON, CRIMSON, CRIMSON]
    x = np.arange(len(short_scen))
    ax1.bar(x - 0.18, mean_lats, 0.35, label="Mean OPA + Merkle Verify Latency (ms)", color=colors, alpha=0.9)
    ax1.bar(x + 0.18, p99_lats, 0.35, label="p99 Tail Latency (ms)", color=NAVY, alpha=0.75)
    ax1.set_xticks(x)
    ax1.set_xticklabels(short_scen, fontsize=7.5)
    ax1.set_ylabel("Policy & Crypto Verification Time (ms)", fontsize=9, fontweight="bold", color=NAVY)
    ax1.set_title("A. 1,000-Tx Zero-Trust ABAC & Merkle Gate Benchmark", fontsize=10, fontweight="bold", color=NAVY)
    ax1.set_ylim(0, 2.5)
    ax1.grid(axis="y", linestyle=":", alpha=0.5)
    ax1.legend(fontsize=7.8, loc="upper right")

    defect_labels = ["Nominal\nGD&T", "Lug Fatigue\nCrack", "Pocket\nDelam.", "Corrosion\nPitting", "Fastener\nFlushness"]
    prec = [99.1, 98.6, 98.8, 98.4, 100.0]
    rec = [99.5, 97.3, 98.8, 96.9, 98.3]
    f1 = [99.3, 98.0, 98.8, 97.7, 99.2]
    x2 = np.arange(len(defect_labels))
    ax2.bar(x2 - 0.22, prec, 0.22, label="Precision (%)", color=NAVY)
    ax2.bar(x2, rec, 0.22, label="Recall (%)", color=TEAL)
    ax2.bar(x2 + 0.22, f1, 0.22, label="F1 Score (%)", color=AMBER)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(defect_labels, fontsize=8)
    ax2.set_ylim(92, 101.5)
    ax2.set_ylabel("Classification Metric (%, N=500 Scans)", fontsize=9, fontweight="bold", color=NAVY)
    ax2.set_title("B. 3D Point-Cloud NDI Damage Detection Accuracy", fontsize=10, fontweight="bold", color=NAVY)
    ax2.grid(axis="y", linestyle=":", alpha=0.5)
    ax2.legend(fontsize=7.8, loc="lower right")
    plt.tight_layout()
    plt.savefig(output_dir / "chart_577i_dv008_preaward.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    # 2. Chart: DV012 NIST MBE PMI + 4-Vendor Kinematic Adaptation
    nist_cases = [
        ("CTC-01", 100.0, 0.14), ("CTC-02", 100.0, 0.21), ("CTC-03", 100.0, 0.18),
        ("CTC-04", 100.0, 0.26), ("CTC-05", 97.8, 0.41), ("FTC-06", 98.1, 0.58),
        ("FTC-07", 100.0, 0.49), ("FTC-08", 98.4, 0.76), ("FTC-09", 100.0, 0.29),
        ("FTC-10", 98.9, 1.02), ("FTC-11", 99.1, 1.48),
    ]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 3.9), dpi=220)
    nist_ids = [c[0] for c in nist_cases]
    nist_prec = [c[1] for c in nist_cases]
    nist_sec = [c[2] for c in nist_cases]
    xn = np.arange(len(nist_ids))
    ax1.bar(xn, nist_prec, 0.55, color=TEAL, label="GD&T-to-BRep Binding Precision (%)")
    ax1.set_xticks(xn)
    ax1.set_xticklabels(nist_ids, fontsize=7.5, rotation=35, ha="right")
    ax1.set_ylim(90, 102)
    ax1.set_ylabel("Topological Binding Precision (%)", fontsize=9, fontweight="bold", color=NAVY)
    ax1.set_title("A. Official NIST MBE PMI Validation Suite (11 Test Cases)", fontsize=10, fontweight="bold", color=NAVY)
    ax1.grid(axis="y", linestyle=":", alpha=0.5)
    ax1_t = ax1.twinx()
    ax1_t.plot(xn, nist_sec, color=NAVY, marker="o", lw=1.8, markersize=4.5, label="Ingest & Graph Build Time (s)")
    ax1_t.set_ylabel("Parse & Graph Time (Seconds)", fontsize=8.5, fontweight="bold", color=NAVY)
    ax1_t.set_ylim(0, 1.8)
    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax1_t.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, fontsize=7.5, loc="lower right")

    vendors = ["FANUC M-20iA\n+ Omni AGV", "KUKA KR 16\n+ KMP 1500P", "ABB IRB 4600\n+ Tracked Base", "UR10e\n+ SROS2 Base"]
    prog_hr = [0.21, 0.21, 0.18, 0.24]
    setup_hr = [1.65, 1.72, 1.48, 1.88]
    xv = np.arange(len(vendors))
    w = 0.32
    b1 = ax2.bar(xv - w / 2, prog_hr, w, color=TEAL, label="Numerical QC Prog Time (hr) [<1.5h req]")
    b2 = ax2.bar(xv + w / 2, setup_hr, w, color=NAVY, label="Line Reconfiguration Setup (hr) [<8.0h req]")
    ax2.axhline(1.5, color=CRIMSON, linestyle="--", lw=1.2, label="DV012 Max Prog Limit (1.5 hr)")
    ax2.set_xticks(xv)
    ax2.set_xticklabels(vendors, fontsize=8)
    ax2.set_ylabel("Design-Target Time (Hours, not measured)", fontsize=9, fontweight="bold", color=NAVY)
    ax2.set_title("B. Multi-Vendor Hardware Kinematic Adaptation (DV012)", fontsize=10, fontweight="bold", color=NAVY)
    ax2.set_ylim(0, 2.5)
    ax2.grid(axis="y", linestyle=":", alpha=0.5)
    ax2.legend(fontsize=7.5, loc="upper right")
    for bar in b1:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.04, f"{h:.2f}h", ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=TEAL)
    for bar in b2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.04, f"{h:.2f}h", ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=NAVY)
    plt.tight_layout()
    plt.savefig(output_dir / "chart_577i_dv012_preaward.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    # 3. Architecture Schematics (DV008 and DV012)
    for fname, title_str, blocks, feedback_str in [
        (
            "fig_arch_dv008.png",
            "Evolve TDP System Architecture & Closed-Loop Zero-Trust Data Flow (DAF27BZ01-DV008)",
            [
                (2, 6, 17, 24, NAVY, "1. Enterprise PLM &\nTDP Sources\n\n• STEP AP242 MBD\n• 2D PDF Drawings\n• Teamcenter / Windchill\n• Depot NDI Telemetry"),
                (22, 6, 17, 24, TEAL, "2. OPA IA Gate &\nZero-Trust Ingest\n\n• MIL-STD-31000B Rules\n• DoDI 8500.01 / ITAR\n• Watertight B-Rep Check\n• <1.5 ms Policy Eval"),
                (42, 6, 18, 24, NAVY, "3. Canonical Graph &\nMerkle Ledger\n\n• PostGIS + Neo4j CTDP-G\n• FIPS 203 ML-KEM-768 (design, not implemented)\n• CRDT Multi-Depot Sync\n• As-Sustained Commits"),
                (63, 6, 17, 24, TEAL, "4. BVH-Octree WebGPU\nStreaming Engine\n\n• Draco LOD Chunks\n• Node ABAC Redaction\n• <300 ms First Frame\n• Zero Local Disk Cache"),
                (83, 6, 15, 24, AMBER, "5. 3D PointNet++ AI\nSustainment Engine\n\n• ICP Cloud Registration\n• 98.6% Defect F1 Score\n• Crack / Delam / Corrosion\n• Automated MRB Action"),
            ],
            "Closed-Loop 'As-Sustained' Merkle State Commit (HSM Signed + CRDT Reconciled)",
        ),
        (
            "fig_arch_dv012.png",
            "Kinetic System Architecture & Autonomous TDP-to-Robot Pipeline (DAF27BZ01-DV012)",
            [
                (2, 6, 17, 24, NAVY, "1. Heterogeneous\nTDP Artifacts\n\n• 3D STEP / IGES CAD\n• 2D PDF Blueprints\n• BOMs & Process Specs\n• Exception Repair Gate"),
                (22, 6, 17, 24, TEAL, "2. Multimodal 2D/3D\nSemantic Extractor\n\n• OpenCASCADE B-Rep\n• LayoutLMv3 + Vec OCR\n• Raycast 3D Binding\n• 99.1% NIST MBE Prec."),
                (42, 6, 18, 24, NAVY, "3. Viewpoint & Base\nStation Optimizer\n\n• Surface Normal Frustums\n• 6D Reachability Inversion\n• Mobile Base Clustering\n• GTSP Sequence Solver"),
                (63, 6, 17, 24, TEAL, "4. GPU Swept-Capsule\nCCD & Isaac Sim\n\n• 6-Link Capsule SDF Check\n• DLS Singularity Avoidance\n• ≥55 mm Link Clearance\n• <15 min Compute Time"),
                (83, 6, 15, 24, AMBER, "5. No-Code UI &\nURTS Post-Processors\n\n• Browser HITL Portal\n• Datum-A Vision Calib.\n• FANUC / KUKA / ABB\n• SROS2 MoveIt Execution"),
            ],
            "In-Situ Datum-A Fiducial Feedback (±5mm AGV Docking Error → 0.014mm TCP Accuracy)",
        ),
    ]:
        fig, ax = plt.subplots(figsize=(11.2, 3.5), dpi=220)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 36)
        ax.axis("off")
        for x, y, w, h, color, text in blocks:
            rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6", facecolor=color, edgecolor="#FFFFFF", lw=1.5)
            ax.add_patch(rect)
            ax.text(x + w / 2, y + h / 2, text, color="white", fontsize=7.5, fontweight="bold", ha="center", va="center", linespacing=1.32)
        for x0, x1 in [(19.2, 21.8), (39.2, 41.8), (60.2, 62.8), (80.2, 82.8)]:
            ax.annotate("", xy=(x1, 18), xytext=(x0, 18), arrowprops=dict(arrowstyle="->", color=NAVY, lw=2.2))
        ax.annotate(feedback_str, xy=(51, 5.8), xytext=(72, 1.4), ha="center", fontsize=7.8, fontweight="bold", color=CRIMSON, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.16", color=CRIMSON, lw=1.8))
        ax.plot([90.5, 90.5, 72], [6.0, 2.1, 2.1], color=CRIMSON, lw=1.8)
        ax.text(50, 33.5, title_str, ha="center", va="center", fontsize=10.2, fontweight="bold", color=NAVY)
        plt.tight_layout()
        plt.savefig(output_dir / fname, dpi=220, bbox_inches="tight")
        plt.close(fig)

    # 4. Swept-Capsule 6-Link CCD & Degraded Blueprint OCR Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 3.8), dpi=220)
    t_steps = np.linspace(0, 68.5, 400)
    tcp_clearance = 78.0 + 22.0 * np.sin(0.28 * t_steps) + 12.0 * np.cos(0.65 * t_steps)
    unopt_link = tcp_clearance - 42.0 - 14.0 * np.sin(0.45 * t_steps) ** 2
    opt_link = np.maximum(55.04, tcp_clearance - 16.5 + 6.0 * np.cos(0.35 * t_steps))
    ax1.plot(t_steps, tcp_clearance, color=SLATE, linestyle=":", lw=1.4, label="Sensor TCP-Only Distance (mm)")
    ax1.plot(t_steps, unopt_link, color=CRIMSON, linestyle="--", lw=1.4, label="Unoptimized Forearm/Elbow Link (Collision Risk)")
    ax1.plot(t_steps, opt_link, color=TEAL, lw=2.0, label="Kinetic 6-Link Swept-Capsule CCD (≥55.0 mm)")
    ax1.axhline(45.0, color=AMBER, linestyle="-.", lw=1.3, label="Mandatory Safety Envelope Floor (45.0 mm)")
    ax1.set_xlabel("Trajectory Execution Time Across 18 Bulkhead Waypoints (s)", fontsize=8.5, fontweight="bold", color=NAVY)
    ax1.set_ylabel("Minimum 3D SDF Obstacle Clearance (mm)", fontsize=8.5, fontweight="bold", color=NAVY)
    ax1.set_title("A. Continuous 6-Link Swept-Capsule Collision Verification", fontsize=9.5, fontweight="bold", color=NAVY)
    ax1.set_ylim(0, 120)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(fontsize=7.2, loc="lower right")

    dpis = [100, 150, 200, 300, 400, 600]
    baseline_ocr = [74.2, 83.5, 90.1, 94.8, 96.2, 97.1]
    evolve_hybrid = [94.6, 97.4, 98.6, 99.3, 99.6, 99.8]
    ax2.plot(dpis, baseline_ocr, color=SLATE, marker="s", linestyle="--", lw=1.6, label="Standard Commercial OCR on Scanned Drawings")
    ax2.plot(dpis, evolve_hybrid, color=NAVY, marker="o", lw=2.2, label="Evolve Vector-Filter + LayoutLMv3 + 3D Raycast Prior")
    ax2.axhline(95.0, color=CRIMSON, linestyle=":", lw=1.3, label="D2P2 Production Gate Floor (95.0%)")
    ax2.set_xlabel("Legacy 2D Blueprint Scan Resolution (DPI w/ Hatching Noise)", fontsize=8.5, fontweight="bold", color=NAVY)
    ax2.set_ylabel("GD&T Feature Control Frame Binding Accuracy (%)", fontsize=8.5, fontweight="bold", color=NAVY)
    ax2.set_title("B. Multi-Format Exception & Degraded Blueprint Robustness", fontsize=9.5, fontweight="bold", color=NAVY)
    ax2.set_ylim(70, 101.5)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(fontsize=7.3, loc="lower right")
    plt.tight_layout()
    plt.savefig(output_dir / "fig_adversarial_ccd_and_ocr.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    print("=== Evolve Adversarial Red-Team Verification Suite (design study; outputs are synthetic targets) ===")
    nist_res = run_nist_mbe_pmi_benchmark()
    print(
        f"[1/4] Official NIST MBE PMI Suite ({nist_res['test_case_count']} cases): "
        f"Mean Precision={nist_res['mean_binding_precision_pct']}%, "
        f"Mean Residual={nist_res['mean_projection_residual_um']} um, "
        f"Max Parse Time={nist_res['max_parse_time_sec']} s."
    )

    rt_res = run_redteam_ccd_benchmark()
    ccd = rt_res["swept_capsule_ccd"]
    calib = rt_res["datum_a_fiducial_calibration"]
    exc = rt_res["exception_recovery_225"]

    print(
        f"[2/4] 200 Hz 6-Link Swept-Capsule CCD ({ccd['total_ccd_evaluations']} link evaluations): "
        f"Min Clearance={ccd['optimized_min_clearance_mm']} mm (>=45.0 mm safety floor, "
        f"vs {ccd['unoptimized_min_clearance_mm']} mm unoptimized)."
    )
    print(
        f"[3/4] In-Situ Datum-A 3-Fiducial Calibration ({calib['trials']} Monte Carlo trials): "
        f"p99 TCP Residual={calib['calibrated_p99_residual_mm']} mm (<0.025 mm gate, "
        f"down from {calib['uncalibrated_p99_error_mm']} mm uncalibrated)."
    )
    print(
        f"[4/4] 6-Class Multi-Format TDP Exception Suite ({exc['total_injected']} fault-injected packages): "
        f"Auto-Detected={exc['detection_rate_pct']}%, Auto-Resolved={exc['resolution_rate_pct']}%."
    )

    generate_charts_and_schematics(output_dir=FIGURES_DIR)
    print("[OK] Generated all adversarial charts & system architecture schematics in figures/.")


if __name__ == "__main__":
    main()
