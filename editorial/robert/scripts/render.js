// Render build/*.html to print PDFs (Chromium, fonts embedded).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const R = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const files = fs.readdirSync(`${R}/build`).filter(f => /^(vol|capa)-.*\.html$/.test(f));
  fs.mkdirSync(`${R}/pdf`, { recursive: true });
  for (const f of files) {
    await page.goto('file://' + `${R}/build/${f}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.pdf({ path: `${R}/pdf/${f.replace('.html', '.pdf')}`, preferCSSPageSize: true, printBackground: true });
    console.log('pdf', f);
  }
  await browser.close();
})();
