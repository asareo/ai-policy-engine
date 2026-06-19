import streamlit as st
import pandas as pd

def load_regulatory_dataset():
    """
    Constructs an expanded tracking matrix mapping global AI policy indicators,
    capturing regulatory strictness caps and sovereign enactment timelines.
    """
    policy_data = {
        "Region": ["United States", "European Union", "United Kingdom", "China", "Canada", "Singapore", "Ghana"],
        "Framework_Name": ["Executive Order 14110", "EU AI Act", "Pro-Innovation Approach", "Generative AI Measures", "Artificial Intelligence & Data Act", "Model Governance Framework", "Digital Economy Policy"],
        "Restriction_Score": [6.5, 9.5, 4.0, 8.5, 7.0, 5.0, 3.5],
        "Enforcement_Level": ["Moderate", "Critical", "Low", "Strict", "High", "Moderate", "Low"],
        "Enactment_Year": [2024, 2024, 2025, 2023, 2025, 2024, 2026],
        "Oversight_Count": [4, 12, 2, 9, 6, 3, 1]
    }
    return pd.DataFrame(policy_data)

st.set_page_config(page_title="Global AI Regulatory Diffusion Tracker", layout="wide")

st.title("Global AI Regulatory Diffusion Tracker")
st.markdown("This analytical interface maps international regulatory convergence, drift patterns, and calculated strictness velocity metrics across global jurisdictions.")

st.divider()

df_policy = load_regulatory_dataset()

# --- PHASE 3: COMPUTATIONAL COMPLEXITY LAYER ---
st.sidebar.header("Simulation Control Panel")
st.sidebar.markdown("Adjust macro variables to project global compliance drift behavior thresholds.")

# 1. Slider: Simulates a global regulatory tightening event (e.g., sudden international treaty enforcement)
strictness_multiplier = st.sidebar.slider(
    "Global Strictness Acceleration Multiplier",
    min_value=1.0,
    max_value=2.0,
    value=1.0,
    step=0.1
)

# Apply the simulated multiplier variable dynamically across dataframe columns
df_policy["Projected_Restriction_Score"] = (df_policy["Restriction_Score"] * strictness_multiplier).clip(upper=10.0)

# 2. Algorithmic Velocity Calculation: Measures regulatory acceleration rate
# Formula: Oversight boards established per year elapsed since a baseline anchor year (2022)
df_policy["Regulatory_Velocity"] = df_policy["Oversight_Count"] / (df_policy["Enactment_Year"] - 2022 + 1)

# Calculate Strictness Z-Score
mean_restriction = df_policy["Restriction_Score"].mean()
std_restriction = df_policy["Restriction_Score"].std()
df_policy["Strictness_Z_Score"] = (df_policy["Restriction_Score"] - mean_restriction) / std_restriction

# Display the updated dataframe with statistical columns
st.subheader("Regulatory Data with Statistical Metrics")
st.dataframe(
    df_policy.style.format({
        "Restriction_Score": "{:.1f}",
        "Projected_Restriction_Score": "{:.1f}",
        "Regulatory_Velocity": "{:.2f}",
        "Strictness_Z_Score": "{:.2f}"
    }),
    use_container_width=True
)

# --- ANALYTICS DISPLAY INTERFACE ---
total_jurisdictions = len(df_policy)
average_strictness = df_policy["Projected_Restriction_Score"].mean()
highest_restriction = df_policy.loc[df_policy["Projected_Restriction_Score"].idxmax()]["Region"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Monitored Sovereign Jurisdictions", value=total_jurisdictions)
with col2:
    st.metric(label="Simulated Strictness Index Average", value=f"{average_strictness:.2f} / 10.0")
with col3:
    st.metric(label="Maximum Compliance Ceiling", value=highest_restriction)

st.divider()

left_chart_col, right_table_col = st.columns([3, 2])

with left_chart_col:
    st.subheader("Dynamic Cross-Border Restriction Projections")
    # Plot the simulated projected column against baseline values to show delta trends
    chart_df = df_policy.set_index("Region")[["Restriction_Score", "Projected_Restriction_Score"]]
    st.bar_chart(chart_df)

with right_table_col:
    st.subheader("Calculated Regulatory Velocity Index")
    # Isolate our engineered acceleration tracking variables
    velocity_grid = df_policy[["Region", "Enactment_Year", "Regulatory_Velocity", "Strictness_Z_Score"]].sort_values(by="Regulatory_Velocity", ascending=False)
    st.dataframe(
        velocity_grid.style.format({
            "Regulatory_Velocity": "{:.2f}",
            "Strictness_Z_Score": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.subheader("Master Policy Tracking Log (With Simulated Vectors)")
st.dataframe(
    df_policy.style.format({
        "Restriction_Score": "{:.1f}",
        "Projected_Restriction_Score": "{:.1f}",
        "Regulatory_Velocity": "{:.2f}",
        "Strictness_Z_Score": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)