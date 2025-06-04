"""
Flow:
1. go to chinese site with search box
2. Use relevant category in chinese and input in search bar with playwright/puppeteer
3. Once searched, collect all news objects, and paginate through frirst 3 pages and make a list
4. Access each item in list and parse it
5. Tranlsate with nlp or special tool
6. Pass to chat or Ollama to summarize meaning and create an output json
7. Enrich or vet data by manual walk through

"""
import json
import os
from datetime import datetime

from outputs.JSON_to_CSV import export_to_csv
from outputs.JSON_to_PDF import export_to_pdf

# 🔄 Load enriched data (produced by GPT pipeline)
input_path = "data/enriched_output/articles_enriched_20250521_1200.json"

with open(input_path, "r", encoding="utf-8") as f:
    enriched_articles = json.load(f)

# 🕒 Generate timestamp for output files
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_dir = "outputs/output"
os.makedirs(output_dir, exist_ok=True)

# 📦 Export CSV
csv_path = os.path.join(output_dir, f"summaries_{timestamp}.csv")
export_to_csv(enriched_articles, csv_path)

# 📰 Export PDF Brief
pdf_path = os.path.join(output_dir, f"brief_{timestamp}.pdf")
export_to_pdf(enriched_articles, pdf_path)

print(f"\n✅ All exports completed.\n- CSV: {csv_path}\n- PDF: {pdf_path}")
