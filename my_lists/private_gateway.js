'use strict';
// Access boundary for the locally hosted My Lists Worker.
// Only explicit read-only Stremio catalog/metadata endpoints are public.
const http = require('node:http');
const crypto = require('node:crypto');
const PORT = Number(process.env.GATEWAY_PORT || 8787);
const TARGET_PORT = Number(process.env.WORKER_PORT || 8788);
const KEY = process.env.ADMIN_KEY || '';
if (KEY.length < 24) {
  console.error('ADMIN_KEY must be a unique secret of at least 24 characters; refusing to start.');
  process.exit(1);
}
const cookieTag = crypto.createHmac('sha256', KEY).update('my-lists-owner-session-v1').digest('hex');
function authorized(req) {
  const cookie = (req.headers.cookie || '').split(';').map(x=>x.trim()).find(x=>x.startsWith('ml_owner='));
  if (cookie) {
    const value = cookie.slice('ml_owner='.length);
    if (value.length === cookieTag.length && crypto.timingSafeEqual(Buffer.from(value), Buffer.from(cookieTag))) return true;
  }
  const auth = req.headers.authorization || '';
  if (!auth.startsWith('Basic ')) return false;
  let raw;
  try { raw = Buffer.from(auth.slice(6), 'base64').toString('utf8'); } catch { return false; }
  const sep = raw.indexOf(':');
  if (sep < 0 || raw.slice(0,sep) !== 'owner') return false;
  const actual = Buffer.from(raw.slice(sep + 1));
  const expected = Buffer.from(KEY);
  return actual.length === expected.length && crypto.timingSafeEqual(actual, expected);
}
function readOnlyStremio(req, pathname) {
  if (req.method !== 'GET' && req.method !== 'HEAD') return false;
  // Match known Stremio protocol endpoints, including optional configuration prefix.
  // No query-string or pathname can make a write request public.
  const path = pathname;
  if (path.length > 2048 || path.includes('..') || /%2f|%5c/i.test(path)) return false;
  return /^(?:\/[A-Za-z0-9_~.%:-]{1,1024})?\/manifest\.json$/i.test(path) ||
    /^(?:\/[A-Za-z0-9_~.%:-]{1,1024})?\/(?:catalog|meta)\/(?:movie|series)\/[A-Za-z0-9_.:-]+(?:\/[A-Za-z0-9_.:-]+)?\.json$/i.test(path);
}
const server = http.createServer((req,res) => {
  let path;
  try { path = new URL(req.url,'http://internal.invalid').pathname; }
  catch { res.writeHead(400); return res.end('Bad URL'); }
  const isPublic=readOnlyStremio(req,path);
  const isAuthorized=authorized(req);
  if (!isPublic && !isAuthorized) {
    res.writeHead(401, {'WWW-Authenticate': 'Basic realm="My Lists owner", charset="UTF-8"', 'Cache-Control':'no-store','Content-Type':'text/plain'});
    return res.end('Owner authentication required');
  }
  // Reject cross-origin browser mutations even for browsers holding cached credentials.
  if (req.method !== 'GET' && req.method !== 'HEAD' && req.method !== 'OPTIONS' && req.headers.origin) {
    const expectedHost=req.headers['x-forwarded-host'] || req.headers.host;
    let originHost;
    try {originHost=new URL(req.headers.origin).host;} catch {originHost='';}
    if (originHost !== expectedHost) {res.writeHead(403);return res.end('Origin mismatch');}
  }
  const headers = {...req.headers, host:`127.0.0.1:${TARGET_PORT}`};
  if ((headers.authorization||'').startsWith('Basic ')) delete headers.authorization;
  delete headers['proxy-authorization'];
  const upstream = http.request({hostname:'127.0.0.1',port:TARGET_PORT,path:req.url,method:req.method,headers}, response => {
    const responseHeaders = {...response.headers};
    delete responseHeaders['access-control-allow-origin'];
    // Don't allow an unrelated website to submit authenticated browser requests.
    responseHeaders['x-content-type-options']='nosniff';
    // Basic authentication establishes a cookie for the app's JavaScript API calls.
    if (isAuthorized && (req.headers.authorization || '').startsWith('Basic ')) {
      const secure = req.headers['x-forwarded-proto'] === 'https';
      responseHeaders['set-cookie'] = `ml_owner=${cookieTag}; Path=/; HttpOnly; SameSite=Strict${secure ? '; Secure' : ''}`;
    }
    res.writeHead(response.statusCode || 502,responseHeaders);
    response.pipe(res);
  });
  upstream.on('error',() => {if (!res.headersSent) res.writeHead(502); res.end('Local application unavailable');});
  req.pipe(upstream);
});
server.listen(PORT,'0.0.0.0',()=>console.log(`Private gateway listening on :${PORT}, worker on loopback :${TARGET_PORT}`));
