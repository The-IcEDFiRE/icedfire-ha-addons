import { readFileSync } from 'node:fs';

// HA app data is mounted at /app/data so AIOStreams SQLite persists there.
const optionsPath = '/app/data/options.json';
let options;
try {
  options = JSON.parse(readFileSync(optionsPath, 'utf8'));
} catch (error) {
  console.error(`Cannot read app settings at ${optionsPath}: ${error.message}`);
  process.exit(1);
}

if (!options.base_url || typeof options.base_url !== 'string') {
  console.error('Missing base_url in Home Assistant app configuration.');
  process.exit(1);
}
if (!/^[a-f\d]{64}$/i.test(options.secret_key ?? '')) {
  console.error('secret_key must be a 64-character hexadecimal string.');
  process.exit(1);
}

// Separate optional HA fields for bootstrapping, never put secrets in Git.
const mappings = {
  operator_auth: 'AIOSTREAMS_AUTH',
  operator_auth_permissions: 'AIOSTREAMS_AUTH_PERMISSIONS',
  database_uri: 'DATABASE_URI',
  database_pool_size: 'DATABASE_POOL_SIZE',
  redis_uri: 'REDIS_URI',
  redis_timeout: 'REDIS_TIMEOUT',
  settings_refresh_interval: 'SETTINGS_REFRESH_INTERVAL',
  internal_url: 'INTERNAL_URL',
  disk_cache_dir: 'DISK_CACHE_DIR',
  log_buffer_max_bytes: 'LOG_BUFFER_MAX_BYTES',
  log_buffer_max_entries: 'LOG_BUFFER_MAX_ENTRIES',
  node_env: 'NODE_ENV',
  system_lifecycle_enabled: 'SYSTEM_LIFECYCLE_ENABLED',
};

for (const [key, name] of Object.entries(mappings)) {
  const value = options[key];
  if (value !== undefined && value !== null && value !== '') {
    process.env[name] = String(value);
  }
}

let overrides;
try {
  overrides = JSON.parse(options.environment_overrides_json || '{}');
  if (!overrides || Array.isArray(overrides) || typeof overrides !== 'object') {
    throw new Error('Expected a JSON object');
  }
} catch (error) {
  console.error(`Invalid environment_overrides_json: ${error.message}`);
  process.exit(1);
}

const reserved = new Set(['BASE_URL', 'SECRET_KEY', 'PORT']);
for (const [name, value] of Object.entries(overrides)) {
  if (!/^[A-Z][A-Z0-9_]*$/.test(name)) {
    console.error(`Invalid environment override name: ${name}`);
    process.exit(1);
  }
  if (reserved.has(name)) {
    console.error(`${name} must not be overridden via environment_overrides_json.`);
    process.exit(1);
  }
  if (value === null || value === '') continue;
  // Arrays/maps must use the exact string representation expected by AIOStreams.
  if (!['string', 'number', 'boolean'].includes(typeof value)) {
    console.error(`Override ${name} must be a string, number, boolean or null.`);
    process.exit(1);
  }
  process.env[name] = String(value);
}

// These two options cannot be overridden by the generic settings field.
process.env.BASE_URL = options.base_url;
process.env.SECRET_KEY = options.secret_key;

// Upstream image is Node-based and does not include a shell.
await import('/app/packages/server/dist/server.js');
