# AIOMetadata configuration expansion

This revision adds **ADDON_PASSWORD** and 55 additional individually configurable AIOMetadata options.

Existing Home Assistant option names remain unchanged. Newly added fields are optional and unset by default.

New fields have individual English labels and help text, mapped to the environment variables in `launcher.json`. The JSON override remains the final fallback field.

Source: https://github.com/cedya77/aiometadata/blob/dev/.env.example

**Important:** Review secrets and take a backup before updating; these changes were syntax-validated but not tested by starting the container on HAOS.
