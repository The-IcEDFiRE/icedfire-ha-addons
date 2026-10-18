# AIOMetadata

AIOMetadata runs as a managed Home Assistant app in this repository.

## First start

1. Install the app.
2. Open the **Configuration** tab.
3. Configure the API keys and data settings you need.
4. Start the app.
5. Open the UI from the **Info** tab or browse to `http://HOME_ASSISTANT_IP:3232/configure`.

## Configuration options

Labels and help text also appear in the Home Assistant Configuration tab. Optional fields left unset use the upstream defaults.

### Public Add-on URL

`host_name` → `HOST_NAME`

Publicly accessible base URL used in generated manifest and resource links.

### TMDB API Key (Public)

`tmdb_api_key` → `TMDB_API_KEY`

Exposed to visitors by upstream configure API. Prefer Built-in TMDB Key for shared deployments.

### TVDB API Key (Public)

`tvdb_api_key` → `TVDB_API_KEY`

May be exposed to visitors. Prefer Built-in TVDB Key for shared deployments.

### Fanart.tv API Key (Public)

`fanart_api_key` → `FANART_API_KEY`

May be exposed to visitors. Prefer Built-in Fanart Key for shared deployments.

### Redis Connection URL

`redis_url` → `REDIS_URL`

Optional connection string to an external Redis instance.

### Database Connection URL

`database_uri` → `DATABASE_URI`

SQLite or PostgreSQL connection URI. The default stores SQLite in managed app storage

### Administrator API Key

`admin_key` → `ADMIN_KEY`

Protects administrative API endpoints. Generate a long random secret.

### Artwork Signing Secret

`image_proxy_signing_secret` → `IMAGE_PROXY_SIGNING_SECRET`

Signs poster and artwork proxy links. Changing it invalidates existing signed image URLs.

### Private Built-in TMDB Key

`built_in_tmdb_api_key` → `BUILT_IN_TMDB_API_KEY`

Server-side default for users who do not provide their own TMDB key; not exposed to browsers.

### Private Built-in TVDB Key

`built_in_tvdb_api_key` → `BUILT_IN_TVDB_API_KEY`

Server-side fallback for TVDB; preferred on shared instances.

### Private Built-in Fanart Key

`built_in_fanart_api_key` → `BUILT_IN_FANART_API_KEY`

Server-side fallback for artwork API requests.

### Private Built-in RPDB Key

`built_in_rpdb_api_key` → `BUILT_IN_RPDB_API_KEY`

Server-side fallback for Rating Poster Database.

### Private Built-in MDBList Key

`built_in_mdblist_api_key` → `BUILT_IN_MDBLIST_API_KEY`

Fallback billed per use; use cautiously on public instances.

### Private Built-in Gemini Key

`built_in_gemini_api_key` → `BUILT_IN_GEMINI_API_KEY`

Server-side AI search API key; shared usage may incur costs.

### RPDB API Key (Public)

`rpdb_api_key` → `RPDB_API_KEY`

Browser-visible default Rating Poster Database API key.

### Logging Detail

`log_level` → `LOG_LEVEL`

How much information to write to logs.

### Dashboard Log History Limit

`log_buffer_size` → `LOG_BUFFER_SIZE`

Number of recent log entries kept in memory.

### Application Mode

`node_env` → `NODE_ENV`

Use production for normal operation.

### Run Database Migrations

`run_migrations` → `RUN_MIGRATIONS`

Create/update database tables at startup. Disable only for special read replicas.

### Read Replica Database URL

`database_read_uri` → `DATABASE_READ_URI`

Optional read-only PostgreSQL replica.

### Warm Cache on Startup

`cache_warmup_on_startup` → `CACHE_WARMUP_ON_STARTUP`

Load frequently requested metadata after startup.

### Maximum Catalogs per User

`max_catalogs` → `MAX_CATALOGS`

Optional cap on catalog selections, helpful on public instances.

### Safe-for-Work Mode

`sfw_mode` → `SFW_MODE`

Filter explicit content globally.

### Enable AI Search

`enable_ai_search` → `ENABLE_AI_SEARCH`

Enable Gemini-backed AI search when configured.

### Enable Streaming Catalogs

`enable_streaming_catalogs` → `ENABLE_STREAMING_CATALOGS`

Offer streaming service catalog sources.

### Advanced: Additional Environment Variables (JSON)

Only use `environment_overrides_json` for variables not listed above. Enter a valid JSON object such as `{"EXAMPLE_VARIABLE":"value"}`. Keep `{}` otherwise. Do not put keys or passwords in Git.

## Backups and upgrades

Use the built-in Home Assistant backup functionality before upgrades; database settings and encryption keys must be preserved on migration.

## Upstream reference

<https://github.com/cedya77/aiometadata/blob/dev/docs/ENVIRONMENT_VARIABLES.md>
