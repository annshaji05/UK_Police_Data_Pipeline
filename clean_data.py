import duckdb

con = duckdb.connect("police_data.duckdb")

# Build a clean, flattened table from the raw nested data.
# We pull fields out of the nested STRUCT columns (location, outcome_status),
# rename them clearly, and cast types properly.
con.execute("""
    CREATE OR REPLACE TABLE crimes_clean AS
    SELECT DISTINCT
        id,
        category,
        month,
        CAST(location.latitude AS DOUBLE) AS latitude,
        CAST(location.longitude AS DOUBLE) AS longitude,
        location.street.name AS street_name,
        COALESCE(outcome_status.category, 'Under investigation') AS outcome_category
    FROM raw_crimes
    WHERE id IS NOT NULL
""")

# Sanity checks
row_count = con.execute("SELECT COUNT(*) FROM crimes_clean").fetchone()[0]
print(f"crimes_clean has {row_count} rows")

print("\nSample rows:")
sample = con.execute("SELECT * FROM crimes_clean LIMIT 5").fetchall()
for row in sample:
    print(row)

print("\nCrime counts by category:")
counts = con.execute("""
    SELECT category, COUNT(*) as total
    FROM crimes_clean
    GROUP BY category
    ORDER BY total DESC
""").fetchall()
for row in counts:
    print(row)

con.close()