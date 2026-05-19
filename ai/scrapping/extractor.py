
from bs4 import BeautifulSoup


def extract_text(html: str) -> dict | None:
    print(f"\n[Extractor] Starting extraction...")

    if not html:
        print("[Extractor] No HTML provided ❌")
        return None

    soup = BeautifulSoup(html, "html.parser")

    _remove_garbage(soup)

    result = {
        "title":       _get_title(soup),
        "description": _get_description(soup),
        "body_text":   _get_body_text(soup),
        "nav_links":   _get_nav_links(soup),
    }

    print(f"[Extractor] Extraction complete ✅")
    return result


def _remove_garbage(soup: BeautifulSoup) -> None:
    garbage_tags = [
        "script", "style", "noscript",
        "header", "footer", "nav",
        "iframe", "svg", "img",
        "form", "button", "input",
        "cookie", "popup", "ads",
    ]
    for tag in garbage_tags:
        for element in soup.find_all(tag):
            element.decompose()



def _get_title(soup: BeautifulSoup) -> str:
    tag = soup.find("title")
    if tag:
        return tag.get_text(strip=True)
    return ""



def _get_description(soup: BeautifulSoup) -> str:
 
    tag = soup.find("meta", attrs={"name": "description"})
    if tag and tag.get("content"):
        return tag["content"].strip()

    tag = soup.find("meta", attrs={"property": "og:description"})
    if tag and tag.get("content"):
        return tag["content"].strip()

    return ""



def _get_body_text(soup: BeautifulSoup) -> str:
    content_tags = soup.find_all(["p", "h1", "h2", "h3", "li"])

    lines = []
    for tag in content_tags:
        text = tag.get_text(strip=True)
        if len(text) > 30:
            lines.append(text)

    return "\n".join(lines)



def _get_nav_links(soup: BeautifulSoup) -> list[str]:
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") and len(href) > 1:
            links.append(href)
    return list(set(links))


if __name__ == "__main__":
    from discovery import discover_url
    from fetcher import fetch_html

    company = "Stripe"

    url  = discover_url(company)
    html = fetch_html(url)
    data = extract_text(html)

    if data:
        print("\n── Title ──")
        print(data["title"])

        print("\n── Description ──")
        print(data["description"])

        print("\n── Body Text (first 500 chars) ──")
        print(data["body_text"][:500])

        print("\n── Nav Links ──")
        print(data["nav_links"][:10])