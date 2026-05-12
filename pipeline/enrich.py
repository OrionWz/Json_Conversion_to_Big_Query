"""Call genderize.io, nationalize.io, and agify.io with simple caching and pacing."""

from __future__ import annotations

import time
from typing import Any

import requests

# Polite delay between unique API lookups (public tiers are rate-limited).
REQUEST_DELAY_SEC = 0.35


def _get_json(url: str, params: dict[str, Any], session: requests.Session) -> dict[str, Any] | None:
    try:
        r = session.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None


def enrich_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Mutates copies: adds gender_inferred, nationality_inferred, age_inferred, etc."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Json_Conversion_to_Big_Query/1.0"})

    gender_cache: dict[str, dict[str, Any]] = {}
    nation_cache: dict[str, dict[str, Any]] = {}
    agify_cache: dict[str, dict[str, Any]] = {}

    out: list[dict[str, Any]] = []
    for base in rows:
        row = dict(base)
        first = (row.get("first_name") or "").strip()
        last = (row.get("last_name") or "").strip()

        gkey = first.lower()
        if gkey and gkey not in gender_cache:
            data = _get_json("https://api.genderize.io", {"name": first}, session)
            gender_cache[gkey] = data or {}
            time.sleep(REQUEST_DELAY_SEC)
        ginfo = gender_cache.get(gkey) or {}
        row["gender_inferred"] = ginfo.get("gender")
        row["gender_probability"] = ginfo.get("probability")

        nkey = last.lower() if last else first.lower()
        if nkey and nkey not in nation_cache:
            # Nationalize expects a *name*; surnames are commonly used for country priors.
            data = _get_json("https://api.nationalize.io", {"name": last or first}, session)
            nation_cache[nkey] = data or {}
            time.sleep(REQUEST_DELAY_SEC)
        ninfo = nation_cache.get(nkey) or {}
        country = None
        prob = None
        top = ninfo.get("country")
        if isinstance(top, list) and top:
            country = top[0].get("country_id")
            prob = top[0].get("probability")
        row["nationality_inferred"] = country
        row["nationality_probability"] = prob

        akey = first.lower()
        if akey and akey not in agify_cache:
            data = _get_json("https://api.agify.io", {"name": first}, session)
            agify_cache[akey] = data or {}
            time.sleep(REQUEST_DELAY_SEC)
        ainfo = agify_cache.get(akey) or {}
        row["age_inferred"] = ainfo.get("age")
        row["age_inferred_count"] = ainfo.get("count")

        out.append(row)

    return out
