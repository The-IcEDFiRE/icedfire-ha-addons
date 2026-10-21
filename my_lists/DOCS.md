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

## Private owner-only mode

This IcEDFiRE package places a private authentication gateway in front of the original Worker. The Worker binds only to `127.0.0.1:8788` **inside the container**, and only the gateway listens on port 8787. A unique `admin_key` of at least 24 characters is **required**; the gateway refuses to start otherwise.

- The browser prompts for Basic authentication: username `owner`, password = the Home Assistant `admin_key`. After authentication it issues a SameSite=Strict, HttpOnly session cookie for same-origin application requests.
- No one without this authentication can access registration, sign-in, account or list-writing API routes. This is server-side access control, not a hidden registration button.
- Anonymous GET/HEAD requests are allowed only for Stremio protocol manifest/catalog/metadata JSON routes, so AIOStreams can read catalogs. **Anyone with a catalog URL can read those catalogs.** Do not expose sensitive list contents via public URLs.
- `private_mode` is informational/reserved in `config.yaml`: the gateway always enforces private access. It cannot be disabled by changing this setting.
- This is an experimental gateway, not an audited identity service. Only expose it over HTTPS via a trusted proxy; do not put raw port 8787 on the public Internet. Keep Home Assistant's admin credentials separate.
- `admin_key` also feeds the upstream My Lists admin dashboard, so the same password currently protects both layers.

**Test before using:** An unauthenticated `GET /` and any `POST /api/...` must return 401; owner-authenticated UI works; and a public `GET /manifest.json` is readable. Do not remove your current installation until these checks work.
