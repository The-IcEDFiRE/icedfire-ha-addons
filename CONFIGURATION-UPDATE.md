# Friendlier configuration fields

Each app now has English UI labels and descriptions in `translations/en.yaml`, plus individual settings for common upstream environment variables. `environment_overrides_json` remains available only as an advanced fallback.

Existing option keys remain unchanged. New options are optional and omitted from the container environment until explicitly set, preserving upstream defaults. Some AIOStreams runtime overrides lock corresponding settings in its own dashboard.

To deploy: commit these files, run the repository publishing workflow to build a new app version for each updated app, then update in Home Assistant. Back up existing instances first.

This package was syntax-checked but not container-tested on HAOS.
