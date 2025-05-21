from markdown2 import markdown
from weasyprint import HTML
import os

def export_to_pdf(results, path):
    if not results:
        print("⚠️ No results to export to PDF.")
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)

    md_lines = [f"# MIIT Weekly Brief\n\n"]

    for r in results:
        md_lines.append(f"## {r['title']}\n")
        md_lines.append(f"[🔗 Original Link]({r['href']})\n")

        md_lines.append("### 🈳 Translation\n")
        md_lines.append(r.get("translation", "").strip() + "\n")

        md_lines.append("### 📝 Summary\n")
        for s in r.get("summary", []):
            md_lines.append(f"- {s}")

        md_lines.append("\n### 🚀 Strategic Insights\n")
        for i in r.get("insights", []):
            md_lines.append(f"- {i}")

        md_lines.append("\n---\n")

    md_content = "\n".join(md_lines)

    try:
        HTML(string=markdown(md_content)).write_pdf(path)
        print(f"✅ PDF saved to {path}")
    except Exception as e:
        print(f"❌ Failed to generate PDF: {e}")
