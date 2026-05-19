import httpx
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY", "")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def _try_serpapi(company_name: str) -> str | None:
    try:
        res = httpx.get(
            "https://serpapi.com/search",
            params={
                "q": f"{company_name} official website",
                "api_key": SERP_API_KEY,
                "num": 3,
            },
            timeout=10,
        )
        results = res.json().get("organic_results", [])
        if results:
            return results[0].get("link")
    except Exception as e:
        print(f"[Discovery] SerpAPI failed: {e}")
    return None



def _try_duckduckgo(company_name: str) -> str | None:
    try:
        res = httpx.get(
            "https://html.duckduckgo.com/html/",
            params={"q": f"{company_name} official website"},
            headers=HEADERS,
            timeout=10,
        )
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.select(".result__url")
        if results:
            url = results[0].get_text(strip=True)
            if not url.startswith("http"):
                url = "https://" + url
            return url
    except Exception as e:
        print(f"[Discovery] DuckDuckGo failed: {e}")
    return None



def _try_guess(company_name: str) -> str | None:
    slug = company_name.lower().replace(" ", "")
    candidates = [
        f"https://www.{slug}.com",
        f"https://{slug}.io",
        f"https://www.{slug}.co",
        f"https://get{slug}.com",
        f"https://{slug}.ai",
    ]
    for url in candidates:
        try:
            res = httpx.get(url, headers=HEADERS, timeout=6, follow_redirects=True)
            if res.status_code == 200:
                print(f"[Discovery] Guessed URL: {url}")
                return url
        except:
            continue
    return None



def discover_url(company_name: str) -> str | None:
    print(f"\n[Discovery] Searching for: {company_name}")

    url = _try_serpapi(company_name)
    if url:
        print(f"[Discovery] SerpAPI hit: {url}")
        return url

    print("[Discovery] SerpAPI failed, trying DuckDuckGo...")
    url = _try_duckduckgo(company_name)
    if url:
        print(f"[Discovery] DuckDuckGo hit: {url}")
        return url

    print("[Discovery] DuckDuckGo failed, guessing URL...")
    url = _try_guess(company_name)
    if url:
        return url

    print("[Discovery] All methods failed. Returning None.")
    return None

if __name__ == "__main__":
    companies = ["Stripe", "Notion", "Some Random Fake Company XYZ"]
    for company in companies:
        url = discover_url(company)
        print(f"Result → {url}\n")