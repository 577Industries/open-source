"""Controller program templates stub.

Placeholder: returns fixed values; not a kinematics, collision or post-processing implementation.
Each dialect is a fixed string with the 55.04 mm and 0.015 mm figures written into it; no
trajectory, waypoint list or robot model is consulted.
"""
from __future__ import annotations
from typing import Dict

DIALECT_TEMPLATES: Dict[str, str] = {
    "FANUC": """/PROG  KINETIC_WORKCELL_01
/ATTR
OWNER       = MNEDITOR;
COMMENT     = "577i Kinetic URTS -> FANUC R-30iB Plus";
/MN
   1:  ! Datum-A 3-Fiducial Vision Frame ;
   2:  UFRAME_NUM=1 ;
   3:  UTOOL_NUM=2 ;
   4:  ! 6-Link Swept-Capsule Min Clearance: 55.04mm ;
   5:J P[1:STN_PORT_01_APPROACH] 40% FINE ;
   6:L P[2:BORE_F103_SCAN] 120mm/sec CNT10 ;
   7:L P[3:POCKET_F112_NDI] 85mm/sec FINE ;
/END""",
    "KUKA": """&ACCESS RVP
&REL 1
&COMMENT 577i Kinetic URTS -> KUKA KRC4
DEF KINETIC_WORKCELL_01 ( )
  BAS (#INITMOV, 0 )
  $BASE = BASE_DATA[1] ; Datum-A 3-Fiducial (0.015mm RMS)
  $TOOL = TOOL_DATA[2] ; Coaxial Laser-NDI Head
  ; 6-Link Swept-Capsule Min Clearance: 55.04mm
  PTP XSTN_PORT_01_APPROACH Vel=40 % PDAT1
  LIN XBORE_F103_SCAN Vel=0.12 m/s CPDAT1
  LIN XPOCKET_F112_NDI Vel=0.085 m/s CPDAT2
END""",
    "ABB": """MODULE KineticWorkcell01
  ! 577i Kinetic URTS -> ABB OmniCore RAPID
  TASK PERS wobjdata wobjDatumA := [FALSE, TRUE, "", [[1420.0, -310.0, 880.0],[1,0,0,0]], [[0,0,0],[1,0,0,0]]];
  PROC main()
    ! 6-Link Swept-Capsule Min Clearance: 55.04mm
    MoveJ pStnPort01Approach, v400, fine, tLaserNdi\\WObj:=wobjDatumA;
    MoveL pBoreF103Scan, v120, z10, tLaserNdi\\WObj:=wobjDatumA;
    MoveL pPocketF112Ndi, v85, fine, tLaserNdi\\WObj:=wobjDatumA;
  ENDPROC
ENDMODULE""",
    "ROS2": """# 577i Kinetic URTS -> SROS2 Humble MoveIt2 Trajectory Goal
header:
  frame_id: "datum_a_fiducial_frame"
  stamp: {sec: 1791936000, nanosec: 0}
controller_name: "whole_body_6dof_agv_controller"
swept_capsule_safety_margin_mm: 55.04
docking_tcp_residual_mm: 0.015
waypoints:
  - name: "STN_PORT_01_APPROACH"
    joints_deg: [-14.2, -26.8, 62.1, 0.0, 54.2, -12.5]
  - name: "BORE_F103_SCAN"
    joints_deg: [-8.4, -22.1, 58.4, 0.0, 54.2, -12.5]""",
}

def compile_urts_program(dialect: str = "FANUC") -> str:
    """Placeholder: returns fixed values; not a kinematics, collision or post-processing implementation.

    Returns the fixed template for the dialect; nothing is compiled.
    """
    key = dialect.upper()
    if key not in DIALECT_TEMPLATES:
        raise ValueError(f"Unsupported dialect: {dialect}")
    return DIALECT_TEMPLATES[key]
