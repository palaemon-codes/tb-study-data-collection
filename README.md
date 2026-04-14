# TB Study Data Collection

A Streamlit web application for cross-sectional TB study data collection in Chennai, India. Built to support clinical research on treatment delays and digital health literacy among TB patients.

## Overview

This tool was developed to assist field researchers in digitally capturing and analysing patient data across five structured sections:

1. **Demographics & Clinical Info** — Patient ID, age, gender, TB type, socioeconomic profile
2. **Digital Pathway Mapping** — Critical timeline dates (symptom onset → diagnosis → treatment start) with automated delay calculation
3. **DHLI Assessment** — 10-item Digital Health Literacy Instrument (Tamil + English), auto-scored
4. **Data Visualization** — Per-patient delay breakdown, Gantt chart timelines, and population-level analytics dashboard
5. **Verification & Export** — Summary review and CSV export (current patient + sample dataset)

## Tech Stack

- **Python 3.8+**
- **Streamlit** — UI and session state
- **Pandas** — Data handling and export
- **Plotly** — Interactive charts (Gantt, histogram, scatter, box plots)

## Getting Started

```bash
git clone https://github.com/palaemon-codes/tb-study-data-collection.git
cd tb-study-data-collection
pip install -r requirements.txt
streamlit run tb_study_app.py
```

App runs at `http://localhost:8501`.

## Deploying to Streamlit Community Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Create a new app, point it to `tb_study_app.py`
4. Deploy

## Data & Privacy

All data is stored in Streamlit session state only — nothing is persisted server-side. Exports are triggered manually by the researcher. A 30-patient synthetic dataset is bundled for demonstration and testing.

## License

Developed for research use as part of a cross-sectional TB care study, Chennai, Tamil Nadu.
