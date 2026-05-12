"""End-to-end: RandomUser -> enrichment APIs -> SQLite -> NDJSON export + SQL analytics."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.database import (
    connect,
    init_schema,
    insert_users,
    load_analysis_query_blocks,
    print_rows,
    run_query,
)
from pipeline.enrich import enrich_rows
from pipeline.export import export_users_ndjson
from pipeline.fetch_users import fetch_random_users, flatten_randomuser_record


def main() -> None:
    parser = argparse.ArgumentParser(description="Build enriched RandomUser dataset locally.")
    parser.add_argument("--count", type=int, default=220, help="Number of RandomUser profiles (>=200 for the assignment).")
    parser.add_argument(
        "--skip-enrichment",
        action="store_true",
        help="Skip genderize/nationalize/agify calls (DB will have NULL enrichment columns).",
    )
    parser.add_argument("--skip-export", action="store_true", help="Do not write NDJSON after loading SQLite.")
    parser.add_argument("--skip-analytics", action="store_true", help="Do not run sql/analysis_queries.sql blocks.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "users.db"
    ndjson_path = data_dir / "users.ndjson"
    schema_path = root / "sql" / "schema.sql"
    analysis_path = root / "sql" / "analysis_queries.sql"

    print(f"Fetching {args.count} users from RandomUser...")
    raw = fetch_random_users(args.count)
    rows = [flatten_randomuser_record(u) for u in raw]
    print(f"Flattened {len(rows)} records.")

    if args.skip_enrichment:
        for r in rows:
            r.setdefault("gender_inferred", None)
            r.setdefault("gender_probability", None)
            r.setdefault("nationality_inferred", None)
            r.setdefault("nationality_probability", None)
            r.setdefault("age_inferred", None)
            r.setdefault("age_inferred_count", None)
    else:
        print("Enriching with genderize.io / nationalize.io / agify.io (cached per distinct name)...")
        rows = enrich_rows(rows)

    schema_sql = schema_path.read_text(encoding="utf-8")
    conn = connect(db_path)
    init_schema(conn, schema_sql)
    insert_users(conn, rows)
    print(f"SQLite database written to {db_path} ({len(rows)} rows).")

    if not args.skip_export:
        n = export_users_ndjson(conn, ndjson_path)
        print(f"Exported {n} rows to {ndjson_path} (newline-delimited JSON for BigQuery).")

    if not args.skip_analytics:
        for title, sql in load_analysis_query_blocks(analysis_path):
            result = run_query(conn, sql)
            print_rows(title, result, limit=40)

    conn.close()


if __name__ == "__main__":
    main()
