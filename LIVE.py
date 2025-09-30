import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# -------------------------
# Generate dummy energy data
# -------------------------
@st.cache_data
def generate_data(hours=500):
    np.random.seed(42)
    timestamps = pd.date_range(datetime.now() - timedelta(hours=hours), periods=hours, freq='H')
    # Simulate energy load with sine + noise
    load = np.sin(np.linspace(0, 50, hours)) + np.random.normal(0, 0.1, hours) + 2
    return pd.DataFrame({"timestamp": timestamps, "load": load})

data = generate_data()

# -------------------------
# Streamlit App
# -------------------------
st.set_page_config(page_title="Power Consumption Tracker", layout="wide")
st.title("⚡ Power Consumption Live Tracker")
st.markdown("Track your energy usage over time and see reports.")

# Sidebar options
st.sidebar.header("Options")
report_type = st.sidebar.selectbox("Select Report", ["Overview", "Recent Trend"])

# -------------------------
# Live Tracking Visualization
# -------------------------
st.subheader("📈 Recent Load (Live Simulation)")
latest_data = data.tail(50)

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(latest_data["timestamp"], latest_data["load"], marker='o', linestyle='-')
ax.set_xlabel("Time")
ax.set_ylabel("Load")
ax.set_title("Recent Energy Load")
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------
# Reports
# -------------------------
st.subheader("📊 Reports")
if report_type == "Overview":
    st.write("### General Statistics")
    st.metric("Total Load", f"{data['load'].sum():.2f}")
    st.metric("Average Load", f"{data['load'].mean():.2f}")
    st.metric("Peak Load", f"{data['load'].max():.2f}")
else:
    st.write("### Recent Trend (Last 50 hours)")
    st.line_chart(latest_data.set_index("timestamp")["load"])

# -------------------------
# Forecast Simulation
# -------------------------
st.subheader("🔮 Forecast (Next 24 Hours)")

# Simple forecast: continue last trend with some noise
last_values = data["load"].values[-24:]
future_times = pd.date_range(data["timestamp"].iloc[-1] + pd.Timedelta(hours=1), periods=24, freq='H')
future_load = last_values[-1] + np.cumsum(np.random.normal(0, 0.05, 24))  # small variation

forecast_df = pd.DataFrame({"timestamp": future_times, "predicted_load": future_load})

st.line_chart(forecast_df.set_index("timestamp")["predicted_load"])
st.write("### Forecast Table")
st.dataframe(forecast_df)
