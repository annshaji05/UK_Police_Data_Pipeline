import duckdb
import glob

con = duckdb.connect("police_data.duckdb")

raw_files = glob.glob("raw_data/*.json")
print("Found raw files:", len(raw_files))

# filename=True adds a "filename" column so we know which raw file each row came from.
# This lets us later extract the area name and month from the filename itself.
con.execute(f"""
    CREATE OR REPLACE TABLE raw_crimes AS
    SELECT * FROM read_json_auto({raw_files}, filename=True)
""")

row_count = con.execute("SELECT COUNT(*) FROM raw_crimes").fetchone()[0]
print(f"Loaded {row_count} rows into raw_crimes")

columns = con.execute("DESCRIBE raw_crimes").fetchall()
print("\nColumns in raw_crimes:")
for col in columns:
    print(col)

con.close()