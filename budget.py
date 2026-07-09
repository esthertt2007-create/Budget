import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Setup Page Configuration
st.set_page_config(page_title="Union Budget Intelligence Dashboard", layout="wide")
st.title("🏛️ Union Budget Advanced Intelligence & Forecasting Platform")
st.markdown("---")

# 2. Comprehensive Multi-Year Dataset Matrix (2014-2015 to 2026-2027)
@st.cache_data
def load_budget_data():
    years_timeline = [
        "2014-2015", "2015-2016", "2016-2017", "2017-2018", 
        "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", 
        "2023-2024", "2024-2025", "2025-2026", "2026-2027"
    ]
    
    baselines = {
        "Rural Development": [83000, 88000, 95000, 105000, 112000, 118000, 122000, 136000, 140000, 150000, 157000, 165000, 192000],
        "Agriculture & Farmers Welfare": [31000, 37000, 45000, 52000, 58000, 65000, 72000, 115000, 118000, 120000, 115000, 125000, 132000],
        "Education": [68000, 71000, 74000, 79000, 85000, 89000, 93000, 88000, 92000, 95000, 92000, 105000, 112000],
        "Health & Family Welfare": [37000, 41000, 43000, 48000, 53000, 63000, 65000, 71000, 74000, 86000, 86000, 94000, 101000],
        "Infrastructure & Roads": [65000, 74000, 83000, 96000, 102000, 115000, 120000, 134000, 142000, 155000, 165000, 195000, 210000],
        "Defence": [222000, 246000, 258000, 350000, 375000, 405000, 430000, 471000, 525000, 585000, 594000, 643000, 675000],
        "Home Affairs": [61000, 69000, 77000, 83000, 92000, 103000, 114000, 139000, 143000, 166000, 172000, 191000, 203000],
        "Railways": [30000, 32000, 41000, 45000, 53000, 62000, 68000, 110000, 137000, 240000, 245000, 265000, 280000],
        "Consumer Affairs, Food & Public Distribution": [115000, 124000, 135000, 145000, 160000, 175000, 182000, 290000, 240000, 205000, 213000, 231000, 242000],
        "Finance & Economic Affairs": [51000, 57000, 61000, 65000, 71000, 78000, 83000, 91000, 98000, 108000, 112000, 126000, 135000],
        "Communications & IT": [21000, 24000, 29000, 32000, 35000, 38000, 42000, 68000, 72000, 93000, 98000, 111000, 118000],
        "New & Renewable Energy": [25000, 29000, 34000, 41000, 44000, 48000, 52000, 57000, 63000, 70000, 78000, 93000, 102000],
        "Social Justice & Empowerment": [7100, 7900, 8500, 10000, 11200, 12100, 12800, 11500, 12300, 13800, 14200, 16000, 17200]
    }
    
    rows = []
    for dept, budgets in baselines.items():
        for yr, bgt in zip(years_timeline, budgets):
            rows.append({"Department": dept, "Year": yr, "Budget": bgt})
            
    base_df = pd.DataFrame(rows)
    
    # Generate cumulative total mapping rows dynamically
    total_rows = []
    for yr in years_timeline:
        yearly_sum = base_df[base_df["Year"] == yr]["Budget"].sum()
        total_rows.append({"Department": "TOTAL (All 13 Sectors Summed)", "Year": yr, "Budget": yearly_sum})
        
    total_df = pd.DataFrame(total_rows)
    return pd.concat([base_df, total_df], ignore_index=True)

df = load_budget_data()

# Variance tracking calculation function for color status allocation
def compute_color_gradient(data_frame):
    changes = data_frame["Budget"].diff().fillna(0)
    return ["#10B981" if x >= 0 else "#EF4444" for x in changes]

# 3. Sidebar Filters Management Framework
st.sidebar.header("Navigation Framework")

core_options = sorted(list(df["Department"].unique()))
if "TOTAL (All 13 Sectors Summed)" in core_options:
    core_options.remove("TOTAL (All 13 Sectors Summed)")
dropdown_menu_options = ["COMBINED MATRIX VIEW", "TOTAL (All 13 Sectors Summed)"] + core_options

selected_dept = st.sidebar.selectbox("Select Target Analytics Focus", dropdown_menu_options)

