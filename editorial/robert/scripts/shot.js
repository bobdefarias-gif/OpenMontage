const { chromium } = require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2400,height:1500}});
await p.goto('file://'+path.resolve(process.argv[2]),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:process.argv[3]});await b.close();})();
