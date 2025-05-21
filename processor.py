import json
import time
import csv
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI
from outputs.JSON_to_CSV import export_to_csv
from outputs.JSON_to_PDF import export_to_pdf
load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

# Load all scraped articles
with open("data/miit_enriched.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

results = []
failures = []

# Function to clean the JSON response from GPT
# This function removes any markdown code fences and whitespace around the JSON response

import re

def clean_code_fences(raw_text):
    # Match only the first ```json ... ``` block and extract JSON inside
    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        # fallback: just strip any backticks and whitespace
        return raw_text.strip('` \n')



def summarize_article(article):
    prompt = f"""
    You are a bilingual Chinese-English policy analyst.

    Please analyze the following Chinese-language article and return a structured JSON with the following keys:

    - "translation": a professional, fluent English translation of the full article
    - "summary": exactly three bullet points that concisely capture the key ideas
    - "insights": three actionable recommendations for a foreign business, policymaker, or strategist interacting with China

    Return the result as **valid JSON only**. No explanation or extra formatting.

    ---
    **Title**: {article['title']}

    **Content (Chinese)**:
    {article['content'][:4000]}
    """

    print(f"[DEBUG] Prompt for '{article['title']}':\n{prompt}\n{'-'*50}")
    # Send the prompt to GPT-4o
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        print(f"[DEBUG] Raw GPT output for '{article['title']}':\n{raw}")

        # Clean raw output before JSON parsing
        clean_raw = clean_code_fences(raw)
        parsed = json.loads(clean_raw)
        return parsed
    except Exception as e:
        print(f"❌ GPT or JSON error for: {article['title']}\n{e}")
        return None





# 🔁 Process each article
for i, article in enumerate(articles[:1]):
    print(f"\n🔄 [{i+1}/{len(articles)}] Processing: {article['title']}")
    parsed = summarize_article(article)

    if parsed:
        results.append({
            "title": article["title"],
            "href": article["href"],
            "translation": parsed.get("translation", ""),
            "summary": parsed.get("summary", []),
            "insights": parsed.get("insights", [])
        })
    else:
        failures.append(article)

    time.sleep(1.5)

# 💾 Save enriched JSON
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
os.makedirs("outputs/output", exist_ok=True)

json_path = f"outputs/output/summaries_{timestamp}.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 💾 Save CSV
csv_path = f"outputs/output/summaries_{timestamp}.csv"
export_to_csv(results, csv_path)
# 💾 Save PDF
pdf_path = f"outputs/output/brief_{timestamp}.pdf"
export_to_pdf(results, pdf_path)
# 🧱 Log failures

print(f"\n✅ All done — {len(results)} succeeded, {len(failures)} failed")
print(f"📁 Outputs saved to: outputs/output/")
