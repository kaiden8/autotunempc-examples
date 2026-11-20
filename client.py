"""Small HTTPS client for the public AutoTuneMPC API."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.autotunempc.com"


def post(path: str, body: dict, *, authenticated: bool) -> None:
    headers = {"content-type": "application/json", "accept": "application/json"}
    if authenticated:
        key = os.environ.get("AUTOTUNE_API_KEY", "").strip()
        if not key:
            print("Set AUTOTUNE_API_KEY to the pack key.", file=sys.stderr)
            raise SystemExit(2)
        headers["X-API-Key"] = key
    request = urllib.request.Request(
        API + path,
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read().decode()
            status = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        status = exc.code
    print(status)
    print(raw)
    if status >= 400:
        raise SystemExit(1)
