#!/bin/bash

echo "🚀 Starting AlphaRed MIIT pipeline..."

echo "🕷️ Running scraper..."
node miit_gather.js
if [ $? -ne 0 ]; then
  echo "❌ Scraper failed"
  exit 1
fi

echo "🧠 Running enricher..."
node enrich_articles.js
if [ $? -ne 0 ]; then
  echo "❌ Enricher failed"
  exit 1
fi

echo "📊 Running processor..."
python3 processor.py
if [ $? -ne 0 ]; then
  echo "❌ Processor failed"
  exit 1
fi

echo "✅ MIIT pipeline completed successfully!"
