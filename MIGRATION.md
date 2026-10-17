# Safe migration from `local_aiostreams`

**Do not uninstall the existing local app until you have verified the replacement.** Installing the GitHub repository creates a second app with a different Supervisor slug and **separate** managed data storage.

## Before starting

1. Make a full Home Assistant backup including `local_aiostreams`, its app configuration, and app data. Download an offline copy; check that it contains what you expect.
2. Record the **existing** `SECRET_KEY` (copy securely, do not paste into GitHub) and `BASE_URL` and `AIOSTREAMS_AUTH` if used.
3. Check the existing app database is in persistent storage: the application logs should show `./data/db.sqlite`, and the local app mapping should have `type: data`, `path: /app/data`. This is not sufficient proof by itself—confirm persistence with a restart and locate the actual managed volume before copying.
4. Install the new GitHub-backed app **but do not start it**. Keep its port from conflicting with the current app until migration.
5. Make sure both apps use compatible AIOStreams releases (prefer the same upstream release on first boot to avoid an irreversible database migration). Once the new image runs a newer version, rolling back may not be safe.

## Safely copy your database and files

1. Stop the OLD app and the NEW app before copying. SQLite must be quiescent.
2. From HAOS host-level access (not an ordinary SSH app shell), identify the actual managed data mount paths for *each* app rather than assuming `/addons` or `/local_apps` is the host data path. `docker inspect` of each app container's `Mounts` is one way to establish source and target paths. Some SSH apps isolate the filesystem, so paths differ.
3. Copy the entire contents of the old app's *managed data* directory (not just `db.sqlite`) into the new app's managed data directory, preserving ownership and permissions. Exclude/replace the new app's `options.json`: each HA app has its own configuration, and its options must remain those set via its own UI.
4. Confirm `db.sqlite` is found at the new app's `/app/data/db.sqlite`. If present, include any SQLite `-wal`/`-shm` companion files from the stopped instance and other data files. Do not copy an actively written SQLite database.
5. Set the new app's `secret_key` field to the original key, and configure `base_url` and any operator credentials.
6. Start only the NEW app. Review logs for database migrations, authentication, and server startup; verify several existing user configurations, credentials, and files.
7. Once verified, enable Start on boot and Automatic updates on the NEW app and take a fresh backup. Keep the OLD app stopped for a recovery period; uninstall only after confirming backup/restore readiness.

## Important

- A full restore of an old app backup usually restores the **old app slug**, not the different GitHub repository slug. It is not a reliable cross-slug migration by itself.
- Do not overwrite new `/app/data/options.json` with the old file.
- The Home Assistant SSH terminal may not expose Supervisor host directories. Obtain host-level access or use a controlled method to move data after checking actual mount paths. Avoid guessing filesystem paths or using privileged operations on an unverified mount.
- If exact host mount paths or container names aren't known, ask for output of `docker ps --format '{{.Names}}'` and `docker inspect <container> --format '{{json .Mounts}}'` from the HAOS host rather than using speculative copy commands.
- AIOStreams also supports user-configuration export/import if full server state is unnecessary, but it does not replace a full SQLite/data migration.
