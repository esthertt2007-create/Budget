import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Setup Page Configuration
st.set_page_config(page_title="Union Budget Intelligence Dashboard", layout="wide")
st.title("🏛️ Union Budget Advanced Intelligence & Forecasting Platform")
st.markdown("---")

# 2. Comprehensive Dataset Base Matrix
@st.cache_data
def load_budget_data():
    years_timeline = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2025-2026", "2026-2027"]
    
    baselines = {
        "Rural Development": [105000, 112000, 118000, 122000, 136000, 140000, 150000, 157000, 165000, 177000, 192000],
        "Agriculture & Farmers Welfare": [52000, 58000, 65000, 72000, 115000, 118000, 120000, 115000, 118000, 125000, 132000],
        "Education": [79000, 85000, 89000, 93000, 88000, 92000, 95000, 92000, 98000, 105000, 112000],
        "Health & Family Welfare": [48000, 53000, 63000, 65000, 71000, 74000, 86000, 86000, 89000, 94000, 101000],
        "Infrastructure & Roads": [96000, 102000, 115000, 120000, 134000, 142000, 155000, 165000, 175000, 195000, 210000],
        "Defence": [350000, 375000, 405000, 430000, 471000, 525000, 585000, 594000, 621000, 643000, 675000],
        "Home Affairs": [83000, 92000, 103000, 114000, 139000, 143000, 166000, 172000, 180000, 191000, 203000],
        "Railways": [45000, 53000, 62000, 68000, 110000, 137000, 240000, 245000, 252000, 265000, 280000],
        "Consumer Affairs, Food & Public Distribution": [145000, 160000, 175000, 182000, 290000, 240000, 205000, 213000, 220000, 231000, 242000],
        "Finance & Economic Affairs": [65000, 71000, 78000, 83000, 91000, 98000, 108000, 112000, 119000, 126000, 135000],
        "Communications & IT": [32000, 35000, 38000, 42000, 68000, 72000, 93000, 98000, 104000, 111000, 118000],
        "New & Renewable Energy": [41000, 44000, 48000, 52000, 57000, 63000, 70000, 78000, 85000, 93000, 102000],
        "Social Justice & Empowerment": [10000, 11200, 12100, 12800, 11500, 12300, 13800, 14200, 15100, 16000, 17200]
    }
    
    rows = []
    for dept, budgets in baselines.items():
        for yr, bgt in zip(years_timeline, budgets):
            rows.append({"Department": dept, "Year": yr, "Budget": bgt})
            
    base_df = pd.DataFrame(rows)
    
    # Calculate Total Cumulative Aggregate Row Groupings dynamically
    total_rows = []
    for yr in years_timeline:
        yearly_sum = base_df[base_df["Year"] == yr]["Budget"].sum()
        total_rows.append({"Department": "TOTAL (All 13 Sectors)", "Year": yr, "Budget": yearly_sum})
        
    total_df = pd.DataFrame(total_rows)
    return pd.concat([base_df, total_df], ignore_index=True)

df = load_budget_data()

# Helper function to generate conditional profit/loss variance arrays for color mapping
def compute_color_gradient(data_frame):
    # Quantify year over year change to flag green vs red states
    changes = data_frame["Budget"].diff().fillna(0)
    return ["#10B981" if x >= 0 else "#EF4444" for x in changes]

# 3. Sidebar Setup (Far Left Navigation Panel)
st.sidebar.header("Navigation Framework")
departments_list = list(df["Department"].unique())
selected_dept = st.sidebar.selectbox("Select Target Analytics Focus", departments_list)

years_list = list(df[df["Department"] == selected_dept]["Year"].unique())
selected_year = st.sidebar.selectbox("Select Target Fiscal Year", years_list)

# Split and isolate current selections vs background tracks
filtered_df = df[(df["Department"] == selected_dept) & (df["Year"] == selected_year)]
dept_all_years_df = df[df["Department"] == selected_dept].reset_index(drop=True)

# 4. Core Visuals and Metrics Blocks
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📈 Historical Trend Framework: {selected_dept}")
    dept_all_years_df["Color_Status"] = compute_color_gradient(dept_all_years_df)
    
    fig1 = px.bar(
        dept_all_years_df, x="Year", y="Budget",
        labels={"Budget": "Allocation Value (Cr)"},
        color="Color_Status",
        color_discrete_map={"#10B981": "#10B981", "#EF4444": "#EF4444"}
    )
    fig1.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📋 Core Statistics")
    max_budget = dept_all_years_df["Budget"].max()
    min_budget = dept_all_years_df["Budget"].min()
    avg_budget = dept_all_years_df["Budget"].mean()
    current_val = filtered_df["Budget"].values[0] if not filtered_df.empty else 0
    
    st.metric(label=f"Selected Allocation ({selected_year})", value=f"₹ {current_val:,} Cr")
    st.metric(label="Peak Sector Value (Max)", value=f"₹ {max_budget:,} Cr")
    st.metric(label="Baseline Value (Min)", value=f"₹ {min_budget:,} Cr")
    st.metric(label="Arithmetic Allocation Mean", value=f"₹ {avg_budget:,.2f} Cr")

st.markdown("---")

# 5. Advanced Macro Forecasting Block (Now positioned above AI Insights)
st.subheader("🔮 Predictive Macro Forecasting Engine (Target: 2027-2028)")

