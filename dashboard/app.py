from pathlib import Path
import glob
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import streamlit.components.v1 as components


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"

st.set_page_config(
    page_title="CrashMap",
    page_icon="🚧",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🚧 CrashMap")

st.caption(
    "Road Accident Analysis and Hotspot Detection using Hadoop, Hive and PySpark"
)


# ---------------------------------------------------------
# LOAD PYSPARK OUTPUT
# ---------------------------------------------------------

def load_result(folder):
    files = glob.glob(str(OUTPUT / folder / "part-*.csv"))

    if not files:
        st.error(f"No PySpark output found for {folder}.")
        st.stop()

    return pd.read_csv(files[0])


city_result = load_result("city_counts")
hour_result = load_result("hour_counts")
severity_result = load_result("severity_counts")
hotspot_result = load_result("hotspots")


# ---------------------------------------------------------
# LOAD SOURCE DATA FOR INTERACTIVE FILTERING
# ---------------------------------------------------------

DATA_PATH = (
    "hdfs://localhost:9000/"
    "user/hive/warehouse/crashmap.db/accidents/"
    "indian_roads_dataset.csv"
)

# Read through Spark-generated output is not necessary here.
# The dashboard uses the local cleaned dataset if available.

LOCAL_DATA = ROOT / "data" / "processed" / "accidents_clean.csv"

if LOCAL_DATA.exists():

    df = pd.read_csv(LOCAL_DATA)

else:

    st.warning(
        "Interactive filtering requires data/processed/accidents_clean.csv. "
        "Using PySpark summary outputs instead."
    )

    df = None


# ---------------------------------------------------------
# INTERACTIVE FILTERS
# ---------------------------------------------------------

st.header("🔎 Explore Accident Patterns")

if df is not None:

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:

        cities = ["All Cities"] + sorted(
            df["city"].dropna().unique().tolist()
        )

        selected_city = st.selectbox(
            "City",
            cities
        )

    with filter_col2:

        days = ["All Days"] + sorted(
            df["day_of_week"].dropna().unique().tolist()
        )

        selected_day = st.selectbox(
            "Day of Week",
            days
        )

    with filter_col3:

        weather_options = ["All Weather"] + sorted(
            df["weather"].dropna().unique().tolist()
        )

        selected_weather = st.selectbox(
            "Weather",
            weather_options
        )

    with filter_col4:

        severity_options = ["All Severities"] + sorted(
            df["accident_severity"].dropna().unique().tolist()
        )

        selected_severity = st.selectbox(
            "Severity",
            severity_options
        )


    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered_df = df.copy()

    if selected_city != "All Cities":
        filtered_df = filtered_df[
            filtered_df["city"] == selected_city
        ]

    if selected_day != "All Days":
        filtered_df = filtered_df[
            filtered_df["day_of_week"] == selected_day
        ]

    if selected_weather != "All Weather":
        filtered_df = filtered_df[
            filtered_df["weather"] == selected_weather
        ]

    if selected_severity != "All Severities":
        filtered_df = filtered_df[
            filtered_df["accident_severity"] == selected_severity
        ]


else:

    filtered_df = None


# ---------------------------------------------------------
# DYNAMIC SUMMARY
# ---------------------------------------------------------

st.divider()

st.header("📊 Current Selection Summary")

if filtered_df is not None and not filtered_df.empty:

    total_accidents = len(filtered_df)

    # Peak hour
    peak_hour_counts = (
        filtered_df
        .groupby("hour")
        .size()
        .sort_values(ascending=False)
    )

    peak_hour = int(peak_hour_counts.index[0])

    # Top city
    top_city_counts = (
        filtered_df
        .groupby("city")
        .size()
        .sort_values(ascending=False)
    )

    top_city = top_city_counts.index[0]

    # Severity
    top_severity_counts = (
        filtered_df
        .groupby("accident_severity")
        .size()
        .sort_values(ascending=False)
    )

    top_severity = top_severity_counts.index[0]

    # Spatial hotspot
    filtered_df["grid_lat"] = (
        (filtered_df["latitude"] * 10).apply(lambda x: int(x)) / 10
    )

    filtered_df["grid_lon"] = (
        (filtered_df["longitude"] * 10).apply(lambda x: int(x)) / 10
    )

    hotspot_counts = (
        filtered_df
        .groupby(["grid_lat", "grid_lon"])
        .size()
        .reset_index(name="accident_count")
        .sort_values("accident_count", ascending=False)
    )

    if not hotspot_counts.empty:

        top_hotspot = hotspot_counts.iloc[0]

        hotspot_text = (
            f"{top_hotspot['grid_lat']:.1f}, "
            f"{top_hotspot['grid_lon']:.1f}"
        )

    else:

        hotspot_text = "N/A"


    # -----------------------------------------------------
    # SUMMARY CARDS
    # -----------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Accidents",
        f"{total_accidents:,}"
    )

    c2.metric(
        "Top City",
        top_city
    )

    c3.metric(
        "Peak Hour",
        f"{peak_hour:02d}:00"
    )

    c4.metric(
        "Top Severity",
        top_severity.title()
    )

    c5.metric(
        "Top Hotspot",
        hotspot_text
    )

