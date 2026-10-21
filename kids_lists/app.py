import os, json, sqlite3, html, secrets, hashlib, hmac, urllib.request, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from pathlib import Path

DATA=Path('/data' if Path('/data').exists() else os.environ.get('DATA_DIR','./data'))
DATA.mkdir(parents=True,exist_ok=True)
DB=DATA/'lists.sqlite3'
SETTINGS=DATA/'secret'
if not SETTINGS.exists():
    SETTINGS.write_text(secrets.token_urlsafe(36))
    os.chmod(SETTINGS,0o600)
SECRET=SETTINGS.read_text().strip()
PASSWORD=os.environ.get('ADMIN_PASSWORD','')
TMDB=os.environ.get('TMDB_API_KEY','')
PORT=int(os.environ.get('PORT','8099'))

def db():
    c=sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, media_type TEXT NOT NULL CHECK(media_type IN (\'movie\',\'series\')), imdb_id TEXT NOT NULL, title TEXT NOT NULL, poster TEXT NOT NULL DEFAULT \'\', UNIQUE(media_type,imdb_id))')
    c.commit();return c

def esc(s):return html.escape(str(s),quote=True)
def json_bytes(obj):return json.dumps(obj,separators=(',',':')).encode()
def sign(v):return hmac.new(SECRET.encode(),v.encode(),hashlib.sha256).hexdigest()
def authenticated(handler):
    if not PASSWORD:return False
    cookie=SimpleCookie()
    try:cookie.load(handler.headers.get('Cookie',''))
    except Exception:return False
    token=cookie.get('session')
    if not token:return False
    return hmac.compare_digest(token.value,sign('admin'))

def layout(body):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kids Lists</title><style>body{{font:16px system-ui,sans-serif;max-width:850px;margin:0 auto;padding:18px;background:#101622;color:#fafafa}}a{{color:#8dccff}}input,select,button{{font:inherit;padding:10px;border-radius:8px;border:1px solid #7d8796;margin:4px 0;background:#fff;color:#111}}button{{cursor:pointer}}form{{margin:10px 0}}.card{{background:#202b3a;border-radius:12px;padding:13px;margin:10px 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}}img{{max-width:100%;border-radius:8px}}.muted{{color:#c5ced9}}.danger{{background:#a52727;color:white}}</style></head><body><h1>Kids Lists</h1>{body}</body></html>'''

class Handler(BaseHTTPRequestHandler):
    def send(self,status,blob,mime='text/html; charset=utf-8',extra=None):
        self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(blob)));self.send_header('Cache-Control','no-store' if 'text/html' in mime else 'public, max-age=60');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY');self.send_header('Referrer-Policy','no-referrer');
        for k,v in (extra or {}).items():self.send_header(k,v)
        self.end_headers();self.wfile.write(blob)
    def page(self,s,status=200,extra=None):self.send(status,layout(s).encode(),extra=extra)
    def redirect(self,where='/',extra=None):self.send(303,b'',extra={'Location':where,**(extra or {})})
    def parse(self):
        length=int(self.headers.get('Content-Length',0))
        if length>16384:raise ValueError('Form too large')
        return {k:v[0] for k,v in urllib.parse.parse_qs(self.rfile.read(length).decode()).items()}
    def require(self):
        if authenticated(self):return True
        self.page('<p>Sign in to manage the approved titles.</p><form action="/login" method="post"><input type="password" name="password" placeholder="Admin password" required><button>Sign in</button></form>',401)
        return False
    def do_GET(self):
        url=urllib.parse.urlsplit(self.path);p=url.path; qs=urllib.parse.parse_qs(url.query)
        if p=='/health':return self.send(200,b'ok','text/plain')
        if p=='/manifest.json':
            return self.send(200,json_bytes({'id':'org.icedfire.kidslists','version':'1.0.0','name':'Kids Lists (curated)','description':'Parent-approved catalogs; not playback enforcement','resources':['catalog'],'types':['movie','series'],'catalogs':[{'type':'movie','id':'kids-movies','name':'Approved Movies'},{'type':'series','id':'kids-series','name':'Approved Series'}]}),'application/json')
        if p.startswith('/catalog/') and p.endswith('.json'):
            bits=p.strip('/').split('/')
            if len(bits)!=3 or bits[1] not in ('kids-movies','kids-series') or bits[0]!='catalog':return self.send(404,b'Not found','text/plain')
            media='movie' if bits[1]=='kids-movies' else 'series'
            with db() as c:rows=c.execute('SELECT imdb_id,title,poster FROM items WHERE media_type=? ORDER BY title COLLATE NOCASE',(media,)).fetchall()
            return self.send(200,json_bytes({'metas':[{'id':i,'type':media,'name':title,**({'poster':poster} if poster else {})} for i,title,poster in rows]}),'application/json')
        if p=='/':
            if not self.require():return
            with db() as c:rows=c.execute('SELECT id,media_type,imdb_id,title,poster FROM items ORDER BY media_type,title COLLATE NOCASE').fetchall()
            cards=''.join(f'<div class="card">{("<img loading=lazy src=\""+esc(poster)+"\">" if poster else "")}<h3>{esc(title)}</h3><p class="muted">{esc(typ)} · {esc(imdb)}</p><form method="post" action="/delete"><input type="hidden" name="id" value="{id}"><input type="hidden" name="csrf" value="{sign("csrf")}"><button class="danger">Remove</button></form></div>' for id,typ,imdb,title,poster in rows)
            base=f'{"https" if self.headers.get("X-Forwarded-Proto","")=="https" else "http"}://{self.headers.get("Host","localhost:8099")}'
            body=f'<p>Approved titles: {len(rows)}. This publishes catalogs only; it does <b>not block</b> unapproved playback.</p><p>Stremio addon manifest: <a href="/manifest.json">{esc(base)}/manifest.json</a></p>'
            body+=f'<div class="card"><h2>Add approved title</h2><form method="post" action="/add"><input type="hidden" name="csrf" value="{sign("csrf")}"><p><select name="type"><option value="movie">Movie</option><option value="series">Series</option></select></p><p><input name="title" placeholder="Title" maxlength="160" required></p><p><input name="imdb" placeholder="IMDb ID (tt1234567)" pattern="tt[0-9]{{7,12}}" required></p><p><input name="poster" type="url" placeholder="Poster URL (optional)" style="width:90%"></p><button>Add to kids catalog</button></form></div>'
            if TMDB:body+='<div class="card"><h2>Find titles</h2><form action="/search" method="get"><input name="q" placeholder="Search TMDB" required><button>Search</button></form></div>'
            else:body+='<p class="muted">For phone-friendly title search, configure your optional TMDB API key. Without it, add titles by IMDb ID. The app and list storage remain local.</p>'
            return self.page(body+'<div class="grid">'+cards+'</div><form method="post" action="/logout"><button>Sign out</button></form>')
        if p=='/search':
            if not self.require():return
            if not TMDB:return self.page('TMDB key not configured',400)
            q=qs.get('q',[''])[0][:100]
            try:
                req=urllib.request.Request('https://api.themoviedb.org/3/search/multi?'+urllib.parse.urlencode({'api_key':TMDB,'query':q,'include_adult':'false'}),headers={'User-Agent':'KidsLists/1.0'})
                with urllib.request.urlopen(req,timeout=8) as res:data=json.load(res)
                results=[]
                for obj in data.get('results',[]):
                    typ=obj.get('media_type')
                    if typ not in ('movie','tv'):continue
                    title=obj.get('title') or obj.get('name') or ''
                    poster='https://image.tmdb.org/t/p/w342'+obj['poster_path'] if obj.get('poster_path') else ''
                    results.append(f'<div class="card"><h3>{esc(title)}</h3><p>{esc(typ)}</p><form method="post" action="/add-tmdb"><input type="hidden" name="csrf" value="{sign("csrf")}"><input type="hidden" name="tmdb_id" value="{int(obj["id"])}"><input type="hidden" name="type" value="{esc(typ)}"><input type="hidden" name="title" value="{esc(title)}"><input type="hidden" name="poster" value="{esc(poster)}"><button>Approve</button></form></div>')
                return self.page('<a href="/">← Back</a><h2>Results for '+esc(q)+'</h2>'+''.join(results))
            except Exception as e:return self.page('<p>TMDB search unavailable: '+esc(type(e).__name__)+'</p>',502)
        return self.send(404,b'Not found','text/plain')
    def do_POST(self):
        p=urllib.parse.urlsplit(self.path).path
        try:f=self.parse()
        except Exception:return self.page('Invalid form',400)
        if p=='/login':
            if PASSWORD and hmac.compare_digest(f.get('password',''),PASSWORD):return self.redirect('/',{'Set-Cookie':'session='+sign('admin')+'; HttpOnly; SameSite=Lax; Path=/'})
            return self.page('Incorrect password',403)
        if not self.require():return
        if p=='/logout':return self.redirect('/',{'Set-Cookie':'session=; Max-Age=0; HttpOnly; SameSite=Lax; Path=/'})
        if not hmac.compare_digest(f.get('csrf',''),sign('csrf')):return self.page('Invalid form token',403)
        if p=='/delete':
            try:id=int(f.get('id','0'))
            except ValueError:return self.page('Invalid item',400)
            with db() as c:c.execute('DELETE FROM items WHERE id=?',(id,))
            return self.redirect()
        if p=='/add-tmdb':
            if not TMDB:return self.page('TMDB is not configured',400)
            try:
                tid=int(f.get('tmdb_id','0'));typ=f.get('type','')
                if typ not in ('movie','tv') or tid<=0:raise ValueError()
                path=f'/3/{typ}/{tid}/external_ids'
                url='https://api.themoviedb.org'+path+'?'+urllib.parse.urlencode({'api_key':TMDB})
                with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'KidsLists/1.0'}),timeout=8) as res:ids=json.load(res)
                imdb=ids.get('imdb_id','')
                f={'type':'series' if typ=='tv' else 'movie','imdb':imdb,'title':f.get('title',''),'poster':f.get('poster','')}
            except Exception:return self.page('Unable to resolve IMDb ID for this title. Add it manually instead.',422)
        if p in ('/add','/add-tmdb'):
            typ=f.get('type','');imdb=f.get('imdb','');title=f.get('title','').strip();poster=f.get('poster','').strip()
            import re
            if typ not in ('movie','series') or not re.fullmatch(r'tt\d{7,12}',imdb) or not (0<len(title)<=160) or len(poster)>500 or (poster and not poster.startswith('https://')):return self.page('Invalid title, IMDb ID, or poster',400)
            with db() as c:c.execute('INSERT INTO items(media_type,imdb_id,title,poster) VALUES(?,?,?,?) ON CONFLICT(media_type,imdb_id) DO UPDATE SET title=excluded.title,poster=excluded.poster',(typ,imdb,title,poster))
            return self.redirect()
        return self.send(404,b'Not found','text/plain')

if __name__=='__main__':
    if not PASSWORD:raise SystemExit('ADMIN_PASSWORD must be configured')
    db().close()
    print(f'Kids Lists listening on {PORT}',flush=True)
    ThreadingHTTPServer(('0.0.0.0',PORT),Handler).serve_forever()
