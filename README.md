# ResilioChain 🔗
### End-to-End Supply Chain Intelligence Platform

> *"Built to optimize Service Levels while minimizing Holding Costs."*

---

## 📌 Problem Statement

Modern businesses lose billions due to **Stock-outs** (shelves going empty) and **Dead Stock** (capital frozen in unsold inventory). ResilioChain solves both by building a **Digital Twin of a warehouse** — predicting future demand and automating ordering decisions.

---

## 🏗️ Project Structure

```
ResilioChain/
├── src/
│   ├── data_generator.py       # Phase 1 — Synthetic 365-day warehouse simulation
│   ├── eda.py                  # Phase 2 — EDA, ABC Analysis, Lag Features (upcoming)
│   ├── forecast.py             # Phase 3 — XGBoost demand forecasting (upcoming)
│   ├── optimizer.py            # Phase 4 — ROP / Safety Stock engine (upcoming)
│   └── app.py                  # Phase 5 — Streamlit dashboard (upcoming)
├── data/
│   ├── transactions.csv        # 1,825 rows — daily sales per product (cleaned)
│   ├── inventory.csv           # 1,825 rows — daily stock levels per product
│   ├── products.csv            # 5 rows — product reference table
│   └── suppliers.csv           # 3 rows — supplier reference table  # Transactions & Products EDA   # Inventory & Suppliers EDA
├── notebooks/
│   └── eda/
│       ├── session_2_eda_loading_and_inspection_part_A.ipynb        # Transactions & Products — loading, types, nulls, drops
│       ├── session_2_eda_loading_and_inspection_part_B.ipynb        # Inventory & Suppliers — loading, types, nulls, drops
│       ├── session_2_eda_grouping_and_aggregations_part_A.ipynb     # Transactions & Products — groupby, aggregations, trends
│       └── session_2_eda_grouping_and_aggregations_part_B.ipynb     # Inventory & Suppliers — stockout rates, supplier performance
├── outputs/                    # Charts and analysis (generated)
├── requirements.txt
└── README.md
```

---

## 🚀 Project Phases

| Phase | Focus | Status |
|-------|-------|--------|
| 1 — Data Engine | Synthetic 365-day simulation | ✅ Complete |
| 2 — EDA | Data Loading, Inspection & Quality Audit | ✅ Complete (Sessions A & B) |
| 3 — Forecasting | XGBoost demand prediction (30-day) | ⏳ Upcoming |
| 4 — Optimization | ROP, Safety Stock, EOQ | ⏳ Upcoming |
| 5 — Deployment | Streamlit + What-If Dashboard | ⏳ Upcoming |

---

## ✅ What's Been Built (Sessions 1 & 2)

### Session 1 — Data Engine (`src/data_generator.py`)

Generates a fully synthetic but realistic warehouse simulation across **365 days** for **5 products** and **3 suppliers**.

**Product Catalogue:**

| ID | Product | Category | Unit Cost | Unit Price | Base Demand/day |
|----|---------|----------|-----------|------------|-----------------|
| P001 | Wireless Headphones | Electronics | $45.00 | $89.99 | 22 |
| P002 | Yoga Mat | Fitness | $12.00 | $29.99 | 18 |
| P003 | Stainless Water Bottle | Kitchen | $8.00 | $19.99 | 30 |
| P004 | Bluetooth Speaker | Electronics | $30.00 | $59.99 | 15 |
| P005 | Winter Jacket | Apparel | $55.00 | $129.99 | 10 |

**Supplier Table:**

| ID | Supplier | Lead Time | Reliability |
|----|----------|-----------|-------------|
| S001 | AsiaTech Imports | 14 days | 92% |
| S002 | EuroGoods Ltd | 7 days | 97% |
| S003 | LocalFast Supply Co | 3 days | 99% |

**Key simulation features:**
- Poisson-distributed demand (realistic "noisy" sales, not flat)
- Day-of-week seasonality (30% weekend boost)
- Monthly seasonality (Dec spike ×1.60, Jan slump ×0.75, summer rise)
- Running inventory simulation with reorder point (ROP = 150 units), order qty = 400
- Supplier lead time noise — delayed shipments modelled stochastically
- Generates 4 CSV files: `transactions.csv`, `inventory.csv`, `products.csv`, `suppliers.csv`

