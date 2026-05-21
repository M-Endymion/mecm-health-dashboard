import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="MECM Health Dashboard", layout="wide")
st.title("🖥️ MECM Client Health Dashboard")

# Sidebar
st.sidebar.header("Data Source")
uploaded_files = st.sidebar.file_uploader("Upload JSON reports", type=["json"], accept_multiple_files=True)

if st.sidebar.button("Load Sample Data"):
    st.success("Sample data loaded! (Make sure you ran generate_sample_data.py)")

# Load data
all_data = []
reports_folder = Path("reports")

if uploaded_files:
    for file in uploaded_files:
        all_data.append(json.load(file))
elif reports_folder.exists():
    for f in reports_folder.glob("*.json"):
        try:
            with open(f) as file:
                all_data.append(json.load(file))
        except:
            pass

if not all_data:
    st.info("👆 Upload JSON files or click 'Load Sample Data'")
    st.stop()

# Create DataFrame
df = pd.DataFrame([{
    "Hostname": d["system"]["hostname"],
    "OS": d["system"]["os"],
    "Disk_Free_GB": round(d["disk"].get("free_gb", 0), 1),
    "Memory_%": d["memory"].get("percent_used", 0),
    "CPU_%": d["cpu"].get("percent_used", 0),
    "MECM": "✅ Installed" if d.get("mecm", {}).get("installed") else "❌ Not Found"
} for d in all_data])

# Dashboard
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clients", len(df))
col2.metric("High Memory", len(df[df["Memory_%"] > 85]))
col3.metric("Low Disk", len(df[df["Disk_Free_GB"] < 25]))
col4.metric("MECM Installed", len(df[df["MECM"].str.contains("Installed")]))

st.dataframe(df, use_container_width=True)

# Charts
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x="Hostname", y="Memory_%", color="Memory_%", 
                 color_continuous_scale="RdYlGn_r", title="Memory Usage %")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df, x="Hostname", y="Disk_Free_GB", title="Free Disk Space (GB)")
    st.plotly_chart(fig, use_container_width=True)

# === FIXED PDF EXPORT ===
if st.button("📄 Export Full Report as PDF"):
    with st.spinner("Generating PDF..."):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("MECM Client Health Report", styles['Title']))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        
        # Table data
        table_data = [df.columns.tolist()] + df.values.tolist()
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(t)
        
        doc.build(elements)
        buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download PDF Report",
            data=buffer,
            file_name=f"MECM_Health_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )
        st.success("PDF Ready!")

st.caption("Built by Jason Ray • Companion to cross-platform-client-health tool")
