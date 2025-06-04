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
        md_lines.append(f"## {r.get('title', 'No Title')}\n")
        md_lines.append(f"[Original Link]({r.get('source_url', '')})\n")
        if r.get('effective_date'):
            md_lines.append(f"**Effective Date:** {r['effective_date']}\n")

        md_lines.append("### Summary\n")
        for s in r.get("summary", []):
            md_lines.append(f"- {s}")
        md_lines.append("")  # Blank line

        md_lines.append("### Strategic Insights\n")
        for i in r.get("strategic_insights", []):
            md_lines.append(f"- {i}")
        md_lines.append("")

        md_lines.append("### Key Provisions\n")
        for k in r.get("key_provisions", []):
            md_lines.append(f"- {k}")
        md_lines.append("")

        md_lines.append("### Recommended Actions\n")
        for a in r.get("recommended_actions", []):
            md_lines.append(f"- {a}")
        md_lines.append("")

        md_lines.append("### Translation\n")
        md_lines.append(r.get("translation", "").strip())
        md_lines.append("\n---\n")

    md_content = "\n".join(md_lines)

    try:
        HTML(string=markdown(md_content)).write_pdf(path)
        print(f"✅ PDF saved to {path}")
    except Exception as e:
        print(f"❌ Failed to generate PDF: {e}")


