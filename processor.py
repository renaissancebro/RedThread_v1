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

Analyze the following Chinese regulation and generate a structured JSON with these keys:

- "title": the regulation's title in English (translate if needed)
- "effective_date": the regulation's effective date (extract or write 'Not specified' if missing)
- "source_url": the URL for the original article
- "summary": 3 to 5 bullet points (short, clear sentences) summarizing the core points, context, and what’s new or important
- "strategic_insights": 3 actionable insights for Western businesses, analysts, or policymakers (not generic, be specific and practical)
- "key_provisions": 4 to 6 bullet points condensing the most important articles, requirements, or enforcement mechanisms from the regulation
- "recommended_actions": 3 recommendations for how a foreign company or policymaker should respond or prepare
- "translation": a fluent, professional English translation of the regulation’s main text (only if short; otherwise, summarize the most critical sections in fluent English)

**Instructions:**
- Do NOT include the original Chinese text.
- Be concise. Total output should fit within a 1–2 page brief when rendered.
- Use clear, professional English with no unnecessary repetition.
- Return **valid JSON only** (no markdown, code fences, or explanation).

---
Title: {article['title']}
Source URL: {article['href']}
Content (Chinese): {article['content']}
"""

    # Print the prompt for debugging

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
for i, article in enumerate(articles[:3]):
    print(f"\n🔄 [{i+1}/{len(articles)}] Processing: {article['title']}")
    parsed = summarize_article(article)

    if parsed:
        # Safely fill in all new keys from the prompt/response, with fallbacks for missing fields
        results.append({
            "title": parsed.get("title", article.get("title", "")),
            "effective_date": parsed.get("effective_date", "Not specified"),
            "source_url": parsed.get("source_url", article.get("href", "")),
            "summary": parsed.get("summary", []),
            "strategic_insights": parsed.get("strategic_insights", []),
            "key_provisions": parsed.get("key_provisions", []),
            "recommended_actions": parsed.get("recommended_actions", []),
            "translation": parsed.get("translation", "")
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
