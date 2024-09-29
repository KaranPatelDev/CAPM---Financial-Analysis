import streamlit as st
import pandas as pd
import numpy as np

# Set up the page title and layout
st.set_page_config(
    page_title="Scenario Analysis",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Scenario Analysis")
st.subheader("Simulate different financial scenarios")

# Getting user input for investment parameters
st.markdown("### Enter Investment Parameters")

initial_investment = st.number_input("Initial Investment ($)", value=10000, min_value=0)
years = st.number_input("Number of Years", value=5, min_value=1)

# Create scenarios
st.subheader("Create Scenarios")
scenario_names = st.text_input("Scenario Names (comma-separated, e.g., 'Optimistic, Pessimistic, Realistic')", "Optimistic, Realistic, Pessimistic")
scenarios = [name.strip() for name in scenario_names.split(',')] if scenario_names else []

# Rate of return adjustments for scenarios
st.markdown("### Set Rates of Return for Each Scenario")
rates_of_return = {}
for scenario in scenarios:
    rate = st.number_input(f"Rate of Return for {scenario} (%)", value=5.0, min_value=-100.0, max_value=100.0)
    rates_of_return[scenario] = rate / 100

# Calculate future values for each scenario
future_values = {}
for name in scenarios:
    future_value = initial_investment * (1 + rates_of_return[name]) ** years
    future_values[name] = future_value

# Display results
st.markdown("### Future Value Results")
result_df = pd.DataFrame({
    'Scenario': scenarios,
    'Future Value ($)': [future_values[name] for name in scenarios]
})

st.dataframe(result_df)

# Visualization
st.markdown("### Future Value Visualization")
st.bar_chart(result_df.set_index('Scenario'))