years_list = list(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Target Fiscal Year", years_list)

# --- Dynamic Year-over-Year Cross Comparison Control Group ---
st.sidebar.markdown("---")
st.sidebar.header("🔄 Custom Multi-Year Variance Tool")
year_base = st.sidebar.selectbox("Select Base Year (Year A)", years_list, index=0)
year_comp = st.sidebar.selectbox("Select Comparison Year (Year B)", years_list, index=len(years_list)-1)

is_combined = selected_dept == "COMBINED MATRIX VIEW"
is_total = selected_dept == "TOTAL (All 13 Sectors Summed)"

# 4. Core Visual Dashboard Generation Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📈 Allocation Analysis: {selected_dept}")
    
    if is_combined:
        combined_matrix_df = df[df["Department"] != "TOTAL (All 13 Sectors Summed)"]
        fig1 = px.bar(
            combined_matrix_df, x="Year", y="Budget", color="Department",
            labels={"Budget": "Allocation Value (Cr)"},
            title="Comparative Inter-Sector Allocation Projections"
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        dept_all_years_df = df[df["Department"] == selected_dept].reset_index(drop=True)
        dept_all_years_df["Color_Status"] = compute_color_gradient(dept_all_years_df)
        
        fig1 = px.bar(
            dept_all_years_df, x="Year", y="Budget",
            labels={"Budget": "Allocation Value (Cr)"},
            color="Color_Status",
            color_discrete_map={"#10B981": "#10B981", "#EF4444": "#EF4444"}
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📋 Contextual Statistics")
    
    if is_combined:
        active_stats_df = df[df["Department"] == "TOTAL (All 13 Sectors Summed)"].reset_index(drop=True)
        selection_filter = df[(df["Department"] == "TOTAL (All 13 Sectors Summed)") & (df["Year"] == selected_year)]
    else:
        active_stats_df = df[df["Department"] == selected_dept].reset_index(drop=True)
        selection_filter = df[(df["Department"] == selected_dept) & (df["Year"] == selected_year)]
        
    max_budget = active_stats_df["Budget"].max()
    min_budget = active_stats_df["Budget"].min()
    avg_budget = active_stats_df["Budget"].mean()
    current_val = selection_filter["Budget"].values[0] if not selection_filter.empty else 0
    
    label_prefix = "Total System" if is_combined else "Sector"
    st.metric(label=f"Selected Allocation ({selected_year})", value=f"₹ {current_val:,} Cr")
    st.metric(label=f"Peak {label_prefix} Value (Max)", value=f"₹ {max_budget:,} Cr")
    st.metric(label=f"Baseline {label_prefix} Value (Min)", value=f"₹ {min_budget:,} Cr")
    st.metric(label=f"Arithmetic Allocation Mean", value=f"₹ {avg_budget:,.2f} Cr")

# --- Dynamic Year Comparison Output Metric Banner ---
st.markdown("---")
st.subheader(f"⏱️ Custom Delta Computations: {year_base} vs {year_comp}")

# Determine data subset based on target selection
if is_combined:
    comp_df = df[df["Department"] == "TOTAL (All 13 Sectors Summed)"]
else:
    comp_df = df[df["Department"] == selected_dept]

val_a = comp_df[comp_df["Year"] == year_base]["Budget"].values[0]
val_b = comp_df[comp_df["Year"] == year_comp]["Budget"].values[0]
absolute_drift = val_b - val_a
percentage_drift = (absolute_drift / val_a) * 100 if val_a != 0 else 0

cm1, cm2, cm3 = st.columns(3)
with cm1:
    st.metric(label=f"Base Allocation ({year_base})", value=f"₹ {val_a:,} Cr")
with cm2:
    st.metric(label=f"Target Allocation ({year_comp})", value=f"₹ {val_b:,} Cr")
with cm3:
    st.metric(
        label="Calculated Drift Variance", 
        value=f"₹ {absolute_drift:,} Cr", 
        delta=f"{percentage_drift:+.2f}%"
    )

st.markdown("---")

# 5. Advanced Macro Forecasting Block (With Funds Target Callout and Graph Indicators)
st.subheader("🔮 Predictive Macro Forecasting Engine (Target: 2027-2028)")

if is_combined:
    calc_target_df = df[df["Department"] == "TOTAL (All 13 Sectors Summed)"].reset_index(drop=True)
else:
    calc_target_df = df[df["Department"] == selected_dept].reset_index(drop=True)

growth_rates = calc_target_df["Budget"].diff().dropna()
avg_growth = growth_rates.mean()
latest_known_budget = calc_target_df.iloc[-1]["Budget"]
forecast_val = latest_known_budget + avg_growth

forecast_matrix = calc_target_df[["Year", "Budget"]].copy()
new_row = pd.DataFrame([{"Year": "2027-2028 (Forecast)", "Budget": forecast_val}])
forecast_matrix = pd.concat([forecast_matrix, new_row], ignore_index=True)
forecast_matrix["Color_Status"] = compute_color_gradient(forecast_matrix)

f_col1, f_col2 = st.columns([1, 2])
with f_col1:
    st.write("")
    st.info(f"### Predicted Value:\n**₹ {forecast_val:,.2f} Cr**")
    st.markdown(f"""
    **Forecasting Metrics Applied:**
    * Target Scope Array: `{"Cumulative Profile" if is_combined else selected_dept}`
    * Historical Linear Delta Addition: `+₹ {avg_growth:,.2f} Cr`
    * Base Period Target Value: `₹ {latest_known_budget:,} Cr`
    """)

with f_col2:
    # Build standard bar visualization
    fig2 = px.bar(
        forecast_matrix, x="Year", y="Budget",
        title=f"Predictive Vector Pathway featuring 2027-2028 Allocation Target for {selected_dept}",
        color="Color_Status",
        color_discrete_map={"#10B981": "#10B981", "#EF4444": "#EF4444"}
    )
    # Add a horizontal line to highlight the exact allocation ceiling target line clearly
    fig2.add_shape(
        type="line", x0=0, x1=len(forecast_matrix)-1, y0=forecast_val, y1=forecast_val,
        line=dict(color="Gold", width=3, dash="dashdot")
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 6. Deep Work AI Analytical Insights Module
st.subheader("🤖 In-Depth AI Evaluation Suite")

last_year_val = calc_target_df.iloc[-2]["Budget"]
latest_year_val = calc_target_df.iloc[-1]["Budget"]
yoy_change = latest_year_val - last_year_val
pct_change = (yoy_change / last_year_val) * 100

st.markdown(f"### 📑 Deep Fiscal Profile Report for: **{selected_dept}**")

if yoy_change >= 0:
    st.markdown("#### 🟢 Structural Plus Points (Fiscal Strengths Analysis)")
    st.markdown(f"""
    * **Capital Injection Momentum:** The current financial trajectory reflects an allocation shift of **₹ {yoy_change:,} Cr** (+{pct_change:.2f}%), indicating robust structural development backing.
    * **Long-Term Resource Security:** Consistent baseline scaling mitigates execution bottlenecks and stabilizes ongoing capital investments.
    * **Reliable Expansion Velocity:** The long-term average system scaling velocity of **₹ {avg_growth:,.2f} Cr** per annum ensures structured growth.
    """)
    st.markdown("#### 🔴 Structural Minus Points (Fiscal Vulnerability Analysis)")
    st.markdown(f"""
    * **Inflation Outpaced Risk:** If real-world commodity inflation outruns this nominal budget expansion rate, localized development metrics may face uncalculated tightening parameters.
    * **Liquidity Distribution Overheads:** Cumulative growth spikes might conceal sub-departmental budgetary pressures where non-priority sub-tracks stay underfunded.
    """)
else:
    st.markdown("#### 🟢 Structural Plus Points (Fiscal Consolidation Analysis)")
    st.markdown(f"""
    * **Targeted Capital Optimization:** The resource tightening framework of **₹ {abs(yoy_change):,} Cr** ({pct_change:.2f}%) highlights a dedicated systemic reduction of operational leakages.
    * **Asset-Light Operational Adjustments:** Tightened constraints encourage structural shifts toward performance-optimized asset frameworks.
    """)
    st.markdown("#### 🔴 Structural Minus Points (Fiscal Bottleneck Risks)")
    st.markdown(f"""
    * **Development Strains:** Negative investment slopes slow down asset rollout pipelines, increasing structural deployment delays.
    * **Liquidity Margin Reductions:** Lowered capital margins limit swift response capabilities against abrupt domestic market changes.
    """)

st.markdown("#### 🔍 Structural Component Decomposition Breakdown")
if is_combined or is_total:
    st.markdown("""
    * **Primary Capital Drivers (+):** *Infrastructure & Roads*, *Railways*, and *Defence* represent the system's primary liquidity columns, driving the majority of central resource additions.
    * **Systemic Balance Weights:** *Education* and *Health & Family Welfare* exhibit gradual, non-volatile adjustments, ensuring defensive social infrastructure stability.
    * **Sub-Departmental Volatility Check:** Allocation adjustments in *Consumer Affairs, Food & Public Distribution* display higher cross-cycle divergence, driven by shifts in central commodity subsidies.
    """)
else:
    st.markdown(f"""
    * **Core Baseline Component Performance:** The operational path for **{selected_dept}** runs above a baseline minimum floor of **₹ {min_budget:,} Cr** established during the early tracking phases.
    * **System Drift Momentum:** The structural trend analysis signals that long-term asset movements follow an average annual momentum index of **₹ {avg_growth:,.2f} Cr** heading directly into the 2027-2028 forecast window.
    """)
