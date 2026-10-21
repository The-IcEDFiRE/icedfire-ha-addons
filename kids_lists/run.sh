#!/bin/sh
set -eu
if [ -f /data/options.json ]; then
  export ADMIN_PASSWORD="$(python3 -c 'import json;print(json.load(open("/data/options.json")).get("admin_password",""))')"
  export TMDB_API_KEY="$(python3 -c 'import json;print(json.load(open("/data/options.json")).get("tmdb_api_key",""))')"
fi
exec python3 -u /opt/kids-lists/app.py
