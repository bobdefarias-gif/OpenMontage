const { chromium } = require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
for(const L of ['EN','FR','NL']){fs.mkdirSync('facebook/'+L,{recursive:true});
 for(const f of fs.readdirSync('html_i18n/'+L).filter(x=>x.endsWith('.html')).sort()){
  await p.goto('file://'+path.resolve('html_i18n',L,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:'facebook/'+L+'/'+f.replace('.html','.png')});}}
await b.close();})();
