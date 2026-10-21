#!/bin/sh
set -eu
cd /srv/my-lists
mkdir -p /data
if [ ! -f /data/.initialized ]; then
  # Initialize D1, using the SAME persistence root as the long-running worker.
  ./node_modules/.bin/wrangler d1 execute my-lists-db --local --config upstream/wrangler.toml --persist-to /data --file /srv/my-lists/upstream/schema.sql
  touch /data/.initialized
fi
# HA options are optional outside Supervisor (for local Docker testing).
if [ -f /data/options.json ]; then
  node - <<'NODE'
const fs=require('fs'); const o=JSON.parse(fs.readFileSync('/data/options.json','utf8'));
for(const [k,v] of Object.entries({ADMIN_KEY:o.admin_key,TMDB_API_KEY:o.tmdb_api_key,PUBLIC_URL:o.public_url})) {
 if(typeof v==='string' && v) fs.appendFileSync('/tmp/mylists_env',`${k}=${JSON.stringify(v)}\n`);
}
NODE
fi
# Wrangler reads vars from .dev.vars for local development; file never enters the image.
node - <<'NODE'
const fs=require('fs');let env={};
if(fs.existsSync('/data/options.json')){
 const o=JSON.parse(fs.readFileSync('/data/options.json','utf8'));
 env={ADMIN_KEY:o.admin_key||'',TMDB_API_KEY:o.tmdb_api_key||'',PUBLIC_URL:o.public_url||''};
}
fs.writeFileSync('upstream/.dev.vars',Object.entries(env).filter(([,v])=>v).map(([k,v])=>`${k}=${JSON.stringify(v)}`).join('\n')+'\n',{mode:0o600});
NODE
# Expose only the authenticated gateway. Wrangler stays on loopback.
if [ -f /data/options.json ]; then
  ADMIN_KEY=$(node -e 'const o=require("/data/options.json"); process.stdout.write(o.admin_key||"")')
  export ADMIN_KEY
fi
node /srv/my-lists/private_gateway.js &
GATEWAY_PID=$!
cleanup() { kill "$GATEWAY_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
./node_modules/.bin/wrangler dev --config upstream/wrangler.toml --ip 127.0.0.1 --port 8788 --persist-to /data --show-interactive-dev-session false &
WORKER_PID=$!
wait "$WORKER_PID"
