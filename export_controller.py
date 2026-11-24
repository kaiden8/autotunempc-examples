"""Free POST /v1/export. No API key.

Kinematic ICR skid-steer. Lateral velocity is slip times yaw rate.
This is not a dynamic rover model. It ignores dynamic slip.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from client import call

TARGETS = ("casadi_python", "ros2_node", "acados_python")


def payload(target: str) -> dict:
    return {
        "target": target,
        "system": {
            "kind": "nonlinear",
            "name": "icr_skid_steer",
            "parameters": {"dt": 0.1, "slip": 0.2},
            "N": 8,
            "u_min": [0.0, -1.2],
            "u_max": [1.2, 1.2],
            "du_min": [-0.8, -0.8],
            "du_max": [0.8, 0.8],
        },
        "x0": [0.0, 0.0, 0.0],
        "x_ref": [0.4, 0.0, 0.0],
        "Q": [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]],
        "R": [[0.2, 0.0], [0.0, 0.2]],
        "Rd": [[0.2, 0.0], [0.0, 0.2]],
        "Qf": [[8.0, 0.0, 0.0], [0.0, 8.0, 0.0], [0.0, 0.0, 8.0]],
    }


def destination(out: str, filename: str) -> Path:
    path = Path(out)
    if path.exists() and path.is_dir():
        return path / filename
    if out.endswith(("/", "\\")) or path.suffix == "":
        path.mkdir(parents=True, exist_ok=True)
        return path / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a free standalone controller. No API key.")
    parser.add_argument("--target", choices=TARGETS, default="casadi_python")
    parser.add_argument("--out", default=".", help="Directory or .py path for the downloaded file.")
    args = parser.parse_args()
    status, raw = call("/v1/export", payload(args.target), authenticated=False)
    if status >= 400:
        print(status, file=sys.stderr)
        print(raw, file=sys.stderr)
        raise SystemExit(1)
    body = json.loads(raw)
    filename = str(body.get("filename") or "mpc_controller.py")
    written = destination(args.out, filename)
    written.write_text(str(body.get("code") or ""), encoding="utf-8")
    print(f"wrote {written}")
    usage = str(body.get("usage") or "").strip()
    if usage:
        print(usage)
    steps = body.get("instructions") or []
    if isinstance(steps, str):
        print(steps)
    else:
        for step in steps:
            print(step)


if __name__ == "__main__":
    main()
