# services/authorization/geoip_service.py
import os
import httpx
from functools import lru_cache
from typing import Tuple

@lru_cache()
def get_geoip_api_url() -> str:
    return os.getenv("GEOIP_API_URL", "https://ipapi.co")

async def resolve_geo(ip: str) -> Tuple[str, str]:
    """
    Returns (city, country_name) by IP.
    If something goes wrong, returns empty strings.
    """
    url = f"{get_geoip_api_url()}/{ip}/json/"
    print("URL:", url)
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            r = await client.get(url)
            data = r.json()
            return data
    except Exception as e:
        return e
