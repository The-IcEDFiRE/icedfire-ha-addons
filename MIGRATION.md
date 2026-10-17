# Safe migration from `local_aiostreams`

Home Assistant identifies apps by repository ID and slug; the repository-hosted AIOStreams app **is a different app** from `local_aiostreams` with separate data. Do **not** uninstall the local instance to migrate.

1. Confirm the current local app's data mount and make a *full Home Assistant backup* that includes it. Confirm the backup completes and can be retrieved.
2. Record existing `BASE_URL`, `AIOSTREAMS_AUTH`, other options, and most importantly the existing `SECRET_KEY` in a secure place. Never paste keys into GitHub.
3. Stop the old local AIOStreams app. Avoid concurrent writes to the SQLite database.
4. Identify its **actual managed data directory**. For the existing wrapper using `map: {type: data, path: /app/data}`, database files such as `db.sqlite` reside under `/app/data` *inside that container*. Don't guess the HAOS host path.
5. Install the new repository app, configure the **same SECRET_KEY** and identical credentials, but don't start it yet. The old and new apps both expose host port 3000.
6. Transfer the entire old persistent data directory (including database sidecars, if any) to the new app's private data directory using a trusted backup/restore approach or a supervised temporary copy. **Do not copy the old `/options.json` over the new instance's options file.** Create a fresh backup before replacing target files.
7. Start the repository app and verify the account list, providers, profiles, and data survive a restart. Take another full backup.
8. Only after verification, disable the old app's autostart; leave it uninstalled until you are certain.
9. Enable automatic updates for the new repo app in the Home Assistant UI **after one manual update and backup-restore test**.

**Why no single copy command?** HAOS host filesystem paths depend on the Supervisor version and terminal app mount access. A blind `cp` can silently copy the wrong data or overwrite the live database. Verify actual paths before selecting a command.
