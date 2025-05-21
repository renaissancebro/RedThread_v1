import csv
import os

def export_to_csv(results, path):
    if not results:
            print("⚠️ No data to write to CSV.")
            return


    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    fieldnames = [
        "title", "href",
        "summary_1", "summary_2", "summary_3",
        "insight_1", "insight_2", "insight_3",
        "translation"
    ]

    with open(path, "w", newline='', encoding="utf-8") as f:
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



    print(f"✅ CSV saved to: {path}")
