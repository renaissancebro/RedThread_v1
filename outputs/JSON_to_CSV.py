import csv
import os

def export_to_csv(results, path):
    if not results:
        print("⚠️ No data to write to CSV.")
        return

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # CSV columns
    fieldnames = [
        "title", "source_url",
        "summary_1", "summary_2", "summary_3", "summary_4", "summary_5",
        "insight_1", "insight_2", "insight_3",
        "key_provision_1", "key_provision_2", "key_provision_3", "key_provision_4", "key_provision_5", "key_provision_6",
        "recommended_action_1", "recommended_action_2", "recommended_action_3",
        "translation"
    ]

    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            # Make sure to avoid IndexError on missing items
            row = {
                "title": r.get("title", ""),
                "source_url": r.get("source_url", ""),
                "summary_1": r.get("summary", [""])[0] if len(r.get("summary", [])) > 0 else "",
                "summary_2": r.get("summary", [""])[1] if len(r.get("summary", [])) > 1 else "",
                "summary_3": r.get("summary", [""])[2] if len(r.get("summary", [])) > 2 else "",
                "summary_4": r.get("summary", [""])[3] if len(r.get("summary", [])) > 3 else "",
                "summary_5": r.get("summary", [""])[4] if len(r.get("summary", [])) > 4 else "",
                "insight_1": r.get("strategic_insights", [""])[0] if len(r.get("strategic_insights", [])) > 0 else "",
                "insight_2": r.get("strategic_insights", [""])[1] if len(r.get("strategic_insights", [])) > 1 else "",
                "insight_3": r.get("strategic_insights", [""])[2] if len(r.get("strategic_insights", [])) > 2 else "",
                "key_provision_1": r.get("key_provisions", [""])[0] if len(r.get("key_provisions", [])) > 0 else "",
                "key_provision_2": r.get("key_provisions", [""])[1] if len(r.get("key_provisions", [])) > 1 else "",
                "key_provision_3": r.get("key_provisions", [""])[2] if len(r.get("key_provisions", [])) > 2 else "",
                "key_provision_4": r.get("key_provisions", [""])[3] if len(r.get("key_provisions", [])) > 3 else "",
                "key_provision_5": r.get("key_provisions", [""])[4] if len(r.get("key_provisions", [])) > 4 else "",
                "key_provision_6": r.get("key_provisions", [""])[5] if len(r.get("key_provisions", [])) > 5 else "",
                "recommended_action_1": r.get("recommended_actions", [""])[0] if len(r.get("recommended_actions", [])) > 0 else "",
                "recommended_action_2": r.get("recommended_actions", [""])[1] if len(r.get("recommended_actions", [])) > 1 else "",
                "recommended_action_3": r.get("recommended_actions", [""])[2] if len(r.get("recommended_actions", [])) > 2 else "",
                "translation": r.get("translation", "")
            }
            writer.writerow(row)

    print(f"✅ CSV saved to: {path}")

