import streamlit as st
import pandas as pd
import datetime

def load_regulatory_dataset():
    """
    Constructs a baseline statistical matrix mapping global AI policy indices,
    tracking variables like regional restriction scores and enforcement timelines.
    """
    # Create structured historical data observations from 2024 to 2026
    policy_data = {
        "Region": ["United States", "European Union", "United Kingdom", "China", "Canada", "Singapore", "Ghana"],
        "Framework_Name": ["Executive Order 14110", "EU AI Act", "Pro-Innovation Approach", "Generative AI Measures", "Artificial Intelligence & Data Act", "Model Governance Framework", "Digital Economy Policy"],
        "Restriction_Score": [6.5, 9.5, 4.0, 8.5, 7.0, 5.0, 3.5],
        "Enforcement_Level": ["Moderate", "Critical", "Low", "Strict", "High", "Moderate", "Low"],
        "Enactment_Year": [2024, 2024, 2025, 2023, 2025, 2024, 2026],
        "Oversight_Count": [4, 12, 2, 9, 6, 3, 1]
    }
    return pd.DataFrame(policy_data)

# --- STREAMLIT ANALYTICS LAYOUT ---
st.set_page_config(page_title="Global AI Regulatory Diffusion Tracker", layout="wide")

st.title("Global AI Regulatory Diffusion Tracker")
st.markdown("This analytical interface maps international regulatory convergence, drift patterns, and compliance strictness distributions across global jurisdictions.")

st.divider()

# Load the target dataset
df_policy = load_regulatory_dataset()

# 1. Macro Summary Metric Calculations
total_jurisdictions = len(df_policy)
average_strictness = df_policy["Restriction_Score"].mean()
highest_restriction = df_policy.loc[df_policy["Restriction_Score"].idxmax()]["Region"]

# Display statistical KPI indicators side-by-side
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Monitored Sovereign Jurisdictions", value=total_jurisdictions)
with col2:
    st.metric(label="Global Strictness Index Average", value=f"{average_strictness:.2f} / 10.0")
with col3:
    st.metric(label="Maximum Compliance Ceiling", value=highest_restriction)

st.divider()

# 2. Dynamic Filtration Control
st.subheader("Interactive Cohort Filtering")
selected_enforcement = st.multiselect(
    "Filter Analysis Matrix by Enforcement Strictness Tier",
    options=df_policy["Enforcement_Level"].unique(),
    default=df_policy["Enforcement_Level"].unique()
)

# Apply runtime filtration to our memory vectors
df_filtered = df_policy[df_policy["Enforcement_Level"].isin(selected_enforcement)]

# 3. Structural Data Layout Splits
left_chart_col, right_table_col = st.columns([3, 2])

with left_chart_col:
    st.subheader("Regional Restriction Score Matrix")
    if not df_filtered.empty:
        # Create a clean cross-sectional bar chart mapping regulatory weight
        chart_matrix = df_filtered.set_index("Region")["Restriction_Score"]
        st.bar_chart(chart_matrix)
    else:
        st.info("No records match the current enforcement level configuration.")

with right_table_col:
    st.subheader("Legislative Timeline Metrics")
    if not df_filtered.empty:
        # Render a focused grid isolating timelines and tracking variables
        timeline_grid = df_filtered[["Region", "Enactment_Year", "Oversight_Count"]].sort_values(by="Enactment_Year")
        st.dataframe(timeline_grid, use_container_width=True, hide_index=True)
    else:
        st.info("No timeline matrix profiles available.")

st.divider()

# 4. Master Analytics Grid Log
st.subheader("Master Policy Tracking Log")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)