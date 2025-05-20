"use strict";
// This script uses Puppeteer to scrape the MIIT website for search results.
const puppeteer = require("puppeteer");
const fs = require("fs");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

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

  // Go to homepage and perform search
  await page.goto("http://www.miit.gov.cn/", { waitUntil: "networkidle2" });
  console.log("Page loaded!");

  await page.waitForSelector("input.search-form-txt.bt-size-16");
  await page.type("input.search-form-txt.bt-size-16", "稀土");

  const [newPage] = await Promise.all([
    new Promise((resolve) =>
      browser.once("targetcreated", async (target) => {
        const newPage = await target.page();
        await newPage.bringToFront();
        resolve(newPage);
      })
    ),
    page.click(".search-form-btn"),
  ]);

  // Crude wait or smarter wait below
  console.log("sleeping for 3s");
  await sleep(3000);
  console.log("done waiting");

  await newPage.waitForSelector(".itemdiv", { timeout: 10000 });
  await newPage.waitForFunction(
    () => {
      const el = document.querySelector(".itemdiv");
      return el && el.innerText.trim().length > 0;
    },
    { timeout: 10000 }
  );

  console.log("✅ Navigated to search results");
  console.log("URL:", await newPage.url());
  console.log("Title:", await newPage.title());

  // Debug dump
  const html = await newPage.content();
  fs.writeFileSync("debug.html", html);
  await newPage.screenshot({ path: "screenshot.png", fullPage: true });

  // Extract text from each result item
  let results = [];
  try {
    results = await newPage.evaluate(() => {
      return Array.from(document.querySelectorAll(".jcse-result-box .itemdiv"))
        .map((el) => el.innerText.trim())
        .filter(Boolean);
    });
    console.log(`\n🧾 Found ${results.length} results:\n`);
  } catch (err) {
    console.error("Error extracting results:", err);
  }
  const logResults = await newPage.evaluate(() => {
    const items = Array.from(
      document.querySelectorAll(".jcse-result-box .itemdiv")
    );
    return items.map((item) => item.innerText);
  });

  results.forEach((text, index) => {
    console.log(`${index + 1}. ${text}`);
  });

  await sleep(5000);
  await browser.close();
})();
