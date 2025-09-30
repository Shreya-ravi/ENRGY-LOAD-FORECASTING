import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# -------------------------
# Load or simulate data
# -------------------------
@st.cache_data
def load_data():
    # Simulated power consumption data
    dates = pd.date_range(datetime.now() - timedelta(days=30), periods=720, freq="H")
    consumption = np.random.uniform(1.0, 5.0, size=len(dates))  # kWh
    return pd.DataFrame({"datetime": dates, "consumption_kWh": consumption})

data = load_data()

# -------------------------
# Streamlit App
# -------------------------
st.set_page_config(page_title="Power Consumption Tracker", layout="wide")

st.title("⚡ Power Consumption Live Tracker")
st.markdown("Track your power usage, generate reports, and analyze trends.")

# Sidebar options
st.sidebar.header("Options")
report_type = st.sidebar.selectbox("Select Report", ["Overview", "Daily Report", "Monthly Summary"])

# -------------------------
# Live Tracking Visualization
# -------------------------
st.subheader("📈 Live Tracking")
latest_data = data.tail(50)

fig, ax = plt.subplots()
ax.plot(latest_data["datetime"], latest_data["consumption_kWh"], marker="o")
ax.set_xlabel("Time")
ax.set_ylabel("Consumption (kWh)")
ax.set_title("Recent Power Consumption")
st.pyplot(fig)

# -------------------------
# Reports
# -------------------------
st.subheader("📊 Reports")

if report_type == "Overview":
    st.write("### General Statistics")
    st.metric("Total Consumption (30 days)", f"{data['consumption_kWh'].sum():.2f} kWh")
    st.metric("Average Daily Usage", f"{data['consumption_kWh'].mean():.2f} kWh")
    st.metric("Peak Usage", f"{data['consumption_kWh'].max():.2f} kWh")

elif report_type == "Daily Report":
    daily = data.groupby(data["datetime"].dt.date)["consumption_kWh"].sum()
    st.write("### Daily Power Usage")
    st.line_chart(daily)

elif report_type == "Monthly Summary":
    monthly = data.groupby(data["datetime"].dt.to_period("M"))["consumption_kWh"].sum()
    st.write("### Monthly Summary")
    st.bar_chart(monthly)

# -------------------------
# User Input for Custom Report
# -------------------------
st.subheader("📝 Custom Report")
start_date = st.date_input("Start Date", data["datetime"].min().date())
end_date = st.date_input("End Date", data["datetime"].max().date())

if st.button("Generate Report"):
    mask = (data["datetime"].dt.date >= start_date) & (data["datetime"].dt.date <= end_date)
    report_data = data.loc[mask]

    if not report_data.empty:
        st.success(f"Report from {start_date} to {end_date}")
        st.write(f"**Total Consumption:** {report_data['consumption_kWh'].sum():.2f} kWh")
        st.write(f"**Average Consumption:** {report_data['consumption_kWh'].mean():.2f} kWh")
        st.line_chart(report_data.set_index("datetime")["consumption_kWh"])
    else:
        st.warning("No data available for this period.")

# -------------------------
# Export Option
# -------------------------
st.sidebar.subheader("Download Data")
st.sidebar.download_button(
    label="Download CSV",
    data=data.to_csv(index=False),
    file_name="power_consumption.csv",
    mime="text/csv"
)
