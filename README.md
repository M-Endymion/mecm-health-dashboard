<div align="center">
  <img src="https://raw.githubusercontent.com/M-Endymion/mecm-health-dashboard/main/thumbnail.png" alt="MECM Health Dashboard" width="100%" />
</div>

<br>

# MECM Client Health Dashboard

A **Streamlit** web dashboard for visualizing MECM/SCCM client health reports.

Built as a companion to my PowerShell and Python client health tools.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

---

## Features

- Upload multiple JSON health reports
- Overview metrics and failing clients
- Interactive charts (Memory, Disk, CPU)
- Data table with filtering
- Export to CSV
- Clean, responsive design

---

## Quick Start

```bash
git clone https://github.com/M-Endymion/mecm-health-dashboard.git
cd mecm-health-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

HH How to Use

1. Run the dashboard locally (```streamlit run app.py```)
2. Generate reports using my cross-platform-client-health tool
3. Upload the JSON files or place them in the ```reports/``` folder
4. View charts and compliance status

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
