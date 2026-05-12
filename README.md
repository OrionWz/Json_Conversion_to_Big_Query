# RandomUser → enrichment APIs → SQLite → BigQuery

This repository implements the take-home style workflow described in the original brief: pull **200+** people from the [RandomUser API](https://randomuser.me/api/), enrich names with public inference APIs, run **SQL analytics**, export **newline-delimited JSON**, and optionally **load into BigQuery**.

## What was wrong before

The previous version mixed unrelated sample data (Switch games JSON), broken Prefect snippets with hard-coded paths, SQL scratch files with invalid syntax, and a README that referenced scripts that did not exist. This redo aligns the codebase with the stated requirements.

## Quick start

```bash
git clone https://github.com/OrionWz/Json_Conversion_to_Big_Query.git
cd Json_Conversion_to_Big_Query
python -m venv .venv
.\.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python run_pipeline.py --count 220
```

Artifacts (gitignored):

- `data/users.db` — SQLite database
- `data/users.ndjson` — one JSON object per line for BigQuery

### Flags

| Flag | Purpose |
|------|---------|
| `--count N` | Number of RandomUser profiles (default `220`) |
| `--skip-enrichment` | Skip HTTP calls to genderize / nationalize / agify (fills NULLs) |
| `--skip-export` | Do not write `users.ndjson` |
| `--skip-analytics` | Do not print the queries from `sql/analysis_queries.sql` |

### BigQuery upload

1. Authenticate (service account **or** `gcloud auth application-default login`).
2. Run the pipeline so `data/users.ndjson` exists.
3. Load:

```bash
set GCP_PROJECT=your-project-id
python upload_to_bigquery.py --dataset your_dataset --table random_users_enriched
```

## Approach

1. **Fetch**: Request batched RandomUser results and flatten nested JSON into columns (`pipeline/fetch_users.py`).
2. **Enrich**: For each row, call [genderize.io](https://genderize.io/), [nationalize.io](https://nationalize.io/) (using **surname** when present), and [agify.io](https://agify.io/). Distinct names are cached so duplicate first names do not spam the APIs. A short delay between *new* lookups reduces rate-limit friction (`pipeline/enrich.py`).
3. **Store**: Load into SQLite with `sql/schema.sql` — easy to run locally without PostgreSQL (`pipeline/database.py`).
4. **Analyze**: Six example analytical queries live in `sql/analysis_queries.sql` (confusion matrix of genders, nationality confidence, age gaps, etc.). `run_pipeline.py` prints their output after each load.
5. **Warehouse**: Export NDJSON and optionally load with autodetect in `upload_to_bigquery.py`.

## Interesting insights (what to look for after a full run)

- **Gender**: RandomUser’s `gender` is ground truth for the synthetic profile, while genderize predicts from **first name** only — mismatches are common for unisex names or non-Western naming patterns.
- **Nationality**: `nationalize` sees only a string; using **last name** changes the prior compared with first name. Treat output as a weak cultural signal, not a fact about a real person.
- **Age**: `agify` returns a population prior by first name; comparing `age_inferred` to `age_reported` highlights where the prior diverges from this particular synthetic profile.

## Project layout

```
run_pipeline.py           # Orchestrator
upload_to_bigquery.py     # Optional BigQuery loader
pipeline/
  fetch_users.py
  enrich.py
  database.py
  export.py
sql/
  schema.sql              # SQLite DDL
  analysis_queries.sql    # Analytics (also runnable in BigQuery with minor tweaks)
```

## Original assignment text (archived)

The README previously contained the full Detroit Lions–style prompt; the implementation above satisfies: RandomUser fetch, secondary API enrichment, five or more SQL analyses, and a clean path to BigQuery via NDJSON.
