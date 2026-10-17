# AIOManager

AIOManager runs as a managed Home Assistant app in this repository.

## First start

1. Install the app.
2. Open the **Configuration** tab.
3. Set the options you need.
4. Start the app.
5. Open the UI from the **Info** tab or browse to `http://HOME_ASSISTANT_IP:1610/`.

## Configuration fields

### `encryption_key`
Optional but recommended stable encryption key for the upstream application.

### `db_type`
Database backend to use.

Supported values:

- `sqlite`
- `postgres`

### `database_url`
Database connection URL.

If `db_type` is `sqlite`, this may be left blank when the upstream app supplies a safe default.

### `cors_origins`
Optional CORS origins string for browser access control.

### `environment_overrides_json`
Advanced passthrough for additional upstream environment variables.

Example:

```json
{
  "LOG_LEVEL": "debug"
}
```

## Storage and backups

- Home Assistant maps private app data to `/app/data`
- Home Assistant options are read from `/app/data/options.json`
- Home Assistant backups are configured as **cold** backups

## Notes

- Keep your encryption key stable if you expect to preserve existing secured data.
- If you use PostgreSQL, manage the database separately.

## Troubleshooting

- If the app does not start, verify your database settings.
- If browser access fails, check the host port and `cors_origins` setting.
- If advanced environment JSON is used, validate the JSON syntax.

## Upstream project

See the upstream project for full application-level documentation:

<https://github.com/sonicx161/aiomanager>
