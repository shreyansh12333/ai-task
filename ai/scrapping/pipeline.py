

import json
from  ai.scrapping.discovery  import discover_url
from  ai.scrapping.fetcher    import fetch_html
from ai.scrapping.extractor  import extract_text
from  ai.scrapping.cleaner    import clean_data
from ai.scrapping.structurer import structure_data

def research(company_name: str) -> dict | None:
    print(f"\n{'='*50}")
    print(f"  Researching: {company_name}")
    print(f"{'='*50}")

    url = discover_url(company_name)
    if not url:
        print("[Pipeline] Could not find URL — using name only")

    html = fetch_html(url) if url else None
    if not html:
        print("[Pipeline] Could not fetch HTML — structuring from name only")

    extracted = extract_text(html) if html else None


    cleaned = clean_data(extracted) if extracted else None

    result = structure_data(cleaned, company_name)

    if result:
        print(f"\n[Pipeline]  Research complete for: {company_name}")
    else:
        print(f"\n[Pipeline]  Research failed for: {company_name}")

    return result

