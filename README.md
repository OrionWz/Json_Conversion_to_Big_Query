# Json Conversion to BigQuery

Python pipeline that builds a **RandomUser** dataset (200+ synthetic profiles), **enriches** names with public APIs, stores everything in **SQLite**, exports **newline-delimited JSON (NDJSON)** for analytics, and can **load the file into Google BigQuery**.

## What it does

- Pulls profiles from the [RandomUser API](https://randomuser.me/api/) and flattens them into tabular fields.
- Calls [genderize.io](https://genderize.io/), [nationalize.io](https://nationalize.io/), and [agify.io](https://agify.io/) to add inferred gender, likely nationality, and estimated age from names (with caching so repeated names do not over-call the APIs).
- Loads rows into a local SQLite database (`sql/schema.sql`).
- Runs several analytical SQL queries from `sql/analysis_queries.sql` and prints summaries (gender vs inference, nationality confidence, age gaps, and similar).
- Writes `data/users.ndjson` for warehouse loads or ad hoc tools.
- Optional: uploads that NDJSON to BigQuery with schema autodetect.

Generated files live under `data/` and are listed in `.gitignore` so they are not committed by default.

## Requirements

- **Python 3.10+** (3.10+ recommended for `list[str]` typing used in the code).
- Internet access for the APIs above.
- For BigQuery only: a Google Cloud project and credentials ([Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) or a service-account JSON and `GOOGLE_APPLICATION_CREDENTIALS`).

## Setup

```bash
git clone https://github.com/OrionWz/Json_Conversion_to_Big_Query.git
cd Json_Conversion_to_Big_Query
python -m venv .venv
```

Activate the virtual environment:

- **Windows:** `.\.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the pipeline

Default run fetches **220** users, enriches them, rebuilds SQLite, exports NDJSON, and prints analytics:

```bash
python run_pipeline.py --count 220
```

### Command-line options

| Option | Description |
|--------|-------------|
| `--count N` | Number of RandomUser profiles (default `220`). |
| `--skip-enrichment` | Skip external enrichment APIs; enrichment columns stay `NULL`. |
| `--skip-export` | Do not write `data/users.ndjson`. |
| `--skip-analytics` | Do not run or print `sql/analysis_queries.sql`. |

Outputs (after a normal run):

- `data/users.db` — SQLite database  
- `data/users.ndjson` — one JSON object per line  

## Load into BigQuery

1. Authenticate (for example `gcloud auth application-default login`, or set `GOOGLE_APPLICATION_CREDENTIALS` to a service-account key).
2. Run the pipeline once so `data/users.ndjson` exists.
3. Set your project and run the uploader (Windows example):

```bash
set GCP_PROJECT=your-gcp-project-id
python upload_to_bigquery.py --dataset your_dataset --table random_users_enriched
```

Arguments:

- `--project` — GCP project ID (optional if `GCP_PROJECT` is set).
- `--dataset` — BigQuery dataset (created if missing, using `--location`, default `US`).
- `--table` — Destination table (default `random_users_enriched`).
- `--json-path` — Path to NDJSON (defaults to `data/users.ndjson`).

Each run replaces the destination table (`WRITE_TRUNCATE`).

## Project structure

```
├── run_pipeline.py          # Entry point: fetch → enrich → SQLite → export → analytics
├── upload_to_bigquery.py    # Optional BigQuery load from NDJSON
├── requirements.txt
├── pipeline/
│   ├── fetch_users.py       # RandomUser HTTP + flattening
│   ├── enrich.py            # genderize / nationalize / agify + caching
│   ├── database.py          # SQLite schema load, inserts, query runner
│   └── export.py            # NDJSON export from SQLite
└── sql/
    ├── schema.sql           # Table definition
    └── analysis_queries.sql # Example analytical queries
```
