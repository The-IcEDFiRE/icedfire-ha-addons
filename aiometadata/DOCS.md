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


## Redis version compatibility

AIOMetadata 3.5.1 and newer requires Redis 8.0+ for the `HSETEX` command. This repository builds Redis from the `redis:8.2-bookworm` upstream image. Before upgrading existing Redis data from 7.x, take a cold backup and verify the restore plan; do not assume you can downgrade data files to Redis 7.x afterward.

## Additional configuration fields

The settings below map directly to upstream environment variables. Leave optional settings blank to use upstream defaults. Boolean options that are unset are not exported.

### Add-on Password

`addon_password` → `ADDON_PASSWORD`

Optional password for protected addon endpoints. Different from the administrator API key.

### Disable Metrics

`disable_metrics` → `DISABLE_METRICS`

Disable dashboard telemetry and metrics collection.

### Dashboard Metadata Language

`dashboard_metadata_language` → `DASHBOARD_METADATA_LANGUAGE`

Preferred language code for titles shown in dashboard content, such as en.

### Manifest Logo URL

`addon_logo_url` → `ADDON_LOGO_URL`

Override the logo image URL advertised in the addon manifest.

### Enable HTTP Compression

`response_compression_enabled` → `RESPONSE_COMPRESSION_ENABLED`

Compress compatible HTTP responses using gzip or Brotli.

### Background Catalog Refresh

`catalog_refresh_ahead_enabled` → `CATALOG_REFRESH_AHEAD_ENABLED`

Refresh expiring catalog entries before users request them.

### Catalog Refresh Window

`catalog_refresh_ahead_fraction` → `CATALOG_REFRESH_AHEAD_FRACTION`

Fraction of cache lifetime used for background catalog refresh; e.g. 0.1.

### Fanart Project API Key

`fanart_api_project_key` → `FANART_API_PROJECT_KEY`

Project client key for Fanart.tv image requests.

### MDBList API Key (Public)

`mdblist_api_key` → `MDBLIST_API_KEY`

Publicly exposed default MDBList key; prefer a private built-in key for shared instances.

### Gemini API Key (Public)

`gemini_api_key` → `GEMINI_API_KEY`

Publicly exposed Gemini key; use a private built-in key for shared instances.

### Simkl Client ID

`simkl_client_id` → `SIMKL_CLIENT_ID`

OAuth application identifier for Simkl integrations.

### Simkl Client Secret

`simkl_client_secret` → `SIMKL_CLIENT_SECRET`

Secret for Simkl browser redirect OAuth flow.

### Simkl Authorization Mode

`simkl_auth_mode` → `SIMKL_AUTH_MODE`

Choose OAuth browser login, device PIN authorization, or both.

### Simkl Redirect URL

`simkl_redirect_uri` → `SIMKL_REDIRECT_URI`

OAuth callback URL registered with your Simkl application.

### Simkl Activity Cache (Seconds)

`simkl_activities_ttl` → `SIMKL_ACTIVITIES_TTL`

How long activity status stays cached; upstream example is 1800 seconds.

### Anime API Base URL

`jikan_api_base` → `JIKAN_API_BASE`

Base URL for the Jikan-compatible anime metadata API.

### Enable Anime Metadata API

`jikan_enabled` → `JIKAN_ENABLED`

Enable MyAnimeList catalogs, search and metadata via the Jikan-compatible provider.

### Anime Results Per Page

`mal_page_size` → `MAL_PAGE_SIZE`

Maximum number of titles per MyAnimeList catalog page.

### AniList Client ID

`anilist_client_id` → `ANILIST_CLIENT_ID`

OAuth application ID for AniList watch-tracking integration.

### AniList Client Secret

`anilist_client_secret` → `ANILIST_CLIENT_SECRET`

OAuth application secret for AniList.

### AniList Redirect URL

`anilist_redirect_uri` → `ANILIST_REDIRECT_URI`

OAuth redirect URL registered with AniList.

### MyAnimeList Client ID

`mal_client_id` → `MAL_CLIENT_ID`

OAuth application identifier for MyAnimeList tracking.

### MyAnimeList Client Secret

`mal_client_secret` → `MAL_CLIENT_SECRET`

OAuth application secret for MyAnimeList.

### MyAnimeList Redirect URL

`mal_redirect_uri` → `MAL_REDIRECT_URI`

OAuth callback URL registered with MyAnimeList.

### Trakt Client ID

`trakt_client_id` → `TRAKT_CLIENT_ID`

OAuth application identifier for Trakt integration.

### Trakt Client Secret

`trakt_client_secret` → `TRAKT_CLIENT_SECRET`

OAuth secret for Trakt integration.

### Trakt Redirect URL

`trakt_redirect_uri` → `TRAKT_REDIRECT_URI`

OAuth callback URL registered with Trakt.

### Disable Trakt Search

`disable_trakt_search` → `DISABLE_TRAKT_SEARCH`

Disable Trakt as an available search provider.

### Trakt Concurrent Requests

`trakt_concurrency` → `TRAKT_CONCURRENCY`