---

### Session 2 — EDA: Data Loading & Inspection (Parts A & B)

**Part A** — `notebooks/eda/session_2_eda_loading_and_inspection_part_A.ipynb`

Deep inspection of `transactions.csv` and `products.csv`:

- Shape validation: `transactions.csv` → **1,825 rows × 9 columns** (5 products × 365 days)
- Zero null values, zero duplicates — dataset confirmed clean
- Date range confirmed: **2024-01-01 → 2024-12-31**
- Demand statistics: Min 4 | Max 72 | Mean 22.33 | Std Dev 10.82 — significant daily fluctuation
- **Redundant columns dropped:** `product_name`, `category`, `unit_cost`, `unit_price` (static reference data better kept in `products.csv`)
- Mathematical consistency verified: `gross_profit = revenue − cogs` holds for all rows
- Profit margin analysis per product (Yoga Mat leads at ~60%)
- `transactions.csv` re-saved in cleaned, lean format

**Part B** — `notebooks/eda/session_2_eda_loading_and_inspection_part_B.ipynb`

Deep inspection of `inventory.csv` and `suppliers.csv`:

- Shape validation: `inventory.csv` → **1,825 rows × 7 columns** (daily diary: one row per product per day)
- `suppliers.csv` → **3 rows × 4 columns** — confirmed static reference table (not a time-series)
- Column semantics documented: `closing_stock`, `stockout_flag`, `reorder_triggered`, `lead_time_days`
- Confirmed the data structure underpinning ROP simulation

---

## 🗂️ Dataset Schema

### `transactions.csv` (cleaned)
| Column | Type | Description |
|--------|------|-------------|
| date | object → datetime | Transaction date |
| product_id | object | Product identifier (P001–P005) |
| units_sold | int | Daily units sold (Poisson-distributed) |
| revenue | float | `units_sold × unit_price` |
| cogs | float | `units_sold × unit_cost` |
| gross_profit | float | `revenue − cogs` |

### `inventory.csv`
| Column | Type | Description |
|--------|------|-------------|
| date | object | Date of snapshot |
| product_id | object | Product identifier |
| closing_stock | int | End-of-day stock level |
| stockout_flag | int | 1 if stock = 0, else 0 |
| reorder_triggered | int | 1 if reorder fired on this day |
| supplier_id | object | Assigned supplier |
| lead_time_days | int | Base lead time (before noise) |

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Data Engineering | Python, Pandas, NumPy, Faker |
| Visualization | Matplotlib, Seaborn, Plotly |
| AI / Forecasting | XGBoost, Scikit-learn |
| Optimization | SciPy |
| Deployment | Streamlit |
| Notebooks | JupyterLab |
| DevOps | Git, GitHub |

---

## ▶️ Quick Start

```bash
git clone https://github.com/dominator959/ResilioChain.git
cd ResilioChain

# Create and activate environment
conda create -n resiliochain python=3.11 -y
conda activate resiliochain

# Install dependencies
pip install -r requirements.txt

# Phase 1 — Generate all datasets
python src/data_generator.py

# Phase 2 — Open EDA notebooks
jupyter lab notebooks/eda/
```

---

## 📊 Commit History

| Date | Session | Description | Author |
|------|---------|-------------|--------|
| 2026-06-01 | 2 | Complete Session 2 EDA — Part A (transactions + products inspection) | faizantoheed456 |
| 2026-06-01 | 2 | Complete Session 2 EDA — Part B (inventory + suppliers inspection) | dominator959 |
| 2026-05-31 | 1 | Session 1: Generating a Data Engine (data reformatted) | faizantoheed456 |
| 2026-05-31 | 1 | Session 1: Generating a Data Engine | faizantoheed456 |
| 2026-05-31 | — | Revise project structure formatting in README | dominator959 |
| 2026-05-31 | — | Add project folder structure | dominator959 |
| 2026-05-31 | — | Add professional README with project roadmap | dominator959 |
| 2026-05-31 | — | Initial project structure and requirements | dominator959 |
| 2026-05-31 | — | Initial commit | dominator959 |

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

*Supply Chain Data Science Portfolio Project — actively being developed.*
