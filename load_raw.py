import duckdb
import glob

# Connect to (or create) a DuckDB database file called "police_data.duckdb"
con = duckdb.connect("police_data.duckdb")

# Find all raw JSON files we've saved so far
raw_files = glob.glob("raw_data/*.json")
print("Found raw files:", raw_files)

# DuckDB can read JSON files directly and turn them into a table.
# We use read_json_auto, which figures out the structure automatically.
# This creates (or replaces) a table called "raw_crimes" containing
# every record from every raw file we've collected.
con.execute(f"""
    CREATE OR REPLACE TABLE raw_crimes AS
    SELECT * FROM read_json_auto({raw_files})
""")

# Quick sanity check: how many rows did we load, and what do the columns look like?
row_count = con.execute("SELECT COUNT(*) FROM raw_crimes").fetchone()[0]
print(f"Loaded {row_count} rows into raw_crimes")

columns = con.execute("DESCRIBE raw_crimes").fetchall()
print("\nColumns in raw_crimes:")
for col in columns:
    print(col)

con.close()