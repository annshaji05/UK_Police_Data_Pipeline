import streamlit as st
import duckdb
import plotly.express as px

# Page setup
st.set_page_config(page_title="UK Police Crime Dashboard", layout="wide")
st.title("🚓 London Crime Dashboard")
st.caption("Street-level crime data from data.police.uk — Westminster, City of London, Hackney, and Richmond upon Thames (May–July 2026)")

# Connect to DuckDB database and load the clean table
con = duckdb.connect("police_data.duckdb", read_only=True)
df = con.execute("SELECT * FROM crimes_clean").df()
con.close()

# --- Sidebar filters ---
st.sidebar.header("Filters")

areas = sorted(df["area"].unique())
selected_areas = st.sidebar.multiselect("Area", areas, default=areas)

months = sorted(df["month"].unique())
selected_months = st.sidebar.multiselect("Month", months, default=months)

categories = sorted(df["category"].unique())
selected_categories = st.sidebar.multiselect("Crime category", categories, default=categories)

# Apply filters
filtered = df[
    df["area"].isin(selected_areas) &
    df["month"].isin(selected_months) &
    df["category"].isin(selected_categories)
]

# --- Summary metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total crimes", f"{len(filtered):,}")
col2.metric("Areas selected", len(selected_areas))
if len(filtered) > 0:
    top_category = filtered["category"].value_counts().idxmax()
    col3.metric("Most common category", top_category)

st.divider()

# --- Chart 1: Crimes by area ---
st.subheader("Crimes by area")
by_area = filtered.groupby("area").size().reset_index(name="count")
fig_area = px.bar(by_area, x="area", y="count", color="area")
st.plotly_chart(fig_area, use_container_width=True)

# --- Chart 2: Crimes by category ---
st.subheader("Crimes by category")
by_category = filtered.groupby("category").size().reset_index(name="count").sort_values("count", ascending=False)
fig_category = px.bar(by_category, x="category", y="count")
st.plotly_chart(fig_category, use_container_width=True)

# --- Chart 3: Trend over time by area ---
st.subheader("Monthly trend by area")
by_month_area = filtered.groupby(["month", "area"]).size().reset_index(name="count")
fig_trend = px.line(by_month_area, x="month", y="count", color="area", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# --- Map (basemap, colored by area) ---
st.subheader("Crime locations")
if len(filtered) > 0:
    area_colors = {
        "westminster": [255, 0, 0],
        "city_of_london": [0, 128, 255],
        "hackney": [0, 200, 0],
        "richmond": [255, 165, 0],
    }
    map_df = filtered[["latitude", "longitude", "area"]].rename(columns={"latitude": "lat", "longitude": "lon"})
    map_df["color"] = map_df["area"].map(area_colors)

    st.map(map_df, latitude="lat", longitude="lon", color="color", zoom=10)

    st.caption("🔴 Westminster · 🔵 City of London · 🟢 Hackney · 🟠 Richmond")
else:
    st.info("No data matches the current filters.")

# --- Raw data table ---
with st.expander("View raw filtered data"):
    st.dataframe(filtered)