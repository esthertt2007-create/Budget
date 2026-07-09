import streamlit as st
import pandas as pd
import numpy as np

# 1. Setup Page Configuration
st.set_page_config(page_title="Department Budget Analytics", layout="wide")
st.title("📊 Departmental Budget Dashboard & Forecasting")
st.markdown("---")

# 2. Mock Data Generation (including 2024, 2025, 2025-2026, 2026-2027)
@st.cache_data
def load_budget_data():
    data = {
        "Department": [
            "Rural Development", "Rural Development", "Rural Development", "Rural Development",
            "Agriculture & Farmers Welfare", "Agriculture & Farmers Welfare", "Agriculture & Farmers Welfare", "Agriculture & Farmers Welfare",
            "Education", "Education", "Education", "Education",
            "Health & Family Welfare", "Health & Family Welfare", "Health & Family Welfare", "Health & Family Welfare",
            "Infrastructure & Roads", "Infrastructure & Roads", "Infrastructure & Roads", "Infrastructure & Roads"
        ],
        "Year": [
            "2024", "2025", "2025-2026", "2026-2027",
            "2024", "2025", "2025-2026", "2026-2027",
            "2024", "2025", "2025-2026", "2026-2027",
            "2024", "2025", "2025-2026", "2026-2027",
            "2024", "2025", "2025-2026", "2026-2027"
        ],
        # Budget values in Crores (INR)
        "Budget": [
            157000, 165000, 177000, 192000,  # Rural Dev
            115000, 118000, 125000, 132000,  # Agri
            92000,  98000,  105000, 112000,  # Edu
            86000,  89000,  94000,  101000,  # Health
            165000, 175000, 195000, 210000   # Infra
        ]
    }
    return pd.DataFrame(data)

df = load_budget_data()

# 3. Sidebar Filters (Requirements a & b)
st.sidebar.header("Filter Options")

# Dropdown for Departments
departments = df["Department"].unique()
selected_dept = st.sidebar.selectbox("Select Department", departments)

# Dropdown for Years
years = df["Year"].unique()
selected_year = st.sidebar.selectbox("Select Year", years)

# Filter data based on selections
filtered_df = df[(df["Department"] == selected_dept) & (df["Year"] == selected_year)]
dept_all_years_df = df[df["Department"] == selected_dept]

# 4. Main Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    ### Requirement c: Bar Chart Representation
    st.subheader(f"📈 Budget Overview for {selected_dept}")
    
    # We display a bar chart across all historical years for visual trend analysis
    st.bar_chart(data=dept_all_years_df, x="Year", y="Budget", use_container_width=True)

with col2:
    ### Requirement d: Statistical Insights
    st.subheader("📋 Statistical Insights (All Years)")
    
    max_budget = dept_all_years_df["Budget"].max()
    min_budget = dept_all_years_df["Budget"].min()
    avg_budget = dept_all_years_df["Budget"].mean()
    current_selection_budget = filtered_df["Budget"].values[0] if not filtered_df.empty else 0
    
    st.metric(label=f"Selected Year Budget ({selected_year})", value=f"₹ {current_selection_budget:,} Cr")
    st.metric(label="Maximum Budget Over Years", value=f"₹ {max_budget:,} Cr")
    st.metric(label="Minimum Budget Over Years", value=f"₹ {min_budget:,} Cr")
    st.metric(label="Average Budget", value=f"₹ {avg_budget:,.2f} Cr")

st.markdown("---")

# 5. Requirement e & f: AI Insights (No API) & 2027-2028 Forecasting
st.subheader("🤖 Rule-Based AI Insights & Predictive Forecasting")

# Calculate trends for the AI Insights
years_list = list(years)
if len(dept_all_years_df) >= 2:
    # Sort by sequence of time
    sorted_dept_df = dept_all_years_df.copy()
    # map years to chronological index for trend calculation
    year_order = {"2024": 0, "2025": 1, "2025-2026": 2, "2026-2027": 3}
    sorted_dept_df["Order"] = sorted_dept_df["Year"].map(year_order)
    sorted_dept_df = sorted_dept_df.sort_values("Order").reset_index(drop=True)
    
    # Check latest direction (from 2025-2026 to 2026-2027)
    last_year_budget = sorted_dept_df.iloc[-2]["Budget"]
    latest_year_budget = sorted_dept_df.iloc[-1]["Budget"]
    pct_change = ((latest_year_budget - last_year_budget) / last_year_budget) * 100
    
    # Generate Rule-Based Insights
    if pct_change > 0:
        insight_text = f"The budget for **{selected_dept}** has **increased** by **{pct_change:.2f}%** moving into the 2026-2027 cycle compared to the previous period."
        alert_type = st.success
    elif pct_change < 0:
        insight_text = f"The budget for **{selected_dept}** has **decreased** by **{abs(pct_change):.2f}%** moving into the 2026-2027 cycle compared to the previous period."
        alert_type = st.warning
    else:
        insight_text = f"The budget for **{selected_dept}** remained **stable** moving into the 2026-2027 cycle."
        alert_type = st.info
        
    st.markdown("### 💡 AI Insights")
    alert_type(insight_text)

    # Simple Linear/Trend Forecast for 2027-2028 (Requirement f)
    # Calculate average absolute growth per period to project next year
    growth_rates = sorted_dept_df["Budget"].diff().dropna()
    avg_growth = growth_rates.mean()
    
    forecast_2027_2028 = latest_year_budget + avg_growth
    
    st.markdown("### 🔮 Next Year Budget Forecast")
    st.info(f"Predicted Budget for **2027-2028**: **₹ {forecast_2027_2028:,.2f} Cr** (Based on an historical average growth pattern of ₹ {avg_growth:,.2f} Cr per cycle).")

else:
    st.error("Insufficient timeline data to generate AI insights or run a predictive forecast.")
