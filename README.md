# AutoTuneMPC examples

```bash
claude mcp add --transport http autotunempc https://api.autotunempc.com/mcp
```

Skill: https://autotunempc.com/SKILL.md

Site: https://autotunempc.com

## Run in 30 seconds

```bash
python3 validate.py
python3 export_controller.py
python3 sysid_example.py
export AUTOTUNE_API_KEY='paste the pack key'
python3 differential_drive.py
python3 battery_peak_shaving.py
python3 root_zone_irrigation.py
```

`validate.py`, `export_controller.py`, and `sysid_example.py` are free and need no key. `validate.py` calls `POST /v1/validate`. `export_controller.py` calls `POST /v1/export`. `sysid_example.py` calls `POST /v1/sysid`. The other three call paid `POST /v1/templates/autotune` and read `AUTOTUNE_API_KEY` from the environment. Nothing in this repo contains a key.

`export_controller.py` targets are `casadi_python` (default), `ros2_node`, and `acados_python`. The ICR plant is kinematic only.

`sysid_example.py` sends `{"samples": [{"t", "u", "y"}, ...]}` and returns `A`, `B`, `dt`, and `fit_error`.

## Prices

The $29 pack is 1000 solves and 4 autotunes. A template autotune spends 2 of those autotune credits.

x402 prices are solve $0.02, autotune $1.50, and template autotune $2.00.

`X-API-Key` is the human door. A 402 plus `PAYMENT-SIGNATURE` is the agent door.

API: https://api.autotunempc.com

MCP: https://api.autotunempc.com/mcp
