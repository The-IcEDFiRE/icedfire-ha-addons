# My Lists (Local) — experimental

This app runs the original My Lists Cloudflare Worker code locally using Wrangler's development runtime. It is NOT Cloudflare-hosted; KV and D1 live in `/data`. **Wrangler dev is a development runtime, not a production-supported server.** Validate thoroughly before relying on it.

## Installing
Add this folder and the workflow to your existing Home Assistant addon repository. The GitHub Actions workflow obtains upstream source and builds container images. The `image` key intentionally references GHCR and cannot install until images are successfully published.

Set a long unique `admin_key`. The UI is served on port 8787 and must not be exposed publicly without a trusted reverse proxy with authentication. TMDB search requires an optional `tmdb_api_key`, and other catalog integrations can still contact their external APIs.

The web application and databases are local. This does **not** mean all metadata is offline. Source code updates are fetched by CI from GitHub, not at runtime.

This creates Stremio catalogs. It is **not** a parental playback access-control barrier. Never give kids unrestricted upstream AIOStreams credentials.

## Notes
- Back up `/data` through Home Assistant; app uses cold backups.
- Schema initialization is performed on first start; upstream migrations require testing prior to deployment.
- OAuth providers may require a public HTTPS domain, so don't assume they function over a private HTTP address.
- If existing data exists, do not delete `/data/.initialized` casually.
