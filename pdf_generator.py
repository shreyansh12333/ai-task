import os
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


def generate_pdf(report_data, company_name):

    os.makedirs("output", exist_ok=True)

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("report_template.html")

    html = template.render(**report_data)

    output_path = f"output/{company_name}_report.pdf"

    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()

        page.set_content(html)

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

    print(f"PDF saved at: {output_path}")

    return output_path