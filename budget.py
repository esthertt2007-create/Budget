import streamlit as st
import pandas as pd
import numpy as np

# 1. Setup Page Configuration
st.set_page_config(page_title="Union Budget Analytics (13 Sectors)", layout="wide")
st.title("📊 Departmental Budget Dashboard & Forecasting")
st.markdown("---")

# 2. Comprehensive Dataset (13 Sectors from 2017 to 2026-2027)
@st.cache_data
def load_budget_data():
    data = {
        "Department": [],
        "Year": [],
        "Budget": []
    }
    
    # Timeline list from 2017 to 2026-2027
    years_timeline = [
        "2017", "2018", "2019", "2020", "2021", "2022", "2023", 
        "2024", "2025", "2025-2026", "2026-2027"
    ]
    
    # 13 Core Sectors of the Union Budget (Scaled in Crores INR)
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
    
    for dept in baselines.keys():
        data["Department"].extend([dept] * len(years_timeline))
        data["Year"].extend(years_timeline)
        data["Budget"].extend(baselines[dept])
        
    return pd.DataFrame(data)

df = load_budget_data()

# 3. Sidebar Filters (Far Left Layout)
st.sidebar.header("Filter Options")
departments = df["Department"].unique()
selected_dept = st.sidebar.selectbox("Select Sector / Department", departments)

years = df["Year"].unique()
selected_year = st.sidebar.selectbox("Select Year", years)

# Filter sequences
filtered_df = df[(df["Department"] == selected_dept) & (df["Year"] == selected_year)]
dept_all_years_df = df[df["Department"] == selected_dept].reset_index(drop=True)

# 4. Main Dashboard Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📈 Budget Overview: {selected_dept} (2017 - 2027)")
    st.bar_chart(data=dept_all_years_df, x="Year", y="Budget", use_container_width=True)

with col2:
    st.subheader("📋 Statistical Insights")
    
    max_budget = dept_all_years_df["Budget"].max()
    min_budget = dept_all_years_df["Budget"].min()
    avg_budget = dept_all_years_df["Budget"].mean()
    current_selection_budget = filtered_df["Budget"].values[0] if not filtered_df.empty else 0
    
    st.metric(label=f"Selected Year Budget ({selected_year})", value=f"₹ {current_selection_budget:,} Cr")
    st.metric(label="Maximum Budget (2017-2027)", value=f"₹ {max_budget:,} Cr")
    st.metric(label="Minimum Budget (2017-2027)", value=f"₹ {min_budget:,} Cr")
    st.metric(label="Average Budget Allocation", value=f"₹ {avg_budget:,.2f} Cr")

st.markdown("---")

# 5. Rule-Based AI Insights & 2027-2028 Forecasting
st.subheader("🤖 Rule-Based AI Insights & Predictive Forecasting")

if len(dept_all_years_df) >= 2:
    # 2026-2027 evaluation against previous period
    last_year_budget = dept_all_years_df.iloc[-2]["Budget"]
    latest_year_budget = dept_all_years_df.iloc[-1]["Budget"]
    pct_change = ((latest_year_budget - last_year_budget) / last_year_budget) * 100
    
    st.markdown("### 💡 AI Insights")
    if pct_change > 0:
        st.success(f"The budget for **{selected_dept}** has **increased** by **{pct_change:.2f}%** in the 2026-2027 cycle compared to the previous fiscal year.")
    elif pct_change < 0:
        st.warning(f"The budget for **{selected_dept}** has **decreased** by **{abs(pct_change):.2f}%** in the 2026-2027 cycle compared to the previous fiscal year.")
    else:
        st.info(f"The budget for **{selected_dept}** remained flat entering the 2026-2027 cycle.")

    # 2027-2028 Predictive Forecast Model
    growth_rates = dept_all_years_df["Budget"].diff().dropna()
    avg_growth = growth_rates.mean()
    
    forecast_2027_2028 = latest_year_budget + avg_growth
    
    st.markdown("### 🔮 Next Year Budget Forecast")
    st.info(f"Predicted Budget for **2027-2028**: **₹ {forecast_2027_2028:,.2f} Cr** (Based on historical average trajectory of +₹ {avg_growth:,.2f} Cr per cycle).")
else:
    st.error("Error drawing parameters from your dataset layout timeline.")
