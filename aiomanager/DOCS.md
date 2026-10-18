# AIOManager

AIOManager runs as a managed Home Assistant app in this repository.

## First start

1. Install the app.
2. Open the **Configuration** tab.
3. Set the options you need.
4. Start the app.
5. Open the UI from the **Info** tab or browse to `http://HOME_ASSISTANT_IP:1610/`.

## Configuration options

Labels and help text also appear in the Home Assistant Configuration tab. Optional fields left unset use the upstream defaults.

### Encryption Key

`encryption_key` → `ENCRYPTION_KEY`

Optional stable secret for encrypted data; when blank the upstream app generates a persistent key.

### Database Type

`db_type` → `DB_TYPE`

Use SQLite for a standalone install; PostgreSQL for an external database.

### PostgreSQL Connection URL

`database_url` → `DATABASE_URL`

Required when Database Type is postgres; ignored with SQLite.

### Allowed Browser Origins

`cors_origins` → `CORS_ORIGINS`

Comma-separated allowed origins, e.g. https://manager.example.com.

### Application Mode

`node_env` → `NODE_ENV`

Optional runtime mode; production is the normal default.

### Verify Database TLS Certificate

`db_ssl_reject_unauthorized` → `DB_SSL_REJECT_UNAUTHORIZED`

Verify the PostgreSQL server certificate (recommended when a trusted CA is configured).

### Database Pool Size

`db_pool_size` → `DB_POOL_SIZE`

Number of PostgreSQL connections; ignored with SQLite.

### Database Connection Timeout (ms)

`db_connection_timeout` → `DB_CONNECTION_TIMEOUT`

Time to wait for a PostgreSQL pool connection.

### Database Startup Retries

`db_max_retries` → `DB_MAX_RETRIES`

Number of PostgreSQL connection retries during startup.

### Read-only Replica Mode

`read_only_replica` → `READ_ONLY_REPLICA`

Run as PostgreSQL standby without background writes. Advanced only.

### Allow Fetching Private URLs

`ssrf_allow_private` → `SSRF_ALLOW_PRIVATE`

Allow metadata proxy access to private LAN addresses; only for trusted local setups.

### Trust Reverse Proxy Headers

`trust_proxy` → `TRUST_PROXY`

Use real client IP from trusted reverse proxy headers. Ensure your proxy replaces these headers.

### Close New Registrations

`registrations_closed` → `REGISTRATIONS_CLOSED`

Prevent new account signups while allowing existing users to sign in.

### Unified Enforcement Checks

`unified_enforcement` → `UNIFIED_ENFORCEMENT`

Advanced consistency checks across server modules.

### Logging Detail

`log_level` → `LOG_LEVEL`

Verbosity of application logs.

### Human-readable Logs

`log_pretty_print` → `LOG_PRETTY_PRINT`

Use pretty output rather than JSON log lines.

### Maximum Sync Payload Size (bytes)

`max_sync_payload_size` → `MAX_SYNC_PAYLOAD_SIZE`

Maximum encrypted sync-state payload accepted by the API.

### Proxy Concurrent Request Limit

`proxy_concurrency_limit` → `PROXY_CONCURRENCY_LIMIT`

Maximum simultaneous outbound proxy/metadata requests.

### Image Proxy Timeout (ms)

`image_proxy_timeout_ms` → `IMAGE_PROXY_TIMEOUT_MS`

Maximum time for poster and image proxy requests.

### Image Cache Lifetime (ms)

`image_cache_ttl_ms` → `IMAGE_CACHE_TTL_MS`

How long shared in-memory poster cache entries remain valid.

### Enable Activity Engine

`activity_engine_enabled` → `ACTIVITY_ENGINE_ENABLED`

Enable background activity polling; resource-intensive on shared instances.

### Activity Scan Interval (ms)

`activity_scan_interval_ms` → `ACTIVITY_SCAN_INTERVAL_MS`

Time between background activity scans.

### Advanced: Additional Environment Variables (JSON)

Only use `environment_overrides_json` for variables not listed above. Enter a valid JSON object such as `{"EXAMPLE_VARIABLE":"value"}`. Keep `{}` otherwise. Do not put keys or passwords in Git.

## Backups and upgrades

Use the built-in Home Assistant backup functionality before upgrades; database settings and encryption keys must be preserved on migration.

## Upstream reference

<https://github.com/Sonicx161/AIOManager/blob/main/.env.example>