growth_rates = dept_all_years_df["Budget"].diff().dropna()
avg_growth = growth_rates.mean()
latest_known_budget = dept_all_years_df.iloc[-1]["Budget"]
forecast_val = latest_known_budget + avg_growth

# Construct forecast visualization matrix
forecast_matrix = dept_all_years_df[["Year", "Budget"]].copy()
new_row = pd.DataFrame([{"Year": "2027-2028 (Forecast)", "Budget": forecast_val}])
forecast_matrix = pd.concat([forecast_matrix, new_row], ignore_index=True)
forecast_matrix["Color_Status"] = compute_color_gradient(forecast_matrix)

f_col1, f_col2 = st.columns([1, 2])
with f_col1:
    st.write("")
    st.write("")
    st.info(f"### Predicted Value:\n**₹ {forecast_val:,.2f} Cr**")
    st.markdown(f"""
    **Forecasting Metrics Applied:**
    * Historical Linear Delta Addition: `+₹ {avg_growth:,.2f} Cr`
    * Base Period Target Value: `₹ {latest_known_budget:,} Cr`
    """)

with f_col2:
    fig2 = px.bar(
        forecast_matrix, x="Year", y="Budget",
        title=f"Predictive Vector Pathway including 2027-2028 Forecast for {selected_dept}",
        color="Color_Status",
        color_discrete_map={"#10B981": "#10B981", "#EF4444": "#EF4444"}
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 6. Deep Work AI Analytical Insights Module
st.subheader(f"🤖 In-Depth AI Evaluation Suite: {selected_dept}")

last_year_val = dept_all_years_df.iloc[-2]["Budget"]
latest_year_val = dept_all_years_df.iloc[-1]["Budget"]
yoy_change = latest_year_val - last_year_val
pct_change = (yoy_change / last_year_val) * 100

# Base parameters for conditional logic based on total vs independent sector selections
is_total = selected_dept == "TOTAL (All 13 Sectors)"

st.markdown(f"### 📑 Deep Fiscal Profile Report for the **{selected_dept}** Track")

# Structural Pros and Cons narrative generator blocks
if yoy_change >= 0:
    st.markdown(f"#### 🟢 Structural Plus Points (Fiscal Strengths Analysis)")
    st.markdown(f"""
    * **Capital Injection Momentum:** The current financial trajectory reflects an increase of **₹ {yoy_change:,} Cr** (+{pct_change:.2f}%), indicating strong macro-economic backing.
    * **Long-Term Resource Security:** Continued baseline increases allow active long-range project planning and mitigate structural project delays.
    * **Stabilized Expansion Velocity:** The average annual scaling increment of **₹ {avg_growth:,.2f} Cr** suggests a reliable and structured funding path rather than an unstable, volatile spike.
    """)
    
    st.markdown(f"#### 🔴 Structural Minus Points (Fiscal Vulnerability Analysis)")
    st.markdown(f"""
    * **Inflation Vulnerability Risk:** While a nominal increase of **{pct_change:.2f}%** is present, if the real-world operational cost inflation moves faster than this growth rate, purchasing power could fall.
    * **Distribution Asymmetry Risk:** Broad overall scaling could mask inner-department bottlenecks where critical localized sub-tracks remain underfunded.
    """)
else:
    st.markdown(f"#### 🟢 Structural Plus Points (Fiscal Consolidation Analysis)")
    st.markdown(f"""
    * **Fiscal Consolidation Drive:** The contraction of **₹ {abs(yoy_change):,} Cr** ({pct_change:.2f}%) indicates a targeted structural effort to eliminate systemic wastage and streamline operations.
    * **Strategic Realignment:** Lower direct capital outlays provide space to shift toward tech-driven, asset-light efficiency measures.
    """)
    
    st.markdown(f"#### 🔴 Structural Minus Points (Fiscal Bottleneck Risks)")
    st.markdown(f"""
    * **Operational Strains:** A negative reduction vector limits development velocity, risking project delays across critical long-term targets.
    * **Liquidity Tightening:** Reduced capital margins restrict quick response capabilities for sudden market adjustments or emergency financial demands.
    """)

# Departmental Component Breakdown Sub-Module
st.markdown("#### 🔍 Structural Component Decomposition Breakdown")
if is_total:
    st.markdown("""
    When evaluating the composite **Total Union Budget Matrix**, individual tracking vectors show diverse operational pathways:
    * **Primary Capital Drivers (+):** Sectors like *Infrastructure & Roads*, *Railways*, and *Defence* maintain consistently positive change vectors, absorbing the majority of central liquidity injections.
    * **Social Safety Balances (Stabilizers):** Fields like *Education* and *Health & Family Welfare* move on long-term gradual increments, avoiding sudden volatility spikes.
    * **Volatile Tracks (Variable Scaling):** *Consumer Affairs, Food & Public Distribution* shows non-linear adjustments reflecting changing market variables and subsidy reallocations.
    """)
else:
    st.markdown(f"""
    Breaking down the standalone matrix for **{selected_dept}**:
    * **Core Baseline Components:** This specific track shows a foundational growth floor anchored at a historic minimum of **₹ {min_budget:,} Cr** (2017) and peaking dynamically at **₹ {max_budget:,} Cr**.
    * **Volatility Vector:** The variance checks across its 11-year timeline show that funding shifts match national economic transitions, maintaining an average structural momentum of **₹ {avg_growth:,.2f} Cr** per year heading directly into the 2028 prediction block.
    """)
