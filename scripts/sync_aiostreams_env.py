#!/usr/bin/env python3
"""Sync documented AIOStreams vars to native HA app fields. Run in CI to propose a PR.

Source: upstream generated env reference. Existing app option names and values are preserved.
Entries not parseable with basic types get optional strings, avoiding incorrect coercions.
"""
import re, json, sys, pathlib, urllib.request
import yaml
ROOT=pathlib.Path(__file__).resolve().parent.parent
URL='https://raw.githubusercontent.com/Viren070/AIOStreams/main/packages/docs/content/docs/configuration/environment-variables.mdx'
CFG=ROOT/'aiostreams/config.yaml'
TRANS=ROOT/'aiostreams/translations/en.yaml'
LAUNCH=ROOT/'aiostreams/launcher.json'
DOC=ROOT/'aiostreams/DOCS.md'
raw=urllib.request.urlopen(URL,timeout=30).read().decode('utf-8')
config=yaml.safe_load(CFG.read_text()); t=yaml.safe_load(TRANS.read_text()); launcher=json.loads(LAUNCH.read_text());
existing_env={v:k for k,v in launcher['env'].items()}
# Parse documentation tables containing `VARIABLE` as their first column.
rows=[]
section='AIOStreams'
for line in raw.splitlines():
    if line.startswith('#'):
        section=re.sub(r'^[# ]+','',line).strip()
    if not line.startswith('|'):
        continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells)<3 or not re.fullmatch(r'`[A-Z][A-Z0-9_]+`',cells[0]):
        continue
    key=cells[0].strip('`')
    # Runtime tables: key, label, type, default, description
    # Bootstrap tables: key, default, description
    if len(cells)>=5:
        label=cells[1].strip('`'); dtype=cells[2]; desc=cells[4]
    else:
        label=key.replace('_',' ').title(); dtype='string'; desc=cells[2]
    desc=re.sub(r'\[(.*?)\]\(.*?\)',r'\1',desc)
    desc=re.sub(r'[`*_]','',desc).strip()
    rows.append((key,label,dtype,desc,section))
if len(rows)<60:
    raise SystemExit(f'Upstream format changed or incomplete reference: only {len(rows)} rows. No files changed.')
secret=re.compile(r'(SECRET|PASSWORD|TOKEN|API_KEY|CREDENTIAL|PRIVATE_KEY|ACCESS_KEY|SIGNATURE|AUTH$|URI$|DATABASE_URL)',re.I)
added=[]
for env,label,dtype,desc,section in rows:
    if env in {'PORT','PATH','NODE_OPTIONS','LD_PRELOAD','DATA_DIR'}:
        continue
    if env in existing_env:
        continue
    field=env.lower()
    if field in config['schema']:
        field='upstream_'+field
    if re.search(r'^(bool|boolean)$',dtype,re.I):
        fmt='bool?'
    elif re.search(r'^(int|integer|number)$',dtype,re.I):
        fmt='int?'
    elif secret.search(env) or '(secret)' in desc.lower():
        fmt='password?'
    else:
        fmt='str?'
    # Avoid converting any runtime setting to a required field or setting a default.
    config['schema'][field]=fmt
    launcher['env'][field]=env
    human=re.sub(r'\s+',' ',re.sub(r'<[^>]*>','',label)).strip() or env.replace('_',' ').title()
    t.setdefault('configuration',{})[field]={
        'name':human[:90],
        'description':(desc or f'Upstream {section} setting. See upstream documentation.')[:800]
    }
    added.append((env,field))
# The JSON fallback is always shown last.
v=config['schema'].pop('environment_overrides_json',None)
if v is not None: config['schema']['environment_overrides_json']=v
v=t['configuration'].pop('environment_overrides_json',None)
if v is not None: t['configuration']['environment_overrides_json']=v
CFG.write_text(yaml.safe_dump(config,sort_keys=False,allow_unicode=True))
TRANS.write_text(yaml.safe_dump(t,sort_keys=False,allow_unicode=True))
LAUNCH.write_text(json.dumps(launcher,indent=2)+'\n')
# Leave DOCS.md mostly human-maintained; append links, not full upstream copy.
print(f'Parsed {len(rows)} environment variables; added {len(added)} new Home Assistant fields:')
for env,field in added: print(f'  {env} => {field}')
