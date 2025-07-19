import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import time
from datetime import datetime

st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")
st.title("🏭 Smart Factory IoT Dashboard")
st.markdown("Real-time monitoring of factory sensor data with alerts and reporting")

DATA_FILE = "data/factory_data.csv"

# Use a built-in Matplotlib style
plt.style.use('ggplot')


def load_data():
    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")


def show_alerts(data):
    latest = data.iloc[-1]
    st.markdown("### 🔔 System Alerts")
    if latest["temperature"] > 80:
        st.error(f"🔥 High Temp: {latest['temperature']} °C")
    if latest["vibration"] > 1.2:
        st.warning(f"⚠️ Vibration High: {latest['vibration']} mm/s")
    if latest["machine_status"] == "Error":
        st.error("❌ Machine Error")
    if (
        latest["temperature"] <= 80
        and latest["vibration"] <= 1.2
        and latest["machine_status"] != "Error"
    ):
        st.success("✅ System running normally")


def plot_graph(data):
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))

    ax[0].plot(data["timestamp"], data["temperature"], color='crimson')
    ax[0].set_title("Temperature Over Time")
    ax[0].set_ylabel("°C")
    ax[0].tick_params(axis='x', rotation=45)

    ax[1].plot(data["timestamp"], data["vibration"], color='navy')
    ax[1].set_title("Vibration Over Time")
    ax[1].set_ylabel("mm/s")
    ax[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)


def download_excel(data, key_suffix):
    output = io.BytesIO()
    data.to_excel(output, index=False)
    st.download_button(
        label="📥 Download Report as Excel",
        data=output.getvalue(),
        file_name="factory_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_excel_{key_suffix}"
    )


# Session state to track refresh control
if "refresh_ready" not in st.session_state:
    st.session_state.refresh_ready = False
if "last_refresh_rate" not in st.session_state:
    st.session_state.last_refresh_rate = 5

# Sidebar interval
refresh_rate = st.sidebar.selectbox("⏱️ Auto-refresh interval", [3, 5, 10], index=1)

# Handle refresh change
if refresh_rate != st.session_state.last_refresh_rate:
    st.session_state.last_refresh_rate = refresh_rate
    st.session_state.refresh_ready = False
    st.stop()  # stop instead of rerun to avoid crash

# Mark as ready
st.session_state.refresh_ready = True

# Live dashboard
placeholder = st.empty()

while True:
    df = load_data()
    key_suffix = datetime.now().strftime("%Y%m%d%H%M%S")

    with placeholder.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            show_alerts(df)
            download_excel(df, key_suffix)

        with col2:
            plot_graph(df)

        st.markdown("### 📋 Recent Sensor Logs")
        st.dataframe(df.tail(10), use_container_width=True)

    time.sleep(refresh_rate)
    st.rerun()

