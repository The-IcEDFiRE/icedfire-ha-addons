# IcEDFiRE HA Addons

Community-maintained **Home Assistant apps** for the AIO ecosystem.

This repository currently provides five independently installable apps:

- **AIOStreams** — streaming add-on wrapper for Home Assistant
- **AIOMetadata** — metadata add-on wrapper for Home Assistant
- **AIOManager** — management add-on wrapper for Home Assistant
- **Redis** — optional private Redis service
- **PostgreSQL** — optional private PostgreSQL 17 database

These are **community wrappers** around upstream containers. They are not official Home Assistant packages from the upstream project authors.

## Features

- Native Home Assistant app installation
- Managed backups with Home Assistant
- `amd64` and `aarch64` builds
- Published to GitHub Container Registry (GHCR)
- Automatic upstream monitoring with GitHub Actions
- Per-app configuration through the Home Assistant UI

## Installation

1. In Home Assistant, open **Settings → Apps → App Store**.
2. Add this repository URL:

   `https://github.com/The-IcEDFiRE/icedfire-ha-addons`

3. Refresh the store.
4. Install the app you want.
5. Open the app's **Documentation** tab for setup help and configuration details.

## Included apps

| App | Default Port | Upstream Image |
| --- | --- | --- |
| AIOStreams | `3000` | `ghcr.io/viren070/aiostreams:latest` |
| AIOMetadata | `3232` | `ghcr.io/cedya77/aiometadata:latest` |
| AIOManager | `1610` | `ghcr.io/sonicx161/aiomanager:latest` |
| Redis | Internal `6379` (not exposed by default) | `redis:7.4-bookworm` |
| PostgreSQL | Internal `5432` (not exposed by default) | `postgres:17-bookworm` |

## Automatic updates

GitHub Actions checks the upstream images on a schedule. When an upstream image changes, this repository:

1. rebuilds the corresponding Home Assistant wrapper image,
2. publishes it to GHCR, and
3. updates the app version so Home Assistant can detect a new release.

You can then either update manually from Home Assistant or enable automatic updates.

## Important notes

- Keep your existing encryption/authentication secrets when migrating an existing installation.
- Review the **Documentation** tab before changing advanced variables.
- `environment_overrides_json` is intended for advanced users who want to pass additional upstream environment variables.
- These wrappers should be tested after install and after restore before relying on unattended updates.

## Credits

- Upstream AIOStreams: `viren070`
- Upstream AIOMetadata: `cedya77`
- Upstream AIOManager: `sonicx161`

## Support

For issues with the Home Assistant wrappers, use this repository.
For application-specific issues, also check the upstream project documentation and issue tracker.

## Optional infrastructure services

Redis and PostgreSQL are separate Home Assistant apps, **not automatically installed as dependencies**. Install them only if one of your AIO apps needs them. Both run on the HAOS internal app network, require authentication, use cold app backups and have their host ports **disabled by default**.

The internal hostname is specific to the app installation; find it in the installed app information. Home Assistant built-in service discovery does **not** register Redis or PostgreSQL as supported service types. See [Redis documentation](redis/DOCS.md) and [PostgreSQL documentation](postgresql/DOCS.md) for complete connection examples.

**Important:** PostgreSQL 17 is deliberately major-version pinned. Backups and upgrades require more caution than ordinary stateless applications. Redis and PostgreSQL builds have not yet been tested on HAOS; validate before enabling automatic upgrades.

## Independent app releases

Changes to one app no longer rebuild all five images. See [Selective updates](SELECTIVE-UPDATES.md) for the update rules and how to force a single-app build.
