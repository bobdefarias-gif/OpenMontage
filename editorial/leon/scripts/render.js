const { chromium } = require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const src=path.resolve(process.argv[2]);await p.goto('file://'+src,{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.pdf({path:process.argv[3],preferCSSPageSize:true,printBackground:true});await b.close();})();
