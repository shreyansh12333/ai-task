
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def structure_data(cleaned: dict, company_name: str) -> dict | None:
    print(f"\n[Structurer] Starting structuring...")

    if not cleaned:
        print("[Structurer] No cleaned data provided")
        return None

    prompt = _build_prompt(cleaned, company_name)

    try:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )
        raw      = response.text
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        result = json.loads(raw.strip())
        print("[Structurer] Structuring complete ✅")
        return result

    except Exception as e:
        print(f"[Structurer] Failed: {e}")
        return None

def _build_prompt(cleaned: dict, company_name: str) -> str:
    return f"""
You are a business analyst. Based on the following scraped website data,
extract and return a structured JSON object about the company.

Company Name : {company_name}
Page Title   : {cleaned.get('title', '')}
Description  : {cleaned.get('description', '')}
Website Text : {cleaned.get('body_text', '')[:2000]}
Site Sections: {', '.join(cleaned.get('nav_links', [])[:15])}

Return ONLY a valid JSON object with these exact fields:
{{
  "company_name"      : "full company name",
  "industry"          : "industry or sector",
  "what_they_do"      : "2-3 sentence explanation of what they do",
  "key_services"      : ["service1", "service2", "service3"],
  "target_customers"  : "who their customers are",
  "business_model"    : "how they make money",
  "key_strengths"     : ["strength1", "strength2", "strength3"],
  "recent_activities" : ["activity1", "activity2"]
}}

Return ONLY the JSON. No explanation. No markdown. No code fences.
""".strip()


if __name__ == "__main__":
    from discovery import discover_url
    from fetcher import fetch_html
    from extractor import extract_text
    from cleaner import clean_data

    company = "Stripe"

    url        = discover_url(company)
    html       = fetch_html(url)
    extracted  = extract_text(html)
    cleaned    = clean_data(extracted)
    structured = structure_data(cleaned, company)

    if structured:
        print("\n── Structured Output ──")
        print(json.dumps(structured, indent=2))