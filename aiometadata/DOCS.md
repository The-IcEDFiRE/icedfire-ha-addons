# AIOMetadata

AIOMetadata runs as a managed Home Assistant app in this repository.

## First start

1. Install the app.
2. Open the **Configuration** tab.
3. Configure the API keys and data settings you need.
4. Start the app.
5. Open the UI from the **Info** tab or browse to `http://HOME_ASSISTANT_IP:3232/configure`.

## Configuration fields

### `host_name`
Optional host name or base setting used by the upstream app.

### `tmdb_api_key`
Optional TMDB API key.

### `tvdb_api_key`
Optional TVDB API key.

### `fanart_api_key`
Optional Fanart API key.

### `redis_url`
Optional Redis connection string if you want to use an external Redis service.

### `database_uri`
Database connection string used by the app.

Default:

```text
sqlite://addon/data/db.sqlite
```

### `environment_overrides_json`
Advanced passthrough for additional upstream environment variables.

Example:

```json
{
  "LOG_LEVEL": "debug",
  "NODE_ENV": "production"
}
```

## Storage and backups

- Home Assistant maps private app data to `/app/addon/data`
- Home Assistant options are read from `/app/addon/data/options.json`
- Home Assistant backups are configured as **cold** backups

## Notes

- If you use SQLite, keep backups enabled.
- If you use Redis, manage that dependency separately.
- API keys added through the UI are stored in Home Assistant app options.

## Troubleshooting

- If metadata results are incomplete, verify your API keys.
- If startup fails with a database error, validate the `database_uri`.
- If you use Redis, confirm the connection string is reachable from Home Assistant.

## Upstream project

See the upstream project for full application-level documentation:

<https://github.com/cedya77/aiometadata>
