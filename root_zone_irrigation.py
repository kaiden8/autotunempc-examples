"""Paid POST /v1/templates/autotune for root_zone_irrigation."""

from client import post

post(
    "/v1/templates/autotune",
    {"name": "root_zone_irrigation", "max_trials": 2},
    authenticated=True,
)
