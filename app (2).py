"""
╔══════════════════════════════════════════════════════════════╗
║  Afficionado Coffee Roasters — Product Analytics Dashboard   ║
║  SELF-CONTAINED — No external utils / modules required       ║
╚══════════════════════════════════════════════════════════════╝

HOW TO RUN:
  1. pip install -r requirements.txt
  2. streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Afficionado Coffee Roasters",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #FAF9F6; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #EDE9E2;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    text-align: center;
    margin-bottom: 0.5rem;
}
.kpi-label {
    font-size: 11px; color: #999999; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.8px;
}
.kpi-value { font-size: 28px; font-weight: 700; color: #1A1A1A; margin-top: 6px; }
.kpi-sub   { font-size: 12px; color: #BBBBBB; margin-top: 4px; }

/* Insight boxes */
.insight-box {
    background: #FFF8F0;
    border-left: 4px solid #C45E1A;
    padding: 0.9rem 1.1rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 0.9rem;
    font-size: 13px;
    color: #444444;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  COLOUR MAP
# ─────────────────────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Coffee":             "#3B6BA5",
    "Tea":                "#2E8B57",
    "Bakery":             "#D4784A",
    "Drinking Chocolate": "#7B4FA6",
    "Coffee beans":       "#8B6914",
    "Branded":            "#4A9BB5",
    "Loose Tea":          "#6DAE6B",
    "Flavours":           "#E0954A",
    "Packaged Chocolate": "#B05F8A",
}

# ─────────────────────────────────────────────────────────────────────────────
#  DATA LOADER  (fully self-contained — no utils module needed)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the Excel file from the same folder as this script (or /data sub-folder)."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Try same folder first, then data/ sub-folder
    candidates = [
        os.path.join(script_dir,         "Afficionado_Coffee_Roasters.xlsx"),
        os.path.join(script_dir, "data", "Afficionado_Coffee_Roasters.xlsx"),
    ]
    path = None
    for c in candidates:
        if os.path.exists(c):
            path = c
            break

    if path is None:
        st.error(
            "❌ **Data file not found.**\n\n"
            "Place `Afficionado_Coffee_Roasters.xlsx` in the **same folder** as `app.py` "
            "or inside a `data/` sub-folder, then refresh the page."
        )
        st.stop()

    df = pd.read_excel(path)
    df["revenue"]          = df["transaction_qty"] * df["unit_price"]
    df["transaction_time"] = df["transaction_time"].astype(str)
    df["hour"] = (
        df["transaction_time"]
        .str[:2]
        .apply(lambda x: int(x) if x.strip().isdigit() else 0)
    )
    return df


df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☕ Afficionado")
    st.markdown("**Product Analytics Dashboard**")
    st.divider()

    sel_loc = st.selectbox(
        "🏪 Store Location",
        ["All Stores"] + sorted(df["store_location"].unique().tolist()),
    )
    sel_cat = st.selectbox(
        "📦 Category",
        ["All Categories"] + sorted(df["product_category"].unique().tolist()),
    )
    top_n = st.slider("🏆 Top N Products", 5, 30, 10, 5)

    st.divider()
    page = st.radio(
        "📄 Navigate",
        [
            "📊 Overview",
            "🏷️ Product Analysis",
            "📈 Revenue Deep Dive",
            "🗺️ Store Comparison",
            "📋 Raw Data",
        ],
    )
    st.divider()
    st.caption("149,116 transactions | 3 stores | 80 SKUs | 2025")

# ─────────────────────────────────────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
filt = df.copy()
if sel_loc != "All Stores":
    filt = filt[filt["store_location"] == sel_loc]
if sel_cat != "All Categories":
    filt = filt[filt["product_category"] == sel_cat]

# ─────────────────────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def kpi_card(label: str, value: str, sub: str) -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f"</div>"
    )


def insight_box(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def product_table(df_in: pd.DataFrame) -> pd.DataFrame:
    """Build full product-level aggregation with all KPI columns."""
    p = (
        df_in.groupby(["product_detail", "product_type", "product_category"])
        .agg(Revenue=("revenue", "sum"), Units=("transaction_qty", "sum"),
             Transactions=("transaction_id", "count"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )
    total = p["Revenue"].sum()
    p["Rev %"]        = (p["Revenue"] / total * 100).round(2)
    p["Cum Rev %"]    = p["Rev %"].cumsum().round(2)
    p["Revenue Rank"] = p["Revenue"].rank(ascending=False).astype(int)
    p["Volume Rank"]  = p["Units"].rank(ascending=False).astype(int)
    p["Rank Diff"]    = p["Volume Rank"] - p["Revenue Rank"]
    p["Avg Price"]    = (p["Revenue"] / p["Units"]).round(2)
    return p


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.title("☕ Afficionado Coffee Roasters")
    st.markdown("**Product Optimization & Revenue Contribution Analysis — 2025**")
    st.divider()

    # ── KPIs ─────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_card("Total Revenue",  f"${filt['revenue'].sum():,.0f}",       "All selected stores"),  unsafe_allow_html=True)
    c2.markdown(kpi_card("Units Sold",     f"{filt['transaction_qty'].sum():,}",   "Total quantity"),        unsafe_allow_html=True)
    c3.markdown(kpi_card("Transactions",   f"{len(filt):,}",                       "Individual orders"),     unsafe_allow_html=True)
    c4.markdown(kpi_card("Active SKUs",    str(filt["product_detail"].nunique()),  "Unique products"),       unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Category pie + Store bar ──────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        cat_rev = (filt.groupby("product_category")["revenue"]
                   .sum().reset_index().sort_values("revenue", ascending=False))
        fig = go.Figure(go.Pie(
            labels=cat_rev["product_category"],
            values=cat_rev["revenue"].round(2),
            hole=0.50,
            marker_colors=[CAT_COLORS.get(c, "#AAA") for c in cat_rev["product_category"]],
            textinfo="label+percent",
            textfont_size=11,
            hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig.update_layout(title="Revenue by Category", height=370,
                          paper_bgcolor="white", showlegend=False,
                          margin=dict(t=50, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        store_rev = (filt.groupby("store_location")["revenue"]
                     .sum().reset_index().sort_values("revenue", ascending=False))
        fig = px.bar(
            store_rev, x="store_location", y="revenue",
            color="store_location",
            color_discrete_sequence=["#3B6BA5", "#2E8B57", "#D4784A"],
            title="Revenue by Store Location",
            text=store_rev["revenue"].apply(lambda x: f"${x:,.0f}"),
        )
        fig.update_layout(height=370, showlegend=False, paper_bgcolor="white",
                          plot_bgcolor="#F9F9F9",
                          yaxis=dict(showgrid=True, gridcolor="#EEE", title="Revenue ($)"),
                          xaxis=dict(showgrid=False, title=""),
                          margin=dict(t=50, b=10))
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # ── Top N Products ────────────────────────────────────────────────────────
    top_prod = (filt.groupby(["product_detail", "product_category"])
                .agg(Revenue=("revenue", "sum"), Units=("transaction_qty", "sum"))
                .reset_index().sort_values("Revenue", ascending=False).head(top_n))

    fig = go.Figure(go.Bar(
        x=top_prod["Revenue"],
        y=top_prod["product_detail"],
        orientation="h",
        marker_color=[CAT_COLORS.get(c, "#AAA") for c in top_prod["product_category"]],
        text=top_prod["Revenue"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        title=f"Top {top_n} Products by Revenue",
        height=max(380, top_n * 42),
        paper_bgcolor="white", plot_bgcolor="#F9F9F9",
        yaxis=dict(categoryorder="total ascending", title=""),
        xaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#EEE"),
        margin=dict(t=50, b=20, l=10, r=90),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Hourly trend ──────────────────────────────────────────────────────────
    hourly = filt.groupby("hour")["revenue"].sum().reset_index()
    fig = px.area(hourly, x="hour", y="revenue",
                  title="Revenue by Hour of Day",
                  color_discrete_sequence=["#3B6BA5"], markers=True)
    fig.update_layout(height=280, paper_bgcolor="white", plot_bgcolor="#F9F9F9",
                      xaxis=dict(title="Hour of Day", dtick=1, showgrid=False),
                      yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#EEE"),
                      margin=dict(t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # ── Key Insights ──────────────────────────────────────────────────────────
    st.markdown("### 💡 Key Insights")
    col1, col2 = st.columns(2)
    with col1:
        insight_box("☕ <b>Coffee + Tea = 66.7% of revenue.</b> These two categories are the business core. Any supply or price disruption would have outsized impact.")
        insight_box("🍫 <b>Drinking Chocolate is the efficiency champion</b> at $18,104 revenue per SKU with just 4 products. Its top 2 products are #1 and #2 across the entire menu.")
    with col2:
        insight_box("📐 <b>Pareto confirmed:</b> 42 of 80 products drive 80% of revenue. The bottom 38 SKUs contribute only 20%, signalling a clear rationalisation opportunity.")
        insight_box("⚠️ <b>Loose Tea has the worst SKU efficiency</b> — 8 products averaging just $1,402 each. Reducing to 3 best performers would free menu space with minimal revenue impact.")


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — PRODUCT ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🏷️ Product Analysis":
    st.title("🏷️ Product Analysis")
    st.markdown("Hero products, underperformers, and popularity vs revenue comparison.")
    st.divider()

    prod = product_table(filt)

    # Scatter
    st.markdown("### 🔵 Popularity vs Revenue — All Products")
    fig = px.scatter(
        prod, x="Units", y="Revenue",
        color="product_category", size="Revenue", size_max=45,
        hover_name="product_detail",
        color_discrete_map=CAT_COLORS,
        hover_data={"Units": True, "Revenue": ":.2f", "Rev %": True, "Avg Price": True},
        title="Units Sold vs Revenue (bubble size = revenue)",
    )
    fig.update_layout(height=480, paper_bgcolor="white", plot_bgcolor="#F9F9F9",
                      xaxis=dict(showgrid=True, gridcolor="#EEE", title="Units Sold"),
                      yaxis=dict(showgrid=True, gridcolor="#EEE", title="Revenue ($)"),
                      legend=dict(title="Category"))
    st.plotly_chart(fig, use_container_width=True)

    # Hero / Underperformer tables
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### 🏆 Top {top_n} Hero Products")
        td = prod.head(top_n)[["product_detail", "product_category",
                                "Revenue", "Units", "Rev %", "Avg Price"]].copy()
        td.columns = ["Product", "Category", "Revenue ($)", "Units", "Rev %", "Avg Price ($)"]
        td["Revenue ($)"]   = td["Revenue ($)"].apply(lambda x: f"${x:,.2f}")
        td["Units"]         = td["Units"].apply(lambda x: f"{x:,}")
        td["Rev %"]         = td["Rev %"].apply(lambda x: f"{x:.2f}%")
        td["Avg Price ($)"] = td["Avg Price ($)"].apply(lambda x: f"${x:.2f}")
        st.dataframe(td.reset_index(drop=True), use_container_width=True, height=400)

    with col2:
        st.markdown("### ⚠️ Bottom 10 Underperformers")
        bd = prod.tail(10)[["product_detail", "product_category",
                             "Revenue", "Units", "Rev %", "Avg Price"]].copy()
        bd.columns = ["Product", "Category", "Revenue ($)", "Units", "Rev %", "Avg Price ($)"]
        bd["Revenue ($)"]   = bd["Revenue ($)"].apply(lambda x: f"${x:,.2f}")
        bd["Units"]         = bd["Units"].apply(lambda x: f"{x:,}")
        bd["Rev %"]         = bd["Rev %"].apply(lambda x: f"{x:.2f}%")
        bd["Avg Price ($)"] = bd["Avg Price ($)"].apply(lambda x: f"${x:.2f}")
        st.dataframe(bd.reset_index(drop=True), use_container_width=True, height=400)

    # Rank divergence
    st.markdown("### 🔄 Rank Divergence: Volume Rank vs Revenue Rank")
    st.caption("🟢 Positive = sells more units than revenue rank suggests (popular but cheaper).  🔴 Negative = fewer units but high revenue (premium, less frequent).")
    div = prod.nlargest(20, "Units").sort_values("Rank Diff", ascending=False)
    fig = go.Figure(go.Bar(
        x=div["Rank Diff"], y=div["product_detail"], orientation="h",
        marker_color=["#2E8B57" if v >= 0 else "#C0392B" for v in div["Rank Diff"]],
        hovertemplate="<b>%{y}</b><br>Rank Diff: %{x}<extra></extra>",
    ))
    fig.update_layout(
        height=530, title="Volume Rank – Revenue Rank  (Top 20 by Volume)",
        xaxis=dict(title="Rank Difference", showgrid=True, gridcolor="#EEE",
                   zeroline=True, zerolinecolor="#AAA"),
        yaxis=dict(categoryorder="total ascending", title=""),
        paper_bgcolor="white", plot_bgcolor="#F9F9F9",
        margin=dict(l=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Full table
    st.markdown("### 📋 Full Product Performance Table")
    disp = prod[["product_detail", "product_type", "product_category",
                 "Revenue", "Units", "Rev %", "Cum Rev %", "Avg Price", "Revenue Rank"]].copy()
    disp.columns = ["Product", "Type", "Category", "Revenue ($)",
                    "Units", "Rev %", "Cumulative %", "Avg Price ($)", "Revenue Rank"]
    st.dataframe(disp, use_container_width=True, height=450)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — REVENUE DEEP DIVE
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📈 Revenue Deep Dive":
    st.title("📈 Revenue Deep Dive")
    st.markdown("Pareto curve, revenue treemap, product-type breakdown, SKU efficiency.")
    st.divider()

    prod_p = (filt.groupby(["product_detail", "product_category"])["revenue"]
              .sum().reset_index().sort_values("revenue", ascending=False).reset_index(drop=True))
    prod_p["rev_pct"] = prod_p["revenue"] / prod_p["revenue"].sum() * 100
    prod_p["cum_pct"] = prod_p["rev_pct"].cumsum()
    prod_p["rank"]    = range(1, len(prod_p) + 1)
    pareto80          = int((prod_p["cum_pct"] <= 80).sum())

    # Pareto chart
    st.markdown("### 📐 Pareto Curve — Revenue Concentration")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=prod_p["rank"], y=prod_p["rev_pct"],
        name="Individual Rev %",
        marker_color=[CAT_COLORS.get(c, "#AAA") for c in prod_p["product_category"]],
        opacity=0.75,
        customdata=prod_p["product_detail"],
        hovertemplate="<b>%{customdata}</b><br>Rev: %{y:.2f}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=prod_p["rank"], y=prod_p["cum_pct"],
        name="Cumulative %", yaxis="y2",
        line=dict(color="#C45E1A", width=2.5), mode="lines",
    ))
    fig.add_hline(y=80, line=dict(color="red", dash="dash", width=1.5), yref="y2",
                  annotation_text=" 80% Revenue", annotation_font=dict(color="red", size=11))
    fig.add_vline(x=pareto80, line=dict(color="#2E8B57", dash="dot", width=1.5),
                  annotation_text=f" {pareto80} products →",
                  annotation_font=dict(color="#2E8B57", size=11))
    fig.update_layout(
        height=430,
        title=f"Pareto: {pareto80} of {len(prod_p)} products → 80% of ${filt['revenue'].sum():,.0f} revenue",
        yaxis=dict(title="Individual Rev %", showgrid=True, gridcolor="#EEE"),
        yaxis2=dict(title="Cumulative Rev %", overlaying="y", side="right",
                    range=[0, 108], showgrid=False),
        xaxis=dict(title="Product Rank", showgrid=False),
        paper_bgcolor="white", plot_bgcolor="#F9F9F9",
        legend=dict(orientation="h", y=1.08, x=0.3),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Products → 80% Revenue", f"{pareto80} of {len(prod_p)}")
    c2.metric("Top 10 Share",           f"{prod_p.head(10)['rev_pct'].sum():.1f}%")
    c3.metric("Long-tail SKUs",         f"{len(prod_p) - pareto80} → 20%")
    st.markdown("<br>", unsafe_allow_html=True)

    # Treemap
    st.markdown("### 🌳 Revenue Treemap — Category → Type → Product")
    tree = (filt.groupby(["product_category", "product_type", "product_detail"])["revenue"]
            .sum().reset_index())
    tree.columns = ["Category", "Type", "Product", "Revenue"]
    fig = px.treemap(tree, path=["Category", "Type", "Product"],
                     values="Revenue", color="Category",
                     color_discrete_map=CAT_COLORS)
    fig.update_layout(height=530, paper_bgcolor="white",
                      margin=dict(t=30, b=10, l=10, r=10))
    fig.update_traces(textinfo="label+value+percent parent")
    st.plotly_chart(fig, use_container_width=True)

    # Product type bar
    st.markdown("### 🏷️ Top 15 Product Types by Revenue")
    type_rev = (filt.groupby(["product_category", "product_type"])["revenue"]
                .sum().reset_index().sort_values("revenue", ascending=False).head(15))
    type_rev.columns = ["Category", "Product Type", "Revenue"]
    fig = px.bar(type_rev, x="Revenue", y="Product Type",
                 color="Category", orientation="h",
                 color_discrete_map=CAT_COLORS)
    fig.update_layout(height=530,
                      yaxis=dict(categoryorder="total ascending", title=""),
                      xaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#EEE"),
                      paper_bgcolor="white", plot_bgcolor="#F9F9F9",
                      legend=dict(title="Category"))
    st.plotly_chart(fig, use_container_width=True)

    # SKU efficiency
    st.markdown("### ⚡ Revenue per SKU — Category Efficiency")
    sku = (filt.groupby("product_category")
           .agg(Revenue=("revenue", "sum"), SKUs=("product_detail", "nunique"))
           .reset_index())
    sku["Rev_per_SKU"] = (sku["Revenue"] / sku["SKUs"]).round(0)
    sku = sku.sort_values("Rev_per_SKU", ascending=False)
    fig = go.Figure(go.Bar(
        x=sku["product_category"], y=sku["Rev_per_SKU"],
        marker_color=[CAT_COLORS.get(c, "#AAA") for c in sku["product_category"]],
        text=sku["Rev_per_SKU"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Rev/SKU: $%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        height=380, title="Revenue per SKU by Category  (higher = more efficient)",
        xaxis=dict(title="", tickangle=-15),
        yaxis=dict(title="Revenue per SKU ($)", showgrid=True, gridcolor="#EEE"),
        paper_bgcolor="white", plot_bgcolor="#F9F9F9",
        margin=dict(t=50, b=60),
    )
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — STORE COMPARISON
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Store Comparison":
    st.title("🗺️ Store Comparison")
    st.markdown("Cross-location revenue, category mix, and per-store top products.")
    st.divider()

    store_cat = (df.groupby(["store_location", "product_category"])["revenue"]
                 .sum().reset_index())
    store_cat.columns = ["Store", "Category", "Revenue"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(store_cat, x="Store", y="Revenue", color="Category",
                     barmode="group", color_discrete_map=CAT_COLORS,
                     title="Revenue by Store & Category (Grouped)")
        fig.update_layout(height=430, paper_bgcolor="white", plot_bgcolor="#F9F9F9",
                          yaxis=dict(showgrid=True, gridcolor="#EEE", title="Revenue ($)"),
                          xaxis=dict(title=""),
                          legend=dict(font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Plotly 6.x removed barnorm — compute percentages manually
        pivot    = store_cat.pivot_table(index="Store", columns="Category",
                                         values="Revenue", aggfunc="sum").fillna(0)
        pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
        pct_long  = pivot_pct.reset_index().melt(id_vars="Store",
                                                  var_name="Category",
                                                  value_name="Revenue %")
        fig2 = px.bar(pct_long, x="Store", y="Revenue %", color="Category",
                      barmode="relative",
                      color_discrete_map=CAT_COLORS,
                      title="Category Mix % by Store (Normalised)",
                      hover_data={"Revenue %": ":.1f"})
        fig2.update_layout(height=430, paper_bgcolor="white", plot_bgcolor="#F9F9F9",
                           yaxis=dict(title="% of Store Revenue",
                                      showgrid=True, gridcolor="#EEE", range=[0, 101]),
                           xaxis=dict(title=""),
                           legend=dict(font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    # KPI table
    st.markdown("### 📊 Store KPI Summary")
    skpi = (df.groupby("store_location")
            .agg(Revenue=("revenue", "sum"), Units=("transaction_qty", "sum"),
                 Transactions=("transaction_id", "count"),
                 Products=("product_detail", "nunique"),
                 Avg_Order=("revenue", "mean"))
            .reset_index().sort_values("Revenue", ascending=False))
    skpi.columns = ["Store", "Revenue ($)", "Units", "Transactions", "Active SKUs", "Avg Order ($)"]
    skpi["Revenue ($)"]   = skpi["Revenue ($)"].apply(lambda x: f"${x:,.2f}")
    skpi["Units"]         = skpi["Units"].apply(lambda x: f"{x:,}")
    skpi["Transactions"]  = skpi["Transactions"].apply(lambda x: f"{x:,}")
    skpi["Avg Order ($)"] = skpi["Avg Order ($)"].apply(lambda x: f"${x:.2f}")
    st.dataframe(skpi.reset_index(drop=True), use_container_width=True)

    # Per-store top products
    st.markdown("### 🏆 Top Products for a Specific Store")
    sel_store = st.selectbox("Select Store", sorted(df["store_location"].unique()))
    n_s       = st.slider("Top N", 5, 20, 10)
    sp = (df[df["store_location"] == sel_store]
          .groupby(["product_detail", "product_category"])["revenue"]
          .sum().reset_index().sort_values("revenue", ascending=False).head(n_s))
    sp.columns = ["Product", "Category", "Revenue"]

    fig = go.Figure(go.Bar(
        x=sp["Revenue"], y=sp["Product"], orientation="h",
        marker_color=[CAT_COLORS.get(c, "#AAA") for c in sp["Category"]],
        text=sp["Revenue"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>$%{x:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        height=max(360, n_s * 42),
        title=f"Top {n_s} Products — {sel_store}",
        yaxis=dict(categoryorder="total ascending", title=""),
        xaxis=dict(showgrid=True, gridcolor="#EEE", title="Revenue ($)"),
        paper_bgcolor="white", plot_bgcolor="#F9F9F9",
        margin=dict(t=50, r=90),
    )
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — RAW DATA
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📋 Raw Data":
    st.title("📋 Raw Transaction Data")
    st.markdown(
        f"Showing **{len(filt):,} records** | "
        f"Total Revenue: **${filt['revenue'].sum():,.2f}**"
    )
    st.divider()

    search = st.text_input("🔍 Search by product name", "")
    show   = filt.copy()
    if search:
        show = show[show["product_detail"].str.contains(search, case=False, na=False)]

    st.dataframe(
        show[["transaction_id", "transaction_time", "store_location",
              "product_category", "product_type", "product_detail",
              "transaction_qty", "unit_price", "revenue"]]
        .rename(columns={
            "transaction_id":   "ID",
            "transaction_time": "Time",
            "store_location":   "Store",
            "product_category": "Category",
            "product_type":     "Type",
            "product_detail":   "Product",
            "transaction_qty":  "Qty",
            "unit_price":       "Unit Price ($)",
            "revenue":          "Revenue ($)",
        }),
        use_container_width=True,
        height=500,
    )

    col1, col2, col3 = st.columns(3)
    col1.download_button(
        "⬇️ Download Filtered CSV",
        show.to_csv(index=False).encode("utf-8"),
        "afficionado_filtered.csv",
        "text/csv",
    )
    col2.metric("Records Shown",   f"{len(show):,}")
    col3.metric("Revenue Shown",   f"${show['revenue'].sum():,.2f}")


# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:11px;color:#CCC'>"
    "☕ Afficionado Coffee Roasters — Product Analytics Dashboard | Streamlit + Plotly"
    "</div>",
    unsafe_allow_html=True,
)
