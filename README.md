# ResilioChain 🔗
### End-to-End Supply Chain Intelligence Platform

> *"I built this to optimize Service Levels while minimizing Holding Costs."*

---

## 📌 Problem Statement
Modern businesses lose billions due to **Stock-outs** (shelves going empty) and **Dead Stock** (capital frozen in unsold inventory). ResilioChain solves both by building a Digital Twin of a warehouse — predicting future demand and automating ordering decisions.

---

## 🏗️ Project Structure
'''
ResilioChain/
├── src/
│   ├── data_generator.py   # Phase 1 — Synthetic 365-day warehouse simulation
│   ├── eda.py              # Phase 2 — EDA, ABC Analysis, Lag Features
│   ├── forecast.py         # Phase 3 — XGBoost demand forecasting
│   ├── optimizer.py        # Phase 4 — ROP / Safety Stock engine
│   └── app.py              # Phase 5 — Streamlit dashboard
├── data/                   # Generated CSVs
├── outputs/                # Charts and analysis
├── notebooks/              # Jupyter exploration
├── requirements.txt
└── README.md

'''
---

## 🚀 Project Phases

| Phase | Focus | Status |
|-------|-------|--------|
| 1 — Data Engine | Synthetic 365-day simulation | 🔄 In Progress |
| 2 — EDA | ABC Analysis, Burn Rate, Lag Features | ⏳ Upcoming |
| 3 — Forecasting | XGBoost demand prediction (30-day) | ⏳ Upcoming |
| 4 — Optimization | ROP, Safety Stock, EOQ | ⏳ Upcoming |
| 5 — Deployment | Streamlit + What-If Dashboard | ⏳ Upcoming |

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Data Engineering | Python, Pandas, NumPy, Faker |
| Visualization | Matplotlib, Seaborn, Plotly |
| AI / Forecasting | XGBoost, Scikit-learn |
| Optimization | SciPy |
| Deployment | Streamlit |
| DevOps | Git, GitHub |

---

## ▶️ Quick Start

```bash
git clone https://github.com/dominator959/ResilioChain.git
cd ResilioChain
conda create -n resiliochain python=3.11 -y
conda activate resiliochain
pip install -r requirements.txt
python src/data_generator.py
```

---

## 💼 Business Value
1. **Capital Efficiency** — Frees frozen cash from over-stocked warehouses
2. **Customer Loyalty** — Eliminates stock-outs so shelves are always full
3. **Operational Clarity** — CEO dashboard shows the future, not just the past

---

## 👥 Team

| Name | GitHub |
|------|--------|
| Muhammad Usman | [@dominator959](https://github.com/dominator959) |
| Faizan Toheed | [@faizantoheed456](https://github.com/faizantoheed456) |

---
*Supply Chain Data Science Portfolio Project*