"use strict";
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Load scraped results
const inputPath = path.join(__dirname, "miit_results.json");
const outputPath = path.join(__dirname, "miit_enriched.json");

(async () => {
  const data = JSON.parse(fs.readFileSync(inputPath, "utf-8"));
  const enriched = [];

  const browser = await puppeteer.launch({
    headless: false,
    protocolTimeout: 60000,
  });
  // How many articles to enrich : data.length
  for (let i = 0; i < 2; i++) {
    const item = data[i];
    console.log(`\n🔍 [${i + 1}/${data.length}] Visiting: ${item.title}`);
    const page = await browser.newPage();

    try {
      await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
      await page.goto(item.href, {
        waitUntil: "domcontentloaded",
        timeout: 30000,
      });

      // You can tweak the selector below if needed
      const content = await page.evaluate(() => {
        const paragraphs = Array.from(document.querySelectorAll("p"));
        return paragraphs
          .map((p) => p.innerText.trim())
          .filter((text) => text.length > 10)
          .join("\n\n");
      });

      item.content = content || "[No content found]";
    } catch (err) {
      console.error(`❌ Error visiting ${item.href}:`, err.message);
      item.content = "[ERROR]";
    } finally {
      enriched.push(item);
      fs.writeFileSync(outputPath, JSON.stringify(enriched, null, 2)); // checkpointing
      await page.close();
      await sleep(1000); // buffer between page loads
    }
  }

  await browser.close();
  console.log(`\n✅ Finished enrichment. Saved to ${outputPath}`);
})();
