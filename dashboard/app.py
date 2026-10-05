from pathlib import Path
import glob
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"

st.set_page_config(
    page_title="CrashMap",
    page_icon="🚧",
    layout="wide"
)

st.title("🚧 CrashMap")
st.caption(
    "Road Accident Analysis and Hotspot Detection using Hadoop, Hive and PySpark"
)


def load_result(folder):
    files = glob.glob(str(OUTPUT / folder / "part-*.csv"))

    if not files:
        st.error(
            f"No PySpark output found for {folder}. "
            "Run scripts/pyspark_analysis.py first."
        )
        st.stop()

    return pd.read_csv(files[0])


city = load_result("city_counts")
hour = load_result("hour_counts")
severity = load_result("severity_counts")
hotspots = load_result("hotspots")

city["accident_count"] = pd.to_numeric(city["accident_count"])
hour["hour"] = pd.to_numeric(hour["hour"])
hour["accident_count"] = pd.to_numeric(hour["accident_count"])
severity["accident_count"] = pd.to_numeric(severity["accident_count"])

for column in ["grid_lat", "grid_lon", "accident_count"]:
    hotspots[column] = pd.to_numeric(hotspots[column])

total = int(city["accident_count"].sum())

top_city = city.iloc[0]
top_hour = hour.loc[hour["accident_count"].idxmax()]
top_hotspot = hotspots.iloc[0]


# -----------------------------
# SUMMARY METRICS
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Accidents",
    f"{total:,}"
)

c2.metric(
    "Highest Accident City",
    str(top_city["city"])
)

c3.metric(
    "Peak Observed Hour",
    f"{int(top_hour['hour']):02d}:00"
)

c4.metric(
    "Top Hotspot",
    f"{top_hotspot['grid_lat']:.1f}, "
    f"{top_hotspot['grid_lon']:.1f}"
)


st.divider()


# -----------------------------
# CITY + HOURLY ANALYSIS
# -----------------------------

left, right = st.columns(2)

with left:

    fig_city = px.bar(
        city.sort_values("accident_count"),
        x="accident_count",
        y="city",
        orientation="h",
        text="accident_count",
        title="Accidents by City"
    )

    fig_city.update_layout(
        xaxis_title="Accident Count",
        yaxis_title="City"
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )


with right:

    fig_hour = px.line(
        hour.sort_values("hour"),
        x="hour",
        y="accident_count",
        markers=True,
        title="Accidents by Hour"
    )

    fig_hour.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Accident Count",
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )


# -----------------------------
# SEVERITY + HOTSPOT TABLE
# -----------------------------

left, right = st.columns(2)

with left:

    fig_severity = px.pie(
        severity,
        names="accident_severity",
        values="accident_count",
        title="Accident Severity Distribution",
        hole=0.35
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )


with right:

    st.subheader("Top Spatial Hotspots")

    display_hotspots = hotspots.head(10).rename(
        columns={
            "grid_lat": "Grid Latitude",
            "grid_lon": "Grid Longitude",
            "accident_count": "Accidents"
        }
    )

    st.dataframe(
        display_hotspots,
        hide_index=True,
        use_container_width=True
    )


# -----------------------------
# FOLIUM HOTSPOT MAP
# -----------------------------

st.divider()

st.subheader("🗺️ Accident Hotspot Map")

st.caption(
    "Each marker represents a 0.1° latitude/longitude grid cell. "
    "Larger circles indicate more accidents in the dataset."
)

m = folium.Map(
    location=[22.5, 79.0],
    zoom_start=5,
    tiles="OpenStreetMap"
)

for _, row in hotspots.head(20).iterrows():

    folium.CircleMarker(
        location=[
            row["grid_lat"] + 0.05,
            row["grid_lon"] + 0.05
        ],

        radius=max(
            5,
            min(22, row["accident_count"] / 35)
        ),

        popup=(
            f"Grid: {row['grid_lat']:.1f}, "
            f"{row['grid_lon']:.1f}<br>"
            f"Accidents: {int(row['accident_count'])}"
        ),

        tooltip=(
            f"{int(row['accident_count'])} accidents"
        ),

        fill=True
    ).add_to(m)


components.html(
    m.get_root().render(),
    height=600
)


st.info(
    "Note: These are patterns and hotspots within the supplied dataset; "
    "they should not be interpreted as official real-world accident statistics."
)
