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

## Configuration fields

### `base_url`
Public or local URL used by AIOStreams to build its links.

Example:

```text
http://10.0.0.16:3000
```

If you use a reverse proxy, set it to the final external URL.

### `secret_key`
Required stable secret used by AIOStreams for encryption and secure state.

**Important:** do not change this key on an existing installation unless you are prepared to reconfigure the app.

### `aiostreams_auth`
Optional basic authentication credential configuration for the upstream container.

### `aiostreams_auth_permissions`
Optional permissions string passed through to the upstream app.

### `environment_overrides_json`
Advanced passthrough for additional upstream environment variables.

Example:

```json
{
  "LOG_LEVEL": "debug",
  "LOG_FORMAT": "json"
}
```

Only add keys you intentionally want to override.

## Storage and backups

- Home Assistant maps private app data to `/app/data`
- Home Assistant options are read from `/app/data/options.json`
- Home Assistant backups are configured as **cold** backups

## Migration from an existing installation

When migrating from `local_aiostreams` or another Docker deployment:

1. Stop the old instance.
2. Keep the **same `secret_key`**.
3. Copy the upstream app data into the new persistent data location.
4. Start the new Home Assistant app and verify your configuration.

## Troubleshooting

- If the app starts but the UI is not reachable, verify the host port mapping.
- If existing data cannot be read, confirm you kept the same `secret_key`.
- If you are using advanced variables, check that your JSON is valid.

## Upstream documentation

See the upstream project for full application-level documentation:

<https://docs.aiostreams.viren070.me/>
