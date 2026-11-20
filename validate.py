"""Free POST /v1/validate. No API key."""

from client import post

post(
    "/v1/validate",
    {
        "system": {
            "kind": "nonlinear",
            "name": "double_integrator",
            "parameters": {"dt": 0.1},
            "N": 8,
        },
        "x0": [0.0, 0.0],
        "x_ref": [1.0, 0.0],
    },
    authenticated=False,
)
