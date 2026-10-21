'use strict';
const {test,after}=require('node:test');
const assert=require('node:assert/strict');
const http=require('node:http');
const {spawn}=require('node:child_process');
const secret='fixed-test-secret-that-is-long-enough';
const local=http.createServer((req,res)=>{res.setHeader('content-type','application/json');res.end(JSON.stringify({path:req.url,method:req.method}));});
const serverPort=18992,gatewayPort=18993;
let child;
async function ready(url, opts={}) { for(let i=0;i<50;i++){try{return await fetch(url,opts)}catch{await new Promise(r=>setTimeout(r,30))}} throw new Error('gateway not running') }
test('private gateway permits only configured public catalogs and owner requests',async()=>{
  await new Promise(resolve=>local.listen(serverPort,'127.0.0.1',resolve));
  child=spawn(process.execPath,['private_gateway.js'],{cwd:require('node:path').join(__dirname,'..'),env:{...process.env,ADMIN_KEY:secret,WORKER_PORT:String(serverPort),GATEWAY_PORT:String(gatewayPort)},stdio:'ignore'});
  const root=`http://127.0.0.1:${gatewayPort}`;
  const pub=await ready(root+'/manifest.json');
  assert.equal(pub.status,200);
  assert.equal((await fetch(root+'/catalog/movie/approved.json')).status,200);
  assert.equal((await fetch(root+'/config/manifest.json')).status,200);
  assert.equal((await fetch(root+'/api/creator/register',{method:'POST'})).status,401);
  assert.equal((await fetch(root+'/api/creator/register',{method:'GET'})).status,401);
  assert.equal((await fetch(root+'/admin')).status,401);
  assert.equal((await fetch(root+'/')).status,401);
  assert.equal((await fetch(root+'/catalog/movie/approved.json',{method:'POST'})).status,401);
  assert.equal((await fetch(root+'/api/creator/register',{method:'POST',headers:{Authorization:'Basic '+Buffer.from('owner:'+secret).toString('base64')}})).status,200);
  assert.equal((await fetch(root+'/',{headers:{Authorization:'Basic '+Buffer.from('owner:'+secret).toString('base64')}})).status,200);
});
after(()=>{child?.kill();local.close()});
