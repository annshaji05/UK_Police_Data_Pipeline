import duckdb

con = duckdb.connect("police_data.duckdb")

con.execute(r"""
    CREATE OR REPLACE TABLE crimes_clean AS
    SELECT DISTINCT
        id,
        category,
        month,
        split_part(regexp_extract(filename, 'crimes_([a-z_]+)_\d{4}-\d{2}', 1), '_2026', 1) AS area,
        CAST(location.latitude AS DOUBLE) AS latitude,
        CAST(location.longitude AS DOUBLE) AS longitude,
        location.street.name AS street_name,
        COALESCE(outcome_status.category, 'Under investigation') AS outcome_category
    FROM raw_crimes
    WHERE id IS NOT NULL
""")

row_count = con.execute("SELECT COUNT(*) FROM crimes_clean").fetchone()[0]
print(f"crimes_clean has {row_count} rows")

print("\nSample rows:")
sample = con.execute("SELECT * FROM crimes_clean LIMIT 5").fetchall()
for row in sample:
    print(row)

print("\nRows per area:")
by_area = con.execute("""
    SELECT area, COUNT(*) as total
    FROM crimes_clean
    GROUP BY area
    ORDER BY total DESC
""").fetchall()
for row in by_area:
    print(row)

print("\nRows per area per month:")
by_area_month = con.execute("""
    SELECT area, month, COUNT(*) as total
    FROM crimes_clean
    GROUP BY area, month
    ORDER BY area, month
""").fetchall()
for row in by_area_month:
    print(row)

con.close()