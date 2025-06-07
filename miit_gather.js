"use strict";
const puppeteer = require("puppeteer");
const fs = require("fs");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)); //helper function, promise to wait for resolved
const website = "http://www.miit.gov.cn/";
const searchTerm = "稀土"; // Search term for the MIIT website

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    protocolTimeout: 60000,
  });

  const page = await browser.newPage();

  // Stealth setup
  await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, "webdriver", { get: () => false });
    Object.defineProperty(navigator, "languages", {
      get: () => ["zh-CN", "zh", "en-US"],
    });
    Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3] });
    window.chrome = { runtime: {} };
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) =>
      parameters.name === "notifications"
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters);
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function (parameter) {
      if (parameter === 37445) return "Intel Inc.";
      if (parameter === 37446) return "Intel Iris OpenGL Engine";
      return getParameter(parameter);
    };
  });

  await page.goto(website, { waitUntil: "networkidle2" });
  console.log("Page loaded!");

  await page.waitForSelector("input.search-form-txt.bt-size-16");
  await page.type("input.search-form-txt.bt-size-16", searchTerm);

  const [searchPage] = await Promise.all([
    new Promise((resolve) =>
      browser.once("targetcreated", async (target) => {
        const newPage = await target.page();
        await newPage.bringToFront();
        resolve(newPage);
      })
    ),
    page.click(".search-form-btn"),
  ]);

  await sleep(3000); // crude wait
  await searchPage.waitForSelector(".itemdiv", { timeout: 10000 });

  const allResults = [];

  for (let i = 1; i <= 2; i++) {
    if (i > 1) {
      const selector = `a[paged="${i}"]`;
      console.log(`📎 Navigating to page ${i}...`);

      try {
        await searchPage.waitForSelector(selector, { visible: true });

        const prevFirstItem = await searchPage.evaluate(() => {
          const el = document.querySelector(".jcse-result-box .itemdiv");
          return el ? el.innerText.trim() : null;
        });

        await searchPage.click(selector);

        await searchPage.waitForFunction(
          (oldText) => {
            const el = document.querySelector(".jcse-result-box .itemdiv");
            return el && el.innerText.trim() !== oldText;
          },
          { timeout: 10000 },
          prevFirstItem
        );

        await sleep(1000);
      } catch (err) {
        console.error(`⚠️ Failed to go to page ${i}`, err);
        break;
      }
    }

    // Extract results for this page
    try {
      const results = await searchPage.evaluate(() => {
        return Array.from(document.querySelectorAll(".jcse-result-box a"))
          .map((a) => {
            const div = a.querySelector(".itemdiv");
            const text = div
              ? div.textContent.replace(/\s+/g, " ").trim()
              : null;
            const relative = a.getAttribute("href");
            const fullHref = new URL(relative, location.origin).href;

            return {
              title: text,
              href: fullHref,
            };
          })
          .filter((item) => item.title && item.href);
      });

      console.log(`✅ Page ${i} - Found ${results.length} results`);
      results.forEach((r, index) => {
        console.log(`\n${index + 1}. ${r.title}`);
        console.log(`🔗 ${r.href}`);
      });

      allResults.push(...results);
    } catch (err) {
      console.error(`❌ Error extracting results on page ${i}:`, err);
    }
  }

  fs.writeFileSync("miit_results.json", JSON.stringify(allResults, null, 2));
  console.log(
    `\n💾 Saved ${allResults.length} total results to 'miit_results.json'`
  );

  await browser.close();
})();
