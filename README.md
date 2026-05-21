<div align="center">
  <img src="https://raw.githubusercontent.com/M-Endymion/mecm-health-dashboard/main/thumbnail-mecm-health.png" alt="MECM Health Dashboard" width="100%" />
</div>

<br>

# MECM Client Health Dashboard

A beautiful **Streamlit** web dashboard for visualizing MECM/SCCM client health.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## Features

- Interactive charts (Memory, Disk, CPU)
- Failing client highlighting
- CSV + PDF export
- Works with reports from `cross-platform-client-health`

---

## Quick Start

```bash
git clone https://github.com/M-Endymion/mecm-health-dashboard.git
cd mecm-health-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## How to Use

1. Run the dashboard locally (```streamlit run app.py```)
2. Generate reports using my cross-platform-client-health tool
3. Upload the JSON files or place them in the ```reports/``` folder
4. View charts and compliance status

---

## Using Sample Data

1. Run the sample data generator:
   ```python generate_sample_data.py```
2. Click **"Load Sample Data"** in the sidebar, or just refresh the dashboard — it will automatically load files from the ```reports/``` folder.

---

### Deployment

- **Streamlit Cloud:** Just connect the repo at share.streamlit.io
- **Docker:** See Dockerfile in the repo
- **Local:** streamlit run app.py

---

## Future Enhancements

- Direct connection to MECM database / WMI
- PDF report export
- Historical trend analysis
- Authentication & multi-user support

---

**Jason Ray** (M-Endymion)

MECM/SCCM Automation & Visualization Tools

- LinkedIn: Jason Ray
- Portfolio: m-endymion.github.io

Last Updated: May 2026
