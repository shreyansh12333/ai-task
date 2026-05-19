# pdf.py

import os
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


def generate_pdf(report_data: dict, company_name: str):

    # ─────────────────────────────────
    # CREATE OUTPUT FOLDER
    # ─────────────────────────────────
    os.makedirs("outputs", exist_ok=True)

    # ─────────────────────────────────
    # LOAD HTML TEMPLATE
    # ─────────────────────────────────
    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("report_template.html")

    # ─────────────────────────────────
    # RENDER HTML WITH DATA
    # ─────────────────────────────────
    html = template.render(**report_data)

    # OPTIONAL DEBUG HTML
    with open("outputs/debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    # ─────────────────────────────────
    # OUTPUT PDF PATH
    # ─────────────────────────────────
    output_path = f"outputs/{company_name}_Report.pdf"

    # ─────────────────────────────────
    # GENERATE PDF
    # ─────────────────────────────────
    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()

        # Better rendering
        page.set_viewport_size({
            "width": 1400,
            "height": 2000
        })

        # Load HTML
        page.set_content(html)

        # Wait for full render
        page.wait_for_load_state("networkidle")

        # Generate PDF
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={
                "top": "20px",
                "bottom": "20px",
                "left": "20px",
                "right": "20px"
            }
        )

        browser.close()

    print(f"\n✅ PDF Generated Successfully")
    print(f"📄 Saved At: {output_path}")

    return output_path