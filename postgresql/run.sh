#!/bin/sh
set -eu
opts=/data/options.json
if [ ! -f "$opts" ]; then echo "Missing Home Assistant options: $opts" >&2; exit 1; fi
export POSTGRES_USER="$(jq -r '.username // "aio"' "$opts")"
export POSTGRES_DB="$(jq -r '.database // "aio"' "$opts")"
export POSTGRES_PASSWORD="$(jq -r '.password // ""' "$opts")"
[ -n "$POSTGRES_PASSWORD" ] || { echo 'Set PostgreSQL password before starting' >&2; exit 1; }
# Place database cluster in a subdirectory; /data also contains Supervisor options.json.
export PGDATA=/data/pgdata
connections=$(jq -r '.max_connections // 100' "$opts")
buffers=$(jq -r '.shared_buffers_mb // 128' "$opts")
case "$connections:$buffers" in *[!0-9:]* ) echo 'Invalid PostgreSQL tuning values' >&2; exit 1;; esac
# Password is only applied when the database is initialized, not changed after creation.
exec docker-entrypoint.sh postgres -c "max_connections=$connections" -c "shared_buffers=${buffers}MB" -c 'password_encryption=scram-sha-256'