Maximum simultaneous Trakt requests.

### Metadata Fetch Concurrency

`meta_concurrency` → `META_CONCURRENCY`

Maximum simultaneous getMeta operations per catalog request.

### Memory Logging Interval (Minutes)

`heap_log_interval_min` → `HEAP_LOG_INTERVAL_MIN`

Periodically log memory usage; zero or unset disables.

### Artwork Download Timeout (ms)

`poster_proxy_timeout_ms` → `POSTER_PROXY_TIMEOUT_MS`

Timeout for upstream poster and background image fetches.

### Use Smaller TMDB Logos

`prefer_smaller_logos_tmdb` → `PREFER_SMALLER_LOGOS_TMDB`

Reduce logo download dimensions and storage.

### Use Smaller TMDB Backdrops

`prefer_smaller_backdrops_tmdb` → `PREFER_SMALLER_BACKDROPS_TMDB`

Prefer smaller TMDB backgrounds to save bandwidth.

### Use Smaller TMDB Landscape Art

`prefer_smaller_landscape_tmdb` → `PREFER_SMALLER_LANDSCAPE_TMDB`

Prefer smaller landscape images.

### Use Smaller TMDB Posters

`prefer_smaller_posters_tmdb` → `PREFER_SMALLER_POSTERS_TMDB`

Prefer smaller TMDB poster renditions.

### Enable Built-in Artwork Cache

`enable_builtin_poster_cache` → `ENABLE_BUILTIN_POSTER_CACHE`

Cache artwork on disk using the application data directory.

### Cache Background Images

`poster_cache_backgrounds` → `POSTER_CACHE_BACKGROUNDS`

Include backgrounds in the built-in disk artwork cache.

### Cache Landscape Posters

`poster_cache_landscape_posters` → `POSTER_CACHE_LANDSCAPE_POSTERS`

Include landscape artwork in the built-in disk cache.

### Cache Logos

`poster_cache_logos` → `POSTER_CACHE_LOGOS`

Include logos in the built-in disk cache.

### Cache Episode Thumbnails

`poster_cache_thumbnails` → `POSTER_CACHE_THUMBNAILS`

Include episode thumbnails; may consume substantial disk space.

### Cache Processed Images

`poster_cache_processed_images` → `POSTER_CACHE_PROCESSED_IMAGES`

Store generated or transformed artwork in the cache.

### Allow Private Artwork URLs

`poster_proxy_allow_private` → `POSTER_PROXY_ALLOW_PRIVATE`

Allow signed artwork URLs to access private network addresses. Disable on public multi-user instances.

### Private Artwork Host Allowlist

`poster_cache_allowed_hosts` → `POSTER_CACHE_ALLOWED_HOSTS`

Comma-separated private hosts permitted for artwork requests.

### Artwork Cache Disk Limit

`poster_cache_max_size` → `POSTER_CACHE_MAX_SIZE`

Maximum disk space for artwork cache, such as 10g.

### Artwork Cache Memory Limit

`poster_cache_memory_size` → `POSTER_CACHE_MEMORY_SIZE`

Memory reserved for hot artwork, such as 128m.

### Artwork Cache Lifetime (Days)

`poster_cache_ttl_days` → `POSTER_CACHE_TTL_DAYS`

How long cached images remain fresh before revalidation.

### Use Upstream Artwork Cache Headers

`poster_cache_infer_ttl` → `POSTER_CACHE_INFER_TTL`

Respect artwork providers cache-control headers where possible.

### Artwork Cache Directory

`poster_cache_dir` → `POSTER_CACHE_DIR`

Override disk cache path; keep under the managed data folder for backup.

### Concurrent Artwork Downloads

`poster_cache_fetch_concurrency` → `POSTER_CACHE_FETCH_CONCURRENCY`

Maximum simultaneous image downloads.

### Maximum Cached Artwork Size

`poster_cache_max_object_bytes` → `POSTER_CACHE_MAX_OBJECT_BYTES`

Skip caching oversized individual assets, e.g. 20m.

### Remove Unused Art After (Days)

`poster_cache_inactive_days` → `POSTER_CACHE_INACTIVE_DAYS`

Evict cached images that have not been requested recently.

### Client Artwork Cache (Days)

`poster_proxy_max_age_days` → `POSTER_PROXY_MAX_AGE_DAYS`

Maximum browser/player cache age for proxied artwork.

### Log Artwork Cache Requests

`poster_cache_log_requests` → `POSTER_CACHE_LOG_REQUESTS`

Log individual artwork cache requests for diagnostics.

### Metadata Disk Store Budget

`meta_cold_store_max_bytes` → `META_COLD_STORE_MAX_BYTES`

Storage budget for the separate metadata SQLite cache, e.g. 2gb.

### Compress Metadata Disk Store

`meta_cold_store_compression` → `META_COLD_STORE_COMPRESSION`

Use LZ4 compression for stored metadata cache entries.


For the latest full upstream variable reference, see [AIOMetadata environment variables](https://github.com/cedya77/aiometadata/blob/dev/docs/ENVIRONMENT_VARIABLES.md).
