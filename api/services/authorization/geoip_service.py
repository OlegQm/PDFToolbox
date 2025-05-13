import os
import geoip2.database
from pathlib import Path
from functools import lru_cache
from typing import Tuple

@lru_cache()
def get_reader() -> geoip2.database.Reader:
    db_path = Path(__file__).resolve().parents[2] / "geoip" / "GeoLite2-City.mmdb"
    return geoip2.database.Reader(str(db_path))

async def resolve_geo(ip: str) -> Tuple[str, str]:
    """
    По IP берёт город и страну из локальной MaxMind GeoLite2 City.
    """
    try:
        reader = get_reader()
        resp = reader.city(ip)
        city = resp.city.name or ""
        country = resp.country.name or ""
        return resp
    except Exception as e:
        return e
