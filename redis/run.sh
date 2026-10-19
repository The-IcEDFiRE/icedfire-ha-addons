#!/bin/sh
set -eu
opts=/data/options.json
if [ ! -f "$opts" ]; then echo "Missing Home Assistant options: $opts" >&2; exit 1; fi
password=$(jq -r '.password // ""' "$opts")
[ -n "$password" ] || { echo 'Configure a Redis password in the Home Assistant app settings first' >&2; exit 1; }
append=$(jq -r 'if .append_only == false then "no" else "yes" end' "$opts")
maxmb=$(jq -r '.maxmemory_mb // 0' "$opts")
policy=$(jq -r '.maxmemory_policy // "noeviction"' "$opts")
seconds=$(jq -r '.save_every_seconds // 900' "$opts")
changes=$(jq -r '.save_after_changes // 1' "$opts")
case "$maxmb:$seconds:$changes" in *[!0-9:]* ) echo 'Invalid numeric configuration' >&2; exit 1;; esac
case "$policy" in noeviction|allkeys-lru|allkeys-lfu|volatile-lru|volatile-ttl) ;; *) echo 'Invalid eviction policy' >&2; exit 1;; esac
case "$append" in yes|no) ;; *) echo 'Invalid persistence option' >&2; exit 1;; esac
# Require authentication on internal network, do not publish host port by default.
set -- redis-server --dir /data --port 6379 --protected-mode yes --requirepass "$password" --appendonly "$append" --maxmemory-policy "$policy"
if [ "$maxmb" -gt 0 ]; then set -- "$@" --maxmemory "${maxmb}mb"; fi
if [ "$seconds" -gt 0 ] && [ "$changes" -gt 0 ]; then set -- "$@" --save "$seconds" "$changes"; else set -- "$@" --save ''; fi
exec docker-entrypoint.sh "$@"
