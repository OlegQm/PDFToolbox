import geoip2.database
from pathlib import Path
from functools import lru_cache
from typing import Tuple

@lru_cache()
def get_reader() -> geoip2.database.Reader:
    """
    Returns a cached instance of the GeoIP2 database reader.

    This function uses an LRU (Least Recently Used) cache to store and reuse
    the GeoIP2 database reader instance, which provides efficient access to
    geolocation data. The database file is expected to be located in the
    `geoip` directory two levels above the current file's directory, with
    the filename `GeoLite2-City.mmdb`.

    Returns:
        geoip2.database.Reader: An instance of the GeoIP2 database reader.

    Raises:
        FileNotFoundError: If the GeoLite2-City.mmdb file is not found at the
            expected location.
    """
    db_path = Path(__file__).resolve().parents[2] / "geoip" / "GeoLite2-City.mmdb"
    return geoip2.database.Reader(str(db_path))

async def resolve_geo(ip: str) -> Tuple[str, str]:
    """
    Returns a tuple (city_name, country_name) based on the IP.
    If nothing is found, both values will be "".
    """
    try:
        resp = get_reader().city(ip)
        city = (
            resp.city.names.get("en", "Unknown city")
            or resp.city.name
            or "Unknown city"
        )
        country = (
            resp.country.names.get("en", "Unknown country")
            or resp.country.name
            or "Unknown country"
        )
        return city, country
    except Exception:
        return "Unknown city", "Unknown country"
