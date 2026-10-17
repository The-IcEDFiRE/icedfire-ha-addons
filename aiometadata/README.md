# AIOMetadata

Upstream image: `ghcr.io/cedya77/aiometadata:latest`.

Host port: `3232`. Persisted upstream directory: `/app/addon/data` (mapped from Home Assistant's private app data).

Home Assistant app options are read from `/app/addon/data/options.json`. This is a **private managed data mount**.

`environment_overrides_json` accepts a JSON object containing additional upstream environment variables. Environment values remain in app options/backups; do not put secrets in Git. Blank optional values are not exported. See the upstream documentation for valid variable names.

**Important:** This is an independently built wrapper, not an official upstream Home Assistant app. Validate startup and a restore before unattended updates.
