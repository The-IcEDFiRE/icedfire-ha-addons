# AIOStreams Home Assistant app

AIOStreams Docker image wrapped as a Home Assistant app, using Home Assistant managed data storage.

- `base_url`: public URL for your AIOStreams endpoint
- `secret_key`: **existing** 64-digit hexadecimal encryption key; never rotate casually
- `operator_auth`: optional comma-separated `username:password` values; treated as `AIOSTREAMS_AUTH`
- `log_level`: logging level

The SQLite database lives at `/app/data/db.sqlite`, because `/app/data` maps to the HA-managed app data directory. `options.json` is read from the same managed mount.

Upstream documentation: https://docs.aiostreams.viren070.me/getting-started/deployment/
