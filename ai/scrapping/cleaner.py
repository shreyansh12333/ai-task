

import re


def clean_data(extracted: dict) -> dict | None:
    print(f"\n[Cleaner] Starting cleaning...")

    if not extracted:
        print("[Cleaner] No data to clean ")
        return None

    cleaned = {
        "title":       _clean_text(extracted.get("title", "")),
        "description": _clean_text(extracted.get("description", "")),
        "body_text":   _clean_body(extracted.get("body_text", "")),
        "nav_links":   _clean_links(extracted.get("nav_links", [])),
    }

    print(f"[Cleaner] Cleaning complete ")
    return cleaned


def _clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.strip()
    return text



def _is_similar(line: str, seen: set) -> bool:
    line_words = set(line.lower().split())
    for seen_line in seen:
        seen_words = set(seen_line.lower().split())
        if len(line_words) == 0:
            continue
        overlap = len(line_words & seen_words) / len(line_words)
        if overlap > 0.8:
            return True
    return False



def _clean_body(body: str) -> str:
    if not body:
        return ""

    lines   = body.split("\n")
    seen    = set()
    cleaned = []

    for line in lines:
        line = _clean_text(line)

        
        if not line:
            continue

        
        if len(line) < 60:
            continue

        
        if re.match(r'^[\d\s\W]+$', line):
            continue

        if line in seen or _is_similar(line, seen):
            continue

        seen.add(line)
        cleaned.append(line)

    return "\n".join(cleaned)

def _clean_links(links: list) -> list:
    if not links:
        return []

    skip_patterns = [
        r'\.(png|jpg|jpeg|gif|svg|css|js|ico)$',
        r'^/cdn',
        r'^/static',
        r'#',
        r'\?',
        r'/customers/',
        r'/blog/',
    ]

    cleaned = []
    for link in links:
        should_skip = any(re.search(p, link) for p in skip_patterns)
        if not should_skip:
            cleaned.append(link)

    return sorted(set(cleaned))



