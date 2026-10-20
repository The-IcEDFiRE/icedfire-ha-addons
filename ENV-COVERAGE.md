# Environment-variable coverage and upstream changes

This repository does not claim that all three upstream services have a fixed, finite list of environment variables. Upstream versions evolve.

AIOStreams: use the **Review AIOStreams environment variables** workflow to fetch the current official generated reference and open a reviewable PR adding newly documented fields to `config.yaml`, `launcher.json`, and `translations/en.yaml`. It runs weekly and can be invoked manually. The current package includes an additional set of important AIOStreams settings and the legacy `ADDON_PASSWORD` option; whether that particular setting is recognized depends on your installed version.

The automated scanner deliberately excludes variables like `PORT` that conflict with the fixed Home Assistant port mapping, and must be reviewed before merging because upstream data types sometimes need explicit validation and custom handling.

AIOMetadata and AIOManager need separate audits against their current upstream source code/documentation; this workflow does not claim to cover them automatically.
