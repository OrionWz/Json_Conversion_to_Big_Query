"""SQLite load + ad-hoc analytics."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any, Iterable

_QUERY_TITLE = re.compile(r"^--\s*\d+\)\s*(.*)$")


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection, schema_sql: str) -> None:
    conn.executescript(schema_sql)
    conn.commit()


def insert_users(conn: sqlite3.Connection, users: Iterable[dict[str, Any]]) -> None:
    sql = """
        INSERT OR REPLACE INTO users (
            randomuser_id, title, first_name, last_name, email,
            gender_reported, date_of_birth, age_reported, phone, cell,
            nationality_code, city, state, country, postcode,
            street_number, street_name, picture_large,
            gender_inferred, gender_probability,
            age_inferred, age_inferred_count,
            nationality_inferred, nationality_probability
        ) VALUES (
            :randomuser_id, :title, :first_name, :last_name, :email,
            :gender_reported, :date_of_birth, :age_reported, :phone, :cell,
            :nationality_code, :city, :state, :country, :postcode,
            :street_number, :street_name, :picture_large,
            :gender_inferred, :gender_probability,
            :age_inferred, :age_inferred_count,
            :nationality_inferred, :nationality_probability
        )
    """
    conn.executemany(sql, list(users))
    conn.commit()


def run_query(conn: sqlite3.Connection, sql: str) -> list[sqlite3.Row]:
    cur = conn.execute(sql)
    return cur.fetchall()


def print_rows(title: str, rows: list[sqlite3.Row], limit: int | None = 30) -> None:
    print(f"\n=== {title} ===")
    if not rows:
        print("(no rows)")
        return
    cols = rows[0].keys()
    header = " | ".join(cols)
    print(header)
    print("-" * len(header))
    for i, row in enumerate(rows):
        if limit is not None and i >= limit:
            print(f"... ({len(rows) - limit} more rows)")
            break
        print(" | ".join(str(row[c]) for c in cols))


def load_analysis_query_blocks(path: Path) -> list[tuple[str, str]]:
    """Split `sql/analysis_queries.sql` on `-- N) Title` banner lines."""
    text = path.read_text(encoding="utf-8")
    blocks: list[tuple[str, str]] = []
    current_title = "query"
    current_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        m = _QUERY_TITLE.match(stripped)
        if m:
            if current_lines:
                stmt = "\n".join(current_lines).strip().rstrip(";")
                if stmt:
                    blocks.append((current_title, stmt))
                current_lines = []
            current_title = (m.group(1) or "").strip() or "query"
        elif stripped.startswith("--"):
            continue
        else:
            current_lines.append(line)
    if current_lines:
        stmt = "\n".join(current_lines).strip().rstrip(";")
        if stmt:
            blocks.append((current_title, stmt))
    return blocks