else:

    st.warning(
        "No accident records match the selected filters."
    )

    st.stop()


# ---------------------------------------------------------
# FILTER DESCRIPTION
# ---------------------------------------------------------

filter_description = []

if selected_city != "All Cities":
    filter_description.append(selected_city)

if selected_day != "All Days":
    filter_description.append(selected_day)

if selected_weather != "All Weather":
    filter_description.append(selected_weather)

if selected_severity != "All Severities":
    filter_description.append(selected_severity)

if filter_description:

    st.info(
        "Showing accident patterns for: "
        + " • ".join(filter_description)
    )

else:

    st.info(
        "Showing accident patterns for the complete dataset."
    )


# ---------------------------------------------------------
# CITY ANALYSIS
# ---------------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    city_counts = (
        filtered_df
        .groupby("city")
        .size()
        .reset_index(name="accident_count")
        .sort_values("accident_count")
    )

    fig = px.bar(
        city_counts,
        x="accident_count",
        y="city",
        orientation="h",
        title="Accidents by City"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# HOURLY ANALYSIS
# ---------------------------------------------------------

with col2:

    hour_counts = (
        filtered_df
        .groupby("hour")
        .size()
        .reset_index(name="accident_count")
        .sort_values("hour")
    )

    fig = px.line(
        hour_counts,
        x="hour",
        y="accident_count",
        markers=True,
        title="Accidents by Hour"
    )

    fig.update_xaxes(
        dtick=1
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# SEVERITY ANALYSIS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    severity_counts = (
        filtered_df
        .groupby("accident_severity")
        .size()
        .reset_index(name="accident_count")
    )

    fig = px.pie(
        severity_counts,
        names="accident_severity",
        values="accident_count",
        title="Accident Severity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# DAY ANALYSIS
# ---------------------------------------------------------

with col2:

    day_counts = (
        filtered_df
        .groupby("day_of_week")
        .size()
        .reset_index(name="accident_count")
    )

    fig = px.bar(
        day_counts,
        x="day_of_week",
        y="accident_count",
        title="Accidents by Day"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# SPATIAL HOTSPOTS
# ---------------------------------------------------------

st.divider()

st.subheader("🔥 Spatial Hotspots")

hotspots = (
    filtered_df
    .groupby(["grid_lat", "grid_lon"])
    .size()
    .reset_index(name="accident_count")
    .sort_values(
        "accident_count",
        ascending=False
    )
)

st.dataframe(
    hotspots.head(10),
    hide_index=True,
    use_container_width=True
)


# ---------------------------------------------------------
# MAP
# ---------------------------------------------------------

st.subheader("🗺️ Accident Hotspot Map")

m = folium.Map(
    location=[22.5, 79.0],
    zoom_start=5
)

for _, row in hotspots.head(20).iterrows():

    folium.CircleMarker(
        location=[
            row["grid_lat"] + 0.05,
            row["grid_lon"] + 0.05
        ],

        radius=max(
            5,
            min(
                22,
                row["accident_count"] / 10
            )
        ),

        popup=(
            f"Grid: "
            f"{row['grid_lat']:.1f}, "
            f"{row['grid_lon']:.1f}"
            f"<br>"
            f"Accidents: "
            f"{int(row['accident_count'])}"
        ),

        fill=True
    ).add_to(m)


components.html(
    m.get_root().render(),
    height=600
)


# ---------------------------------------------------------
# PROJECT DISCLAIMER
# ---------------------------------------------------------

st.info(
    "These hotspots represent patterns within the supplied dataset "
    "and are not official real-world accident statistics."
)
