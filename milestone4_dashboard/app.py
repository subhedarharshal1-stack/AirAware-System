import streamlit as st
import pandas as pd
import joblib
import sys
import os
from datetime import datetime, timedelta

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from milestone3_aqi_analysis.aqi_category import get_aqi_category
from milestone3_aqi_analysis.alert_system import generate_alert

st.set_page_config(layout="wide")

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    return pd.read_csv("data/air_quality.csv")

df = load_data()

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model():
    return joblib.load("milestone2_forecasting_model/aqi_model.pkl")

model = load_model()

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("AirWare Dashboard")

cities = df["City"].dropna().unique()
selected_city = st.sidebar.selectbox("Select City", cities, key="city_selector")

# Button
run_button = st.sidebar.button("Get AQI")

# Developer credit in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Developer:** Harshal Subhedar")   # <-- Your name added

# ---------------- MAIN UI ---------------- #

st.title("AirWare - AQI Prediction Dashboard")
st.subheader("Real-time Air Quality Monitoring & Forecasting")

st.divider()

if run_button:
    city_df = df[df["City"] == selected_city].copy()
    if city_df.empty:
        st.warning(f"No data available for {selected_city}")
        st.stop()

    # Ensure Date column is datetime
    city_df["Date"] = pd.to_datetime(city_df["Date"])

    # ---------------- TODAY'S OVERVIEW ---------------- #
    st.header("Today's Air Quality Overview")

    # Get latest actual AQI as current (or use model prediction if preferred)
    latest_aqi = city_df["AQI"].iloc[-1]
    latest_category = get_aqi_category(latest_aqi)

    # Change from yesterday
    if len(city_df) > 1:
        previous_aqi = city_df["AQI"].iloc[-2]
        change = latest_aqi - previous_aqi
    else:
        change = 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current AQI", f"{latest_aqi:.1f}")
    with col2:
        st.metric("Category", latest_category)
    with col3:
        st.metric("Change from yesterday", f"{change:+.1f}")

    st.divider()

    # ---------------- CURRENT AQI STATUS ---------------- #
    st.subheader("Current AQI Status")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("AQI", latest_category)
    with col_b:
        st.metric("Alert", latest_category)

    st.divider()

    # ---------------- AIR QUALITY ALERT ---------------- #
    st.subheader("Air Quality Alert")
    alert_message = generate_alert(latest_aqi)
    st.warning(alert_message)

    # Recommendation based on AQI
    if latest_aqi <= 50:
        recommendation = "You can safely perform outdoor activities."
    elif latest_aqi <= 100:
        recommendation = "Sensitive individuals should limit prolonged outdoor exertion."
    else:
        recommendation = "Avoid outdoor activities."
    st.info(f"**Recommendation:** {recommendation}")

    st.divider()

    # ---------------- 7-DAY AQI FORECAST ---------------- #
    st.subheader("7-Day AQI Forecast")

    # Define pollutant columns expected in the image
    pollutant_cols = ["PM2.5", "PM10", "O3", "CO", "NOx", "SO2", "HCHO", "PM1"]
    # Check which ones exist in the dataframe
    existing_pollutants = [col for col in pollutant_cols if col in city_df.columns]

    if not existing_pollutants:
        st.warning("Pollutant data not found in the dataset. Cannot display forecast table.")
    else:
        # Use the last available row for forecast values
        last_row = city_df.iloc[-1]
        # Generate dates for the next 7 days
        last_date = city_df["Date"].iloc[-1]
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, 8)]

        # Build forecast dataframe
        forecast_data = []
        for d in forecast_dates:
            row = {"Date": d.date(), "Time": "7:00 AM"}
            for pol in existing_pollutants:
                row[pol] = last_row[pol]
            forecast_data.append(row)

        forecast_df = pd.DataFrame(forecast_data)

        # Format numeric columns to one decimal for display
        for pol in existing_pollutants:
            forecast_df[pol] = forecast_df[pol].map("{:.1f}".format)

        st.dataframe(forecast_df.set_index("Date"), use_container_width=True)

    st.divider()

    # Optional: display a small note with the current date
    st.caption(f"Dashboard generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")

else:
    st.info("👈 Select a city and click **Get AQI** to view the dashboard")