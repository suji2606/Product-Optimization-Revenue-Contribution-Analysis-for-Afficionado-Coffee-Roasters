# ☕ Afficionado Coffee Roasters — Product Analytics Dashboard

## 📁 Folder Structure (IMPORTANT — keep as-is)
```
afficionado_coffee_dashboard/
│
├── app.py                              ← Main Streamlit app  (run this)
├── requirements.txt                    ← Python dependencies
├── README.md                           ← This file
│
├── Afficionado_Coffee_Roasters.xlsx    ← ⚠️  PLACE THE DATA FILE HERE
│                                           (same folder as app.py)
│
└── docs/
    ├── research_paper.md               ← Full EDA & research paper
    └── executive_summary.md            ← Stakeholder executive summary
```

---

## 🚀 How to Run (Step-by-Step)

### Step 1 — Make sure Python 3.9+ is installed
Download from https://www.python.org/downloads/ if needed.

### Step 2 — Open a terminal / command prompt in this folder
```
cd path/to/afficionado_coffee_dashboard
```

### Step 3 — Install dependencies (only needed once)
```
pip install -r requirements.txt
```

### Step 4 — Run the app
```
streamlit run app.py
```

### Step 5 — The app opens automatically in your browser
URL: http://localhost:8501

---

## ⚠️ Important — Data File Location
The Excel file **must** be in the **same folder as app.py**, like this:
```
afficionado_coffee_dashboard/
├── app.py
└── Afficionado_Coffee_Roasters.xlsx   ✅  correct location
```

The app also checks inside a `data/` sub-folder as a fallback.
If the file is missing you will see a clear red error message with instructions.

---

## 📊 Dashboard Pages

| Page | What You Get |
|------|-------------|
| 📊 Overview | KPI cards, category pie, store bars, top-N products, hourly trend, key insights |
| 🏷️ Product Analysis | Popularity vs revenue scatter, hero products, underperformers, rank divergence, full table |
| 📈 Revenue Deep Dive | Pareto curve, treemap, product-type bars, SKU efficiency scores |
| 🗺️ Store Comparison | Grouped & normalised category bars, KPI table, per-store top products |
| 📋 Raw Data | Searchable transaction table, CSV download |

### Sidebar Controls
- 🏪 **Store Location** — filter by store or view all
- 📦 **Category** — drill into one category
- 🏆 **Top N** — adjust how many products show in rankings

---

## 🔑 Key Findings

| Metric | Value |
|--------|-------|
| Total Revenue | $698,812 |
| Total Transactions | 149,116 |
| Total Units Sold | 214,470 |
| Unique Products (SKUs) | 80 |
| Products driving 80% revenue | 42 (Pareto rule) |
| #1 Product | Sustainably Grown Organic Lg — $21,152 |
| Best category efficiency | Drinking Chocolate — $18,104/SKU |
| Worst category efficiency | Loose Tea — $1,402/SKU |
| Store revenue variance | Only 2.8% between stores |

---

## 📄 Documents in /docs
- **research_paper.md** — Full EDA, methodology, analysis, and strategic recommendations
- **executive_summary.md** — Concise summary for stakeholders / management

---
*Built with Python · Streamlit · Plotly · pandas*
