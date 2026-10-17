# AIOStreams Home Assistant app

Enter your `base_url` and **existing** `secret_key` (64 hexadecimal characters) in the Configuration tab. Additional bootstrap fields are optional. To set *any* other official AIOStreams environment variable, add it to `environment_overrides_json` as JSON, e.g. `{"LOG_LEVEL":"debug","AIOSTREAMS_AUTH_REQUIRED":true}`. Use strings for comma-separated lists or JSON-array settings when required by upstream.

Only set runtime variables if you want to **lock** them: upstream marks environment-overridden runtime settings read-only in the AIOStreams dashboard. Leave unneeded fields empty.

`PORT` is fixed to 3000 inside the image; use the HA port mapping to change the host-side port. Keep the `SECRET_KEY` stable through migrations. Generic override JSON is not secret-masked. See the root README for details and migration instructions.
