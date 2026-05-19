

import httpx
import os

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}



def fetch_html(url: str) -> str | None:
    print(f"\n[Fetcher] Fetching: {url}")

    html = _try_normal(url)
    if html:
        print(f"[Fetcher] Normal fetch succeeded ")
        return html

  
    print("[Fetcher] Normal failed, trying with extra headers...")
    html = _try_with_extra_headers(url)
    if html:
        print(f"[Fetcher] Extra headers fetch succeeded ")
        return html

    print("[Fetcher] Trying /about page...")
    html = _try_normal(url.rstrip("/") + "/about")
    if html:
        print(f"[Fetcher] /about page fetch succeeded ")
        return html
    print("[Fetcher] All fetch attempts failed ")
    return None



def _try_normal(url: str) -> str | None:
    try:
        res = httpx.get(
            url,
            headers=HEADERS,
            timeout=10,
            follow_redirects=True,
        )
        if res.status_code == 200:
            return res.text
        print(f"[Fetcher] Status code: {res.status_code}")
    except Exception as e:
        print(f"[Fetcher] Normal request failed: {e}")
    return None



def _try_with_extra_headers(url: str) -> str | None:
    try:
        extra_headers = {
            **HEADERS,
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        res = httpx.get(
            url,
            headers=extra_headers,
            timeout=15,
            follow_redirects=True,
        )
        if res.status_code == 200:
            return res.text
        print(f"[Fetcher] Status code: {res.status_code}")
    except Exception as e:
        print(f"[Fetcher] Extra headers request failed: {e}")
    return None



