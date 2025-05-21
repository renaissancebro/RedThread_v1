# 💾 Save CSV
csv_path = f"outputs/output/summaries_{timestamp}.csv"
with open(csv_path, "w", newline='', encoding="utf-8") as f:
    fieldnames = [
        "title", "href",
        "summary_1", "summary_2", "summary_3",
        "insight_1", "insight_2", "insight_3",
        "translation"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        writer.writerow({
            "title": r["title"],
            "href": r["href"],
            "summary_1": r["summary"][0] if len(r["summary"]) > 0 else "",
            "summary_2": r["summary"][1] if len(r["summary"]) > 1 else "",
            "summary_3": r["summary"][2] if len(r["summary"]) > 2 else "",
            "insight_1": r["insights"][0] if len(r["insights"]) > 0 else "",
            "insight_2": r["insights"][1] if len(r["insights"]) > 1 else "",
            "insight_3": r["insights"][2] if len(r["insights"]) > 2 else "",
            "translation": r["translation"]
        })

# 🧱 Log failures
if failures:
    with open(f"outputs/output/failures_{timestamp}.log", "w", encoding="utf-8") as f:
        for fail in failures:
            f.write(f"{fail['title']} | {fail['href']}\n")
