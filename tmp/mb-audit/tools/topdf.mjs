import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file://' + process.cwd() + '/report/report.html', { waitUntil: 'load' });
await p.pdf({ path: 'report/Mark-Bank-audit.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:7px;color:#9e9186;width:100%;padding:0 13mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>Mark Bank audit · 25 November 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>' });
await b.close();
