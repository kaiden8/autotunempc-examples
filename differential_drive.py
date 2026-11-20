"""Paid POST /v1/templates/autotune for differential_drive."""

from client import post

post(
    "/v1/templates/autotune",
    {"name": "differential_drive", "max_trials": 2},
    authenticated=True,
)
