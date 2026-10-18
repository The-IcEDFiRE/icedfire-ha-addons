# IcEDFiRE PostgreSQL — Configuration and Connections

This optional service provides PostgreSQL to AIO applications that explicitly support PostgreSQL databases. It is **not** a drop-in replacement for every SQLite setting.

## Setup

1. Install the PostgreSQL app.
2. In **Configuration**, set a strong **Initial Database Password**, plus your initial database and username.
3. Leave the host port mapping **disabled**, keeping database access inside Home Assistant's app network.
4. Start PostgreSQL. On first start, it creates a new cluster under `/data/pgdata`.
5. Find the actual **Hostname** on the app Info page or with `ha apps info` for the installed slug.
6. Enter the database connection URI into the AIO app's database field (only if that app supports PostgreSQL).

Example URI (replace host, user, password and DB; URL-encode special password characters):

```text
postgresql://aio:YOUR_URL_ENCODED_PASSWORD@ACTUAL_POSTGRESQL_APP_HOSTNAME:5432/aio
```

### Multiple applications

For better separation, create a **different database and non-superuser role for each app**. The initial `username` is a privileged bootstrap account; do not share it between all apps in production. Use a SQL client against the internal hostname or a temporary, carefully protected administration connection to create accounts. Home Assistant does not automatically provision databases for your other apps.

## Configuration fields

- **Initial Database Name / User / Password**: applied **on first initialization only**. Changing these fields later will not rename the existing database/user or rotate the stored database password.
- **Maximum Connections**: PostgreSQL connection limit.
- **Shared Buffer Size**: memory allocated to shared buffers; increase only if sufficient RAM is available.

## Persistent data and upgrades

- Database files are stored at `/data/pgdata`, in HA-managed persistent app storage.
- This wrapper pins **PostgreSQL 17**, so regular image refreshes won't silently upgrade to PostgreSQL 18 or change on-disk major-version format.
- **Never replace this wrapper with PostgreSQL 18/19 against the same cluster without an explicit major-version migration.**
- A **cold Home Assistant app backup** stops PostgreSQL while data is copied; test restoring backups separately before enabling unattended upgrades.

Official PostgreSQL docs: <https://www.postgresql.org/docs/17/>
