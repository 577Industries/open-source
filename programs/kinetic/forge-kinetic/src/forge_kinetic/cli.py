"""CLI entry point for the Kinetic Core Physical AI & Robotics Platform."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .perception import compute_sensor_envelope
from .kinematics import solve_whole_body_ik
from .ccd import evaluate_6link_swept_ccd
from .urts import compile_urts_program

def main() -> int:
    parser = argparse.ArgumentParser(prog="forge-kinetic", description="577 Industries Kinetic Core Robotics Platform")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_env = sub.add_parser("envelope", help="Evaluate sensor operating envelope and HITL handoff boundary")
    p_env.add_argument("--standoff-mm", type=float, default=780.0)
    p_env.add_argument("--occluder-offset", type=float, default=0.18)
    sub.add_parser("ik-solve", help="Solve redundant 6-DOF + AGV whole-body inverse kinematics")
    p_ccd = sub.add_parser("swept-ccd", help="Evaluate 200 Hz 6-link swept-capsule SDF collision clearance")
    p_ccd.add_argument("--freq-hz", type=int, default=200)
    p_urts = sub.add_parser("urts-compile", help="Compile URTS trajectory into native controller code")
    p_urts.add_argument("--dialect", default="FANUC", choices=["FANUC", "KUKA", "ABB", "ROS2"])
    args, _ = parser.parse_known_args()

    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)

    if args.cmd == "envelope":
        res = compute_sensor_envelope(args.standoff_mm, 42.0, args.occluder_offset).to_dict()
        (out_dir / "sensor-envelope.json").write_text(json.dumps(res, indent=2))
        print(json.dumps(res, indent=2))
    elif args.cmd == "ik-solve":
        res = solve_whole_body_ik([1420.0, -310.0, 880.0]).to_dict()
        (out_dir / "ik-posture.json").write_text(json.dumps(res, indent=2))
        print(json.dumps(res, indent=2))
    elif args.cmd == "swept-ccd":
        res = evaluate_6link_swept_ccd(args.freq_hz).to_dict()
        (out_dir / "swept-ccd-profile.json").write_text(json.dumps(res, indent=2))
        print(json.dumps(res, indent=2))
    elif args.cmd == "urts-compile":
        code = compile_urts_program(args.dialect)
        (out_dir / f"urts-{args.dialect.lower()}.txt").write_text(code)
        print(code)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
