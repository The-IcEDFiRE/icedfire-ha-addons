import { readFileSync } from 'node:fs';

// The app data mapping intentionally mounts Supervisor's /data at /app/data
// so AIOStreams' default ./data/db.sqlite remains in backed-up storage.
const optionsPath = '/app/data/options.json';
let options;
try {
  options = JSON.parse(readFileSync(optionsPath, 'utf8'));
} catch (error) {
  console.error(`Cannot read Home Assistant app options at ${optionsPath}: ${error.message}`);
  process.exit(1);
}

if (!options.base_url) {
  console.error('Missing base_url in Home Assistant app Configuration.');
  process.exit(1);
}
if (!/^[a-f\d]{64}$/i.test(options.secret_key ?? '')) {
  console.error('secret_key must be a 64-character hexadecimal string in app Configuration.');
  process.exit(1);
}

process.env.BASE_URL = options.base_url;
process.env.SECRET_KEY = options.secret_key;
if (options.operator_auth) {
  process.env.AIOSTREAMS_AUTH = options.operator_auth;
} else {
  delete process.env.AIOSTREAMS_AUTH;
}
if (options.log_level) {
  process.env.LOG_LEVEL = options.log_level;
}

// Keep the official image's server entrypoint in use; no shell or extra packages.
await import('/app/packages/server/dist/server.js');
