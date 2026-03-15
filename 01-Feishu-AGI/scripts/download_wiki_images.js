#!/usr/bin/env node
const fs = require('fs/promises');
const path = require('path');
const { chromium } = require('playwright');

function guessExt(contentType, fallbackName = '') {
  const ct = (contentType || '').toLowerCase();
  if (ct.includes('png')) return '.png';
  if (ct.includes('jpeg') || ct.includes('jpg')) return '.jpg';
  if (ct.includes('webp')) return '.webp';
  if (ct.includes('gif')) return '.gif';
  const ext = path.extname(fallbackName || '');
  return ext || '.png';
}

(async () => {
  const [wikiToken, jobsPath] = process.argv.slice(2);
  if (!wikiToken || !jobsPath) {
    console.error('Usage: download_wiki_images.js <wikiToken> <jobsJsonPath>');
    process.exit(1);
  }

  const jobs = JSON.parse(await fs.readFile(jobsPath, 'utf8'));
  const outDir = jobs.out_dir;
  const images = jobs.images || [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  try {
    await page.goto(`https://waytoagi.feishu.cn/wiki/${wikiToken}`, {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    await page.waitForTimeout(2500);

    const results = [];
    for (const img of images) {
      const previewUrl = `https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/preview/${img.token}/?preview_type=16`;
      try {
        const fetched = await page.evaluate(async (url) => {
          const res = await fetch(url, { credentials: 'include' });
          const contentType = res.headers.get('content-type') || '';
          const ab = await res.arrayBuffer();
          let binary = '';
          const bytes = new Uint8Array(ab);
          const chunkSize = 0x8000;
          for (let i = 0; i < bytes.length; i += chunkSize) {
            const chunk = bytes.subarray(i, i + chunkSize);
            binary += String.fromCharCode(...chunk);
          }
          return {
            ok: res.ok,
            status: res.status,
            contentType,
            base64: btoa(binary),
            bytes: bytes.length,
          };
        }, previewUrl);

        if (!fetched.ok) throw new Error(`HTTP ${fetched.status}`);
        const ext = guessExt(fetched.contentType, img.name);
        const finalName = img.filename || `${img.token}${ext}`;
        const savedPath = path.join(outDir, finalName);
        await fs.mkdir(path.dirname(savedPath), { recursive: true });
        await fs.writeFile(savedPath, Buffer.from(fetched.base64, 'base64'));
        results.push({
          token: img.token,
          saved_path: savedPath,
          content_type: fetched.contentType,
          bytes: fetched.bytes,
          ok: true,
        });
      } catch (err) {
        results.push({
          token: img.token,
          ok: false,
          error: err instanceof Error ? err.message : String(err),
        });
      }
    }

    console.log(JSON.stringify({ ok: true, results }));
  } finally {
    await context.close();
    await browser.close();
  }
})().catch(err => {
  console.error(JSON.stringify({ ok: false, error: err instanceof Error ? err.message : String(err) }));
  process.exit(1);
});

