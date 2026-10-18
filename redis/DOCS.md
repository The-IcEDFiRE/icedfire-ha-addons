# IcEDFiRE Redis — Configuration and Connections

This optional service supplies Redis caching to apps that support a Redis URL. It is not required for every AIO app.

## Setup

1. Install the Redis app; enter a **strong unique password** on the Configuration tab.
2. Leave the host port mapping **disabled** unless you have a specific reason to connect from outside HAOS.
3. Start the app and confirm there are no startup errors.
4. Open **Settings → Apps → Redis → Info** and use the actual **Hostname** shown for this installed app in client URLs. The hostname may vary by repository installation; **do not assume `redis`**.

Example client URL (replace hostname and password):

```text
redis://:YOUR_URL_ENCODED_PASSWORD@ACTUAL_REDIS_APP_HOSTNAME:6379/0
```

In the AIO app Configuration tab, paste that URL in **Redis Connection URL** (`redis_uri`, `redis_url`, etc., depending on the app). Set this only for apps that support Redis.

## Settings

- **Redis Password**: required, used by clients to authenticate. Use a URL-encoded password when embedding it in a URL.
- **Append-Only Persistence**: recommended when Redis holds important state, not just disposable cache.
- **Memory Limit**: optional Redis application memory cap. Set this carefully relative to HAOS RAM.
- **Eviction Policy**: selects behavior at the memory cap. `noeviction` avoids silently dropping state.
- **Snapshot Interval / Changes**: RDB snapshot trigger; AOF and snapshots can coexist.

## Backups

The complete Redis `/data` directory is under the Home Assistant private app storage mount and included in **cold** app backups. Redis credentials are backed up as app options. Back up the AIO apps separately as well; backing up Redis alone does not back up their data.

## Notes

Redis is **not** exposed through Home Assistant's MQTT/MySQL service discovery. Connection details must be entered explicitly in consumer apps. Be cautious with authentication changes: existing clients stop working until updated.

Official Redis documentation: <https://redis.io/docs/latest/>
