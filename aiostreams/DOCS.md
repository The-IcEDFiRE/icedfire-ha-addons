# AIOStreams

AIOStreams runs as a managed Home Assistant app in this repository.

## First start

1. Install the app.
2. Open the **Configuration** tab.
3. Set at least:
   - `base_url`
   - `secret_key`
4. Optionally configure authentication:
   - `aiostreams_auth`
   - `aiostreams_auth_permissions`
5. Start the app.
6. Open the web UI from the **Info** tab or browse to `http://HOME_ASSISTANT_IP:3000/stremio/configure`.

## Configuration options

Labels and help text also appear in the Home Assistant Configuration tab. Optional fields left unset use the upstream defaults.

### Public Base URL

`base_url` → `BASE_URL`

Full URL used in manifest and configuration links. Example: https://streams.example.com.

### Encryption Secret Key

`secret_key` → `SECRET_KEY`

Required 64-character hexadecimal key. Keep the same key when restoring or migrating.

### Operator Login Credentials

`aiostreams_auth` → `AIOSTREAMS_AUTH`

Comma-separated username:password pairs for dashboard/operator access.

### Operator Permissions

`aiostreams_auth_permissions` → `AIOSTREAMS_AUTH_PERMISSIONS`

Per-user permissions, e.g. alice=admin,bob=proxy|service|createConfig.

### Database Connection URL

`database_uri` → `DATABASE_URI`

Optional SQLite or PostgreSQL connection. Leave blank to use the persistent SQLite default.

### Database Connection Pool Size

`database_pool_size` → `DATABASE_POOL_SIZE`

Maximum PostgreSQL connections; not needed for SQLite.

### Redis Connection URL

`redis_uri` → `REDIS_URI`

Optional shared-cache Redis URI; leave blank for a single instance.

### Redis Connection Timeout (ms)

`redis_timeout` → `REDIS_TIMEOUT`

Maximum time to wait for a Redis connection.

### Settings Refresh Interval (seconds)

`settings_refresh_interval` → `SETTINGS_REFRESH_INTERVAL`

How often to refresh changes made on another instance. Usually unnecessary to change for one instance.

### Internal Service URL

`internal_url` → `INTERNAL_URL`

Override internal URL used by built-in add-ons; the default normally works.

### Disk Cache Directory

`disk_cache_dir` → `DISK_CACHE_DIR`

Override cache location. Use a persistent or deliberately disposable location.

### Log Memory Limit (bytes)

`log_buffer_max_bytes` → `LOG_BUFFER_MAX_BYTES`

Maximum memory used for recent dashboard log lines.

### Maximum Saved Log Entries

`log_buffer_max_entries` → `LOG_BUFFER_MAX_ENTRIES`

Maximum number of recent dashboard log lines kept in memory.

### Application Mode

`node_env` → `NODE_ENV`

Normally leave blank (production). Development/test are for troubleshooting.

### Allow Dashboard Process Controls

`system_lifecycle_enabled` → `SYSTEM_LIFECYCLE_ENABLED`

Allow dashboard System page to restart or stop the AIOStreams process.

### Logging Detail

`log_level` → `LOG_LEVEL`

Optional override. Configuring runtime options here makes them read-only in AIOStreams dashboard.

### Log Output Format

`log_format` → `LOG_FORMAT`

Optional runtime override. JSON is suitable for log collectors.

### Require Login for Configuration

`auth_required` → `AIOSTREAMS_AUTH_REQUIRED`

Lock the configure page behind operator login. Overrides the dashboard setting.

### Allow Private Network URLs

`allow_private_urls` → `ALLOW_PRIVATE_URLS`

Permit requests to LAN and loopback addresses. Disable for public multi-user deployments; locks dashboard setting.

### Default Provider Timeout (ms)

`default_timeout` → `DEFAULT_TIMEOUT`

Fallback timeout for fetching streams from providers; locks dashboard setting.

### Advanced: Additional Environment Variables (JSON)

Only use `environment_overrides_json` for variables not listed above. Enter a valid JSON object such as `{"EXAMPLE_VARIABLE":"value"}`. Keep `{}` otherwise. Do not put keys or passwords in Git.

## Backups and upgrades

Use the built-in Home Assistant backup functionality before upgrades; database settings and encryption keys must be preserved on migration.

## Upstream reference

<https://docs.aiostreams.viren070.me/configuration/environment-variables/>
