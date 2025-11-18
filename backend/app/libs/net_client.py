from __future__ import annotations
import random, time
import httpx
from typing import Optional

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
]

def pick_ua() -> str:
    return random.choice(UA_POOL)

def client(base: str | None = None, referer: str | None = None):
    headers = {"User-Agent": pick_ua()}
    if referer:
        headers["Referer"] = referer
    return httpx.Client(
        base_url=base,
        headers=headers,
        follow_redirects=True,
        timeout=15.0
    )

def get(url: str, referer: str | None = None, tries: int = 3, sleep: float = 1.2):
    """Make GET request with retry and anti-ban measures"""
    last = None
    for i in range(tries):
        try:
            with client(referer=referer) as c:
                r = c.get(url)
                if r.status_code in (200, 302):
                    return r
                last = r
        except Exception as e:
            last = e
        time.sleep(sleep * (i + 1))
    raise RuntimeError(f"GET fail: {url} last={last}")
