<div align="center">

<img src="icon.png" alt="aiomanager community icon" width="108">

</div>

# AIOManager

Upstream image: `ghcr.io/sonicx161/aiomanager:latest`.

Host port: `1610`. Persisted upstream directory: `/app/data` (mapped from Home Assistant's private app data).

Home Assistant app options are read from `/app/data/options.json`. This is a **private managed data mount**.

`environment_overrides_json` accepts a JSON object containing additional upstream environment variables. Environment values remain in app options/backups; do not put secrets in Git. Blank optional values are not exported. See the upstream documentation for valid variable names.

**Important:** This is an independently built wrapper, not an official upstream Home Assistant app. Validate startup and a restore before unattended updates.
