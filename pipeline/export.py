"""Export SQLite rows to newline-delimited JSON for BigQuery loads."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def export_users_ndjson(conn: sqlite3.Connection, out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cur = conn.execute(
        """
        SELECT
            randomuser_id, title, first_name, last_name, email,
            gender_reported, date_of_birth, age_reported, phone, cell,
            nationality_code, city, state, country, postcode,
            street_number, street_name, picture_large,
            gender_inferred, gender_probability,
            age_inferred, age_inferred_count,
            nationality_inferred, nationality_probability
        FROM users
        ORDER BY id
        """
    )
    n = 0
    with out_path.open("w", encoding="utf-8") as f:
        while True:
            row = cur.fetchone()
            if row is None:
                break
            payload = {k: row[k] for k in row.keys()}
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            n += 1
    return n
