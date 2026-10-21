# Kids Lists (Local)

This is **not** the original My Lists application. It is a small fully local alternative, created for the IcEDFiRE Home Assistant app repository. It uses SQLite stored at `/data/lists.sqlite3` and a phone-friendly admin page.

1. Set a strong `admin_password` in Configuration before starting.
2. Optionally enter a TMDB v3 API key for searching and one-click title approval. This feature calls TMDB; the web UI, list storage and catalogs do **not** use hosted My Lists.
3. Start the app and open its Web UI. Add IMDb IDs manually or search and approve using TMDB.
4. Copy `http://YOUR-HOME-ASSISTANT-IP:8099/manifest.json` into AIOStreams as a custom addon. Use an HTTPS URL if your player cannot reach private HTTP hosts.
5. Select `Approved Movies` and `Approved Series` as catalog rows. List edits take effect on the server immediately; client caching can cause a brief delay.

**Safety:** This addon creates curated catalogs only. It does not prevent Stremio/AIOStreams playback of unapproved titles. Do not rely on it for strict parental enforcement. Restrict access to the admin port using your firewall or trusted LAN/VPN. It does not include an ingress proxy, and is not intended to be exposed publicly without HTTPS and access controls.

**Automatic updates:** publishing a new GHCR image and changing `config.yaml` version announces an update to Home Assistant. The included workflow builds on updates to this app. This is an independent local implementation; it does not automatically inherit upstream My Lists features.
