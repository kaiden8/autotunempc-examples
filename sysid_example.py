"""Free POST /v1/sysid. No API key.

Simulates a 2-state discrete thermal zone, adds a little measurement noise,
and prints the fitted A, B, dt, and fit error next to the plant that made the log.
"""

from __future__ import annotations

import json
import random
import sys

from client import call

# Discrete zone. State is two temperatures. Input is heater power.
A_TRUE = [[0.96, 0.03], [0.02, 0.90]]
B_TRUE = [[0.08], [0.01]]
DT = 0.5
NOISE = 0.002
N_SAMPLES = 80


def simulate() -> list[dict]:
    rng = random.Random(7)
    state = [0.25, 0.20]
    samples = []
    clock = 0.0
    for step in range(N_SAMPLES):
        heater = 0.6 if (step // 10) % 2 == 0 else 0.0
        heater += 0.15 * ((step % 7) - 3) / 3.0
        measured = [state[0] + rng.gauss(0.0, NOISE), state[1] + rng.gauss(0.0, NOISE)]
        samples.append({"t": clock, "u": [heater], "y": measured})
        state = [
            A_TRUE[0][0] * state[0] + A_TRUE[0][1] * state[1] + B_TRUE[0][0] * heater,
            A_TRUE[1][0] * state[0] + A_TRUE[1][1] * state[1] + B_TRUE[1][0] * heater,
        ]
        clock += DT
    return samples


def _format(matrix: list) -> str:
    return json.dumps(matrix)


def main() -> None:
    status, raw = call("/v1/sysid", {"samples": simulate()}, authenticated=False)
    if status >= 400:
        print(status, file=sys.stderr)
        print(raw, file=sys.stderr)
        raise SystemExit(1)
    fitted = json.loads(raw)
    print("true A", _format(A_TRUE))
    print("fit  A", _format(fitted["A"]))
    print("true B", _format(B_TRUE))
    print("fit  B", _format(fitted["B"]))
    print("true dt", DT)
    print("fit  dt", fitted["dt"])
    print("fit_error", fitted["fit_error"])


if __name__ == "__main__":
    main()
