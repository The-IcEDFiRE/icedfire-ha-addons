#!/usr/bin/env python3
import sys, pathlib, yaml
app, action, *extra = sys.argv[1:]
if app not in ('aiostreams','aiometadata','aiomanager','redis','postgresql'): raise SystemExit('unknown app')
path = pathlib.Path(app) / 'config.yaml'
config = yaml.safe_load(path.read_text())
if action == 'version': print(config['version'])
elif action == 'upstream':
    value = (pathlib.Path(app)/'Dockerfile').read_text().splitlines()[0]
    print(value.partition('=')[2])
elif action == 'set-version':
    version=extra[0]
    # Preserve existing YAML representation and formatting
    data=path.read_text().splitlines(keepends=True)
    import re
    result=[re.sub(r'^(version:\s*).*$' , lambda m:m.group(1)+'"'+version+'"', row.rstrip('\n'))+'\n' if row.startswith('version:') else row for row in data]
    path.write_text(''.join(result))
else: raise SystemExit('unknown action')
