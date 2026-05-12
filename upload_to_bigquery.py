"""Load newline-delimited JSON (from `data/users.ndjson`) into BigQuery.

Authentication:
  - Set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON path, or
  - Use `gcloud auth application-default login` for interactive local dev.

Example:
  python upload_to_bigquery.py --project my-gcp-project --dataset demo --table random_users
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from google.cloud import bigquery
from google.cloud.exceptions import NotFound


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=os.environ.get("GCP_PROJECT"), help="GCP project id")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--table", default="random_users_enriched")
    parser.add_argument(
        "--json-path",
        type=Path,
        default=Path(__file__).resolve().parent / "data" / "users.ndjson",
    )
    parser.add_argument(
        "--location",
        default="US",
        help="BigQuery dataset location (dataset is created if missing).",
    )
    args = parser.parse_args()

    if not args.project:
        raise SystemExit("Pass --project or set GCP_PROJECT in the environment.")

    if not args.json_path.is_file():
        raise SystemExit(f"Missing export file: {args.json_path} (run python run_pipeline.py first).")

    client = bigquery.Client(project=args.project, location=args.location)
    dataset_ref = f"{args.project}.{args.dataset}"

    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        ds = bigquery.Dataset(dataset_ref)
        ds.location = args.location
        client.create_dataset(ds)

    table_ref = f"{dataset_ref}.{args.table}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with args.json_path.open("rb") as handle:
        load_job = client.load_table_from_file(handle, table_ref, job_config=job_config)
    load_job.result()

    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_ref}.")


if __name__ == "__main__":
    main()
