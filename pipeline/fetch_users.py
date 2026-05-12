"""Download random profiles from https://randomuser.me/api/ and normalize fields."""

from __future__ import annotations

from typing import Any

import requests

RANDOMUSER_URL = "https://randomuser.me/api/"


def fetch_random_users(count: int = 220) -> list[dict[str, Any]]:
    """Request `count` users in as few HTTP calls as possible (API cap: 5000 per call)."""
    if count < 1:
        raise ValueError("count must be >= 1")
    out: list[dict[str, Any]] = []
    remaining = count
    while remaining > 0:
        batch = min(5000, remaining)
        resp = requests.get(RANDOMUSER_URL, params={"results": batch}, timeout=120)
        resp.raise_for_status()
        payload = resp.json()
        chunk = payload.get("results") or []
        if not chunk:
            break
        out.extend(chunk)
        remaining = count - len(out)
    return out[:count]


def flatten_randomuser_record(u: dict[str, Any]) -> dict[str, Any]:
    """Map nested RandomUser JSON into flat columns for SQLite / BigQuery."""
    name = u.get("name") or {}
    loc = u.get("location") or {}
    street = loc.get("street") or {}
    dob = u.get("dob") or {}
    pic = u.get("picture") or {}

    if isinstance(street, dict):
        street_number = street.get("number")
        street_name = street.get("name")
    else:
        street_number, street_name = None, None

    login = u.get("login") or {}
    uid = login.get("uuid") or u.get("id", {}).get("value") or login.get("username")
    if not uid:
        raise ValueError("RandomUser record missing a stable id (login.uuid)")

    age_val = dob.get("age")
    try:
        age_reported = int(age_val) if age_val is not None else None
    except (TypeError, ValueError):
        age_reported = None

    return {
        "randomuser_id": str(uid),
        "title": name.get("title"),
        "first_name": (name.get("first") or "").strip(),
        "last_name": (name.get("last") or "").strip(),
        "email": u.get("email"),
        "gender_reported": u.get("gender"),
        "date_of_birth": dob.get("date"),
        "age_reported": age_reported,
        "phone": u.get("phone"),
        "cell": u.get("cell"),
        "nationality_code": u.get("nat"),
        "city": loc.get("city"),
        "state": loc.get("state"),
        "country": loc.get("country"),
        "postcode": str(loc.get("postcode")) if loc.get("postcode") is not None else None,
        "street_number": str(street_number) if street_number is not None else None,
        "street_name": street_name,
        "picture_large": pic.get("large"),
    }
