import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

st.title("🏭 Smart Factory IoT Dashboard")
st.markdown("Real-time monitoring of factory sensor data")

DATA_FILE = "data/factory_data.csv"

def load_data():
    return pd.read_csv(DATA_FILE)

def show_alerts(data):
    latest = data.iloc[-1]
    if latest["temperature"] > 80:
        st.error(f"🔥 High Temp Alert: {latest['temperature']} °C")
    if latest["vibration"] > 1.2:
        st.warning(f"⚠️ High Vibration Alert: {latest['vibration']} mm/s")
    if latest["machine_status"] == "Error":
        st.error("❌ Machine Error Detected!")

def plot_graph(data):
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(data["timestamp"], data["temperature"], color='red')
    ax[0].set_title("Temperature Over Time")
    ax[0].tick_params(axis='x', rotation=45)
    ax[1].plot(data["timestamp"], data["vibration"], color='blue')
    ax[1].set_title("Vibration Over Time")
    ax[1].tick_params(axis='x', rotation=45)
    st.pyplot(fig)

while True:
    df = load_data()
    show_alerts(df)
    plot_graph(df)
    st.dataframe(df.tail(5))
    time.sleep(5)