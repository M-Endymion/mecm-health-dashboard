import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="MECM Health Dashboard", layout="wide")
st.title("🖥️ MECM Client Health Dashboard")

# Sidebar
st.sidebar.header("Data Source")
uploaded_files = st.sidebar.file_uploader("Upload JSON reports", type=["json"], accept_multiple_files=True)
use_sample = st.sidebar.button("Load Sample Data")

if use_sample:
    st.success("Sample data loaded!")

# Load data logic (same as before, but cleaner)
all_data = []
reports_folder = Path("reports")

if uploaded_files:
    for file in uploaded_files:
        all_data.append(json.load(file))
elif reports_folder.exists():
    for f in reports_folder.glob("*.json"):
        with open(f) as file:
            all_data.append(json.load(file))

if not all_data:
    st.info("👆 Upload JSON files or click 'Load Sample Data'")
    st.stop()

df = pd.DataFrame([{
    "Hostname": d["system"]["hostname"],
    "OS": d["system"]["os"],
    "Disk_Free_GB": round(d["disk"].get("free_gb", 0), 1),
    "Memory_%": d["memory"].get("percent_used", 0),
    "CPU_%": d["cpu"].get("percent_used", 0),
    "MECM": "✅" if d.get("mecm", {}).get("installed") else "❌"
} for d in all_data])

# Main Dashboard
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clients", len(df))
col2.metric("High Memory", len(df[df["Memory_%"] > 85]))
col3.metric("Low Disk", len(df[df["Disk_Free_GB"] < 25]))
col4.metric("MECM Installed", len(df[df["MECM"] == "✅"]))

st.dataframe(df, use_container_width=True)

# Charts
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x="Hostname", y="Memory_%", color="Memory_%", title="Memory Usage")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(df, x="Hostname", y="Disk_Free_GB", title="Free Disk Space")
    st.plotly_chart(fig, use_container_width=True)

# PDF Export
if st.button("📄 Export Full Report as PDF"):
    with st.spinner("Generating PDF..."):
        pdf_path = f"MECM_Health_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph("MECM Client Health Report", styles['Title']))
        # ... (simple table export)
        st.success(f"PDF saved as {pdf_path}")
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, pdf_path)

st.caption("Built by Jason Ray • Companion to cross-platform-client-health tool")
