const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
  await page.goto('http://www.miit.gov.cn/', { waitUntil: 'domcontentloaded' });

  console.log('Page loaded!');

  // Fill in the search box
  await page.locator('input.search-form-txt.bt-size-16').fill('稀土');

  // Click the search button (no navigation!)
  await page.locator('.search-form-btn').click();

  // Wait for the new tab or popup to open
  const newPagePromise = new Promise(resolve => browser.once('targetcreated', target => resolve(target.page())));
  const newPage = await newPagePromise;

  await newPage.bringToFront();
  await newPage.waitForLoadState?.('domcontentloaded'); // only works in Playwright, so fallback below
  try {
    await newPage.waitForSelector('.jcse-result-box .news-result', { timeout: 10000 });
  } catch(err) {
    await newPage.screenshot({ path: 'after_click.png', fullPage: true });
  }
    const results = await newPage.$$('.jcse-result-box .news-result');
  console.log(`Found ${results.length} results`);

  for (const r of results) {
    const text = await r.evaluate(el => el.innerText.trim());
    console.log(text);
  }

  await browser.close();
})();
