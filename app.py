import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(page_title="MECM Client Health Dashboard", layout="wide")
st.title("🖥️ MECM Client Health Dashboard")
st.markdown("**Visualize and analyze client health across your environment**")

# Sidebar
st.sidebar.header("Upload Data")
uploaded_files = st.sidebar.file_uploader(
    "Upload JSON health reports (multiple allowed)", 
    type=["json"], 
    accept_multiple_files=True
)

data_folder = st.sidebar.text_input("Or load from folder", "reports")

# Load data
all_data = []

if uploaded_files:
    for file in uploaded_files:
        try:
            data = json.load(file)
            all_data.append(data)
        except:
            st.warning(f"Could not read {file.name}")

elif Path(data_folder).exists():
    for json_file in Path(data_folder).glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                all_data.append(data)
        except:
            pass

if not all_data:
    st.info("Upload JSON reports or place them in the 'reports' folder to begin.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame([{
    "Hostname": d["system"]["hostname"],
    "OS": d["system"]["os"],
    "Timestamp": d["system"]["timestamp"],
    "Disk_Free_GB": d["disk"].get("free_gb"),
    "Disk_Status": d["disk"].get("status"),
    "Memory_Used_%": d["memory"].get("percent_used"),
    "CPU_Used_%": d["cpu"].get("percent_used"),
    "MECM_Status": "Installed" if d.get("mecm", {}).get("installed") else "Not Found"
} for d in all_data])

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Clients", len(df))
col2.metric("Healthy Clients", len(df[df["Memory_Used_%"] < 85]))
col3.metric("MECM Clients", len(df[df["MECM_Status"] == "Installed"]))

st.subheader("Client Overview")
st.dataframe(df, use_container_width=True)

# Charts
st.subheader("Health Charts")
c1, c2 = st.columns(2)

with c1:
    fig = px.bar(df, x="Hostname", y="Memory_Used_%", color="Memory_Used_%",
                 color_continuous_scale="RdYlGn_r", title="Memory Usage %")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df, x="Hostname", y="Disk_Free_GB", title="Free Disk Space (GB)")
    st.plotly_chart(fig, use_container_width=True)

# Failing Clients
st.subheader("🔴 Clients Needing Attention")
failing = df[(df["Memory_Used_%"] > 85) | (df["Disk_Free_GB"] < 20)]
if not failing.empty:
    st.dataframe(failing, use_container_width=True)
else:
    st.success("All clients look healthy!")

# Export buttons
st.subheader("Export")
col_a, col_b = st.columns(2)
if col_a.button("Export to CSV"):
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "client_health.csv", "text/csv")

if col_b.button("Export Summary Report"):
    st.info("PDF export coming in next update...")

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
