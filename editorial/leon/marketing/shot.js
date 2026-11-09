const { chromium } = require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
for(const f of fs.readdirSync('html').filter(x=>x.endsWith('.html')).sort()){
 await p.goto('file://'+path.resolve('html',f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:'posts/'+f.replace('.html','.png')});}
await b.close();})();
