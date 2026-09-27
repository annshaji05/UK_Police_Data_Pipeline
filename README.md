# London Crime Data Pipeline

## About Me
Hi, I'm Ann. I recently graduated with a First Class Honours degree in Computer Science from London South Bank University. My final year project involved building an end-to-end machine learning pipeline to predict student academic outcomes using the Open University Learning Analytics Dataset (OULAD) — covering feature engineering, preprocessing, and comparing Logistic Regression, Random Forest, and Gradient Boosting models, achieving 89.61% accuracy with Gradient Boosting. I built an interactive Streamlit application around it so users could input student data and get live predictions, and integrated a locally hosted vision-language model (via LM Studio) for AI-powered image analysis within the app.

Alongside that, I've built a course management backend using Java and Spring Boot with RESTful APIs, JPA, and H2 for structured data storage, and designed a fully normalised (BCNF-compliant) relational database with complex SQL queries, joins, triggers, and stored procedures.

This project builds on that same interest — turning raw data into something genuinely usable through a clear, well-engineered pipeline — this time applied to real-world public safety data rather than academic data, and with a stronger focus on the data engineering side: raw data handling, a proper local database, and clean, reproducible transformations.

## Purpose
This project is a small end-to-end data pipeline that pulls real, publicly available UK crime data, stores it properly (raw and cleaned), and presents it through an interactive dashboard. It was built as part of my application to The Information Lab's Data Engineering Consultant role, to demonstrate real data engineering decisions: handling raw data responsibly, modelling it cleanly, and building something genuinely usable from it.

The dashboard is aimed at an analyst-style audience — someone comparing crime patterns across different London areas and time periods, rather than just checking crime near a single address.

## Data Source
- **API:** [UK Police Data API](https://data.police.uk/docs/method/crime-street/) — an open, official government data source (data.police.uk)
- **Endpoint used:** `crimes-street/all-crime` — returns street-level crime data within roughly a 1-mile radius of a given coordinate, for a given month
- **Authentication:** None required — this API is fully open, so no credentials were needed or stored
- **Pagination:** This endpoint has no pagination — it returns the complete result set for a single point in one response. Its only volume limit applies to custom polygon queries exceeding 10,000 crimes (returns a 503 error), which doesn't apply to the single-point queries used here
- **Rate limits:** No official hard limit is published, but the fetch script adds a 1-second pause between requests to avoid hammering the public API unnecessarily

**Data collected:** 4 London areas, chosen to represent contrasting crime environments — Westminster/Covent Garden (tourist/nightlife), City of London (financial district), Hackney (dense residential), and Richmond upon Thames (affluent, quieter) — across 3 months (May, June, July 2026).

## Pipeline Overview

The pipeline is split into clear, separate stages:

1. **`fetch_raw.py`** — Calls the API for each area/month combination (4 areas × 3 months = 12 calls) and saves each response completely untouched as a timestamped JSON file in `raw_data/`. This preserves an unmodified record of exactly what the API returned, and means the entire pipeline can be rebuilt from scratch without needing to re-call the API.

2. **`load_raw.py`** — Loads every raw JSON file in `raw_data/` into a local DuckDB database (`police_data.duckdb`), into a table called `raw_crimes`. DuckDB reads the nested JSON structure automatically, so this stage does not transform the data at all — it's a straight load.

3. **`clean_data.py`** — Builds a second table, `crimes_clean`, using SQL run inside DuckDB. This stage:
   - Extracts the area name from each file's filename
   - Flattens nested fields (e.g. `location.latitude` → `latitude`)
   - Converts latitude/longitude from text to proper numeric types
   - Removes exact duplicate rows
   - Replaces missing outcome statuses with a clear `"Under investigation"` label instead of leaving nulls
   - Filters out any row with a missing ID

4. **`dashboard.py`** — A Streamlit app that reads from `crimes_clean` and presents:
   - Sidebar filters (area, month, crime category)
   - Summary metrics (total crimes, most common category)
   - Bar charts comparing areas and crime categories
   - A line chart showing monthly trends by area
   - A colour-coded interactive map of crime locations
   - An expandable raw data table

```
raw_data/*.json  →  DuckDB "raw_crimes" (untouched)  →  DuckDB "crimes_clean" (flattened, deduped, typed)  →  Streamlit dashboard
```

## How to Run This Project

**1. Clone the repository**
```
git clone https://github.com/annshaji05/UK_Police_Data_Pipeline.git
cd UK_Police_Data_Pipeline
```

**2. Create and activate a virtual environment**
```
python -m venv .venv
.venv\Scripts\activate
```
*(On Mac/Linux, use `source .venv/bin/activate` instead)*

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Run the pipeline, in order**
```
python fetch_raw.py
python load_raw.py
python clean_data.py
```

**5. Launch the dashboard**
```
streamlit run dashboard.py
```
This will open automatically in your browser.

## Future Improvements
- Add more months of historical data to show longer-term trends
- Add more London areas, or expand to other UK police forces, for wider comparison
- Add automated tests to check the cleaning logic (e.g. no nulls in key columns, no duplicate IDs)
- Schedule `fetch_raw.py` to run automatically (e.g. monthly), so the dashboard stays up to date without manual re-running
- Add outcome-rate analysis (e.g. % of crimes resulting in a charge, by area/category)
- Deploy the dashboard online (e.g. Streamlit Community Cloud) so it doesn't need to be run locally
