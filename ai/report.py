import os
import json
import sys

from dotenv import load_dotenv
from google import genai


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf import generate_pdf

sys.path.pop(0)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-2.5-flash"


def generate_report(company_data: dict) -> dict | None:

    print(f"\n[Report] Generating report for: {company_data.get('company_name')}")

    prompt = _build_prompt(company_data)

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw = response.text.strip()

    
        if raw.startswith("```"):

            raw = raw.replace("```json", "")
            raw = raw.replace("```", "")
            raw = raw.strip()

        result = json.loads(raw)

        print("[Report] Report generated ")

        return result

    except Exception as e:

        print(f"[Report] Failed: {e}")

        return None


def _build_prompt(data: dict) -> str:

    return f"""
You are a senior business consultant writing a professional audit report 
for a potential client.

Based on the company data below, generate a 
detailed, insightful, and personalized report.

COMPANY DATA:
{json.dumps(data, indent=2)}

Return ONLY a valid JSON object with these exact fields:

{{
  "executive_summary": "3-4 sentence personalized summary of the company",

  "company_overview": {{
      "description": "detailed paragraph about what they do",
      "industry": "their industry",
      "business_model": "how they make money",
      "target_market": "who their customers are"
  }},

  "strengths": [
      {{
          "title": "strength title",
          "detail": "2 sentence explanation"
      }}
  ],

  "opportunities": [
      {{
          "title": "opportunity title",
          "detail": "2 sentence explanation"
      }}
  ],

  "recommendations": [
      {{
          "title": "recommendation title",
          "detail": "2 sentence actionable advice"
      }}
  ],

  "market_positioning": "paragraph about where they stand in the market",

  "audit_score": {{
      "overall": 85,
      "digital_presence": 80,
      "market_fit": 90,
      "growth_potential": 85,
      "note": "one line explanation of the score"
  }},

  "closing_statement": "personalized closing paragraph to the prospect"
}}

Rules:
- Be specific to this company
- Never generic
- Use their actual services, customers, and strengths
- Recommendations must be actionable
- Return ONLY JSON
- No markdown
- No explanation
""".strip()

