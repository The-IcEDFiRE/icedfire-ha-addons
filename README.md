# IcEDFiRE HA Addons

Home Assistant app repository: **AIOStreams**, **AIOMetadata**, **AIOManager**.

Repository URL: `https://github.com/The-IcEDFiRE/icedfire-ha-addons`

## Publishing

1. Upload these files to the existing renamed repository on the `main` branch.
2. GitHub Settings → Actions → General: enable workflow read/write permissions and allow Actions to create commits.
3. Actions → **Check upstream images and publish apps** → Run workflow. It builds amd64 and arm64 manifests and publishes three GHCR packages.
4. Make each GHCR package public (GitHub profile → Packages → package settings).
5. Wait for the workflow to commit version strings to `config.yaml`, then add this repository through Settings → Apps → App store → Repositories.
6. Test manual installation and cold backup/restore before enabling HAOS app auto-updates.

The workflow checks upstream multi-architecture image digests every 6 hours; GitHub may delay scheduled workflows. On changes, it publishes a tagged image first, then bumps that app's `version` in Git. HAOS will discover a new version on its own store polling schedule; enabling automatic updates in Home Assistant is **a separate UI action**.

### First-run safety

The initial `0.0.0` version is a placeholder. **Run the publishing workflow before installing anything**. The upstream containers are not shipped with prebuilt images in this ZIP. All three runtime integrations need validation on a real HAOS host.

### Configuration

Important environment fields appear in the HAOS UI; remaining upstream environment variables can be specified as JSON in `environment_overrides_json`. These are values passed to the containers, not automatic dashboard settings. They are saved as HA app options and included in app backups. Never put secrets in version-controlled config files.

### Data and dependencies

- AIOStreams: `/app/data`, port 3000, requires stable `SECRET_KEY`.
- AIOMetadata: `/app/addon/data`, port 3232; may require TMDB API credentials. Redis is external/optional depending on desired features; not bundled.
- AIOManager: `/app/data`, port 1610; SQLite by default, encryption key can be automatically generated in the persistent data directory.

All apps use `backup: cold`. Note that app options are written within the *same mapped data volume* where upstream persistent files reside; those applications must tolerate the additional `options.json` file.

See [MIGRATION.md](MIGRATION.md) before replacing a live local app.
