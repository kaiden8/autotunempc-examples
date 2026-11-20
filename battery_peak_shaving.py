"""Paid POST /v1/templates/autotune for battery_peak_shaving."""

from client import post

post(
    "/v1/templates/autotune",
    {"name": "battery_peak_shaving", "max_trials": 2},
    authenticated=True,
)
