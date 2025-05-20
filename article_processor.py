import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

# Load your article file
with open("miit_enriched.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

results = []
failures = []

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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content

# ✅ Select one article
article = articles[0]
print(f"Processing: {article['title']}")

# 🔁 Process with error handling
raw_output = summarize_article(article)

try:
    parsed = json.loads(raw_output)
    print("\n📌 Translation:\n", parsed["translation"])
    print("\n📝 Summary:\n", "\n".join(f"- {s}" for s in parsed["summary"]))
    print("\n🚀 Insights:\n", "\n".join(f"- {i}" for i in parsed["insights"]))

    results.append({
        "title": article["title"],
        "href": article["href"],
        "translation": parsed["translation"],
        "summary": parsed["summary"],
        "insights": parsed["insights"]
    })

except Exception as e:
    print("❌ JSON parsing failed.")
    print("Raw output:\n", raw_output)
    print("Error:\n", e)
    failures.append({
        "title": article["title"],
        "href": article["href"],
        "error": str(e)
    })

# Optional: wait to avoid hitting rate limits
time.sleep(1.5)

# 💾 Save outputs
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
with open(f"summaries_{timestamp}.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

if failures:
    with open(f"failures_{timestamp}.log", "w", encoding="utf-8") as f:
        for fail in failures:
            f.write(f"{fail['title']} | {fail['error']}\n")

print(f"\n✅ Done. {len(results)} succeeded, {len(failures)} failed.")
