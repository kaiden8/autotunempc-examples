"""Small HTTPS client for the public AutoTuneMPC API."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.autotunempc.com"


def base_url() -> str:
    """Public API, or AUTOTUNE_API_BASE when that variable is set."""
    raw = os.environ.get("AUTOTUNE_API_BASE", "").strip() or API
    return raw.rstrip("/")


def call(path: str, body: dict, *, authenticated: bool) -> tuple[int, str]:
    """POST JSON and return the status and response text. Does not print."""
    headers = {"content-type": "application/json", "accept": "application/json"}
    if authenticated:
        key = os.environ.get("AUTOTUNE_API_KEY", "").strip()
        if not key:
            print("Set AUTOTUNE_API_KEY to the pack key.", file=sys.stderr)
            raise SystemExit(2)
        headers["X-API-Key"] = key
    request = urllib.request.Request(
        base_url() + path,
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode(errors="replace")


def post(path: str, body: dict, *, authenticated: bool) -> None:
    status, raw = call(path, body, authenticated=authenticated)
    print(status)
    print(raw)
    if status >= 400:
        raise SystemExit(1)
