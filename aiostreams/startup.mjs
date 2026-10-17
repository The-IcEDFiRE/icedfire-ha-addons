import { readFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
const launcher = JSON.parse(readFileSync(new URL('./launcher.json', import.meta.url), 'utf8'));
const options = JSON.parse(readFileSync(`${launcher.data_path}/options.json`, 'utf8'));
for (const field of launcher.required) {
  if (!options[field]) throw new Error(`Missing required Home Assistant option: ${field}`);
}
for (const [field, variable] of Object.entries(launcher.env)) {
  const value = options[field];
  if (value !== undefined && value !== null && value !== '') process.env[variable] = String(value);
}
let extras;
try { extras = JSON.parse(options.environment_overrides_json || '{}'); }
catch (error) { throw new Error(`Invalid environment_overrides_json: ${error.message}`); }
if (!extras || Array.isArray(extras) || typeof extras !== 'object') throw new Error('environment_overrides_json must contain a JSON object');
for (const [key, value] of Object.entries(extras)) {
  if (!/^[A-Z_][A-Z0-9_]*$/.test(key)) throw new Error(`Invalid environment variable name: ${key}`);
  if (['PATH', 'NODE_OPTIONS', 'LD_PRELOAD', 'DATA_DIR', 'PORT'].includes(key)) throw new Error(`Protected environment variable: ${key}`);
  if (value !== null && value !== '') process.env[key] = typeof value === 'string' ? value : JSON.stringify(value);
}
const args = launcher.mode === 'shell' ? [] : [launcher.target];
const command = launcher.mode === 'shell' ? launcher.target : process.execPath;
const child = spawn(command, args, { env: process.env, stdio: 'inherit' });
for (const signal of ['SIGTERM','SIGINT']) process.on(signal, () => child.kill(signal));
child.on('error', e => { console.error(e); process.exitCode = 1; });
child.on('exit', (code, signal) => { process.exit(signal ? 128 + (signal === 'SIGTERM' ? 15 : 2) : code ?? 1); });
