import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="UK Crime Dashboard", page_icon="🚔", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #ff4b4b; }
    h2, h3 { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

st.title("🚔 UK Crime Dashboard")
st.markdown("### Real-time UK Crime Data Explorer")

CITIES = {
    "London": (51.5074, -0.1278),
    "Manchester": (53.4808, -2.2426),
    "Birmingham": (52.4862, -1.8904),
    "Leeds": (53.7997, -1.5492),
    "Bristol": (51.4545, -2.5879),
    "Liverpool": (53.4084, -2.9916),
    "Sheffield": (53.3811, -1.4701),
    "Nottingham": (52.9548, -1.1581),
}

col1, col2 = st.columns(2)
with col1:
    city = st.selectbox("📍 Select City", list(CITIES.keys()))
with col2:
    crime_type = st.selectbox("🔍 Select Crime Type", [
        "all-crime", "burglary", "robbery", "vehicle-crime",
        "violent-crime", "shoplifting", "drugs"
    ])

lat, lng = CITIES[city]

@st.cache_data
def get_crime_data(lat, lng, crime):
    url = f"https://data.police.uk/api/crimes-street/{crime}?lat={lat}&lng={lng}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else []

with st.spinner("Loading crime data..."):
    data = get_crime_data(lat, lng, crime_type)

if data:
    df = pd.DataFrame([{
        "category": d["category"],
        "lat": float(d["location"]["latitude"]),
        "lon": float(d["location"]["longitude"]),
        "street": d["location"]["street"]["name"],
        "outcome": d.get("outcome_status", {}).get("category", "Unknown") if d.get("outcome_status") else "Unknown"
    } for d in data])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Crimes", len(df))
    col2.metric("Crime Type", crime_type.replace("-", " ").title())
    col3.metric("City", city)

    st.subheader("🗺️ Crime Map")
    fig_map = px.scatter_mapbox(
        df, lat="lat", lon="lon",
        color="category", hover_name="street",
        hover_data=["outcome"],
        zoom=11, height=500,
        mapbox_style="carto-darkmatter"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Crimes by Type")
        fig_bar = px.bar(
            df["category"].value_counts().reset_index(),
            x="category", y="count",
            color="count", color_continuous_scale="reds"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("🥧 Outcome Distribution")
        fig_pie = px.pie(
            df, names="outcome",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.error("No data found. Try a different city or crime type!")