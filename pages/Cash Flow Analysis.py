import streamlit as st
import pandas as pd
import numpy as np

# Set up the page title and layout
st.set_page_config(
    page_title="Cash Flow Analysis",
    page_icon="💵",
    layout="wide"
)

st.title("💵 Cash Flow Analysis")
st.subheader("Analyze your company's cash flows")

# User input for cash flows
st.markdown("### Enter Cash Flow Data")

# User input for cash inflows
inflows = st.text_area("Cash Inflows (comma-separated, e.g., 5000, 7000, 6000):", "5000, 7000, 6000")
inflows = [float(i) for i in inflows.split(',')] if inflows else []

# User input for cash outflows
outflows = st.text_area("Cash Outflows (comma-separated, e.g., 3000, 4000, 2000):", "3000, 4000, 2000")
outflows = [float(i) for i in outflows.split(',')] if outflows else []

# Calculate net cash flow
net_cash_flow = sum(inflows) - sum(outflows)

# Display results
st.markdown("### Results")
st.write(f"**Total Cash Inflows:** ${sum(inflows):,.2f}")
st.write(f"**Total Cash Outflows:** ${sum(outflows):,.2f}")
st.write(f"**Net Cash Flow:** ${net_cash_flow:,.2f}")

# Financial health assessment
if net_cash_flow > 0:
    st.success("The company is in a good liquidity position!")
else:
    st.warning("The company may face liquidity issues. Consider reviewing cash management.")

# Cash Flow Forecasting
st.markdown("### Cash Flow Forecasting")
forecast_years = st.number_input("Number of Years to Forecast", min_value=1, max_value=10, value=3)
growth_rate = st.number_input("Expected Growth Rate for Inflows (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
outflow_growth_rate = st.number_input("Expected Growth Rate for Outflows (%)", min_value=0.0, max_value=100.0, value=3.0) / 100

forecast_inflows = [sum(inflows) * ((1 + growth_rate) ** year) for year in range(1, forecast_years + 1)]
forecast_outflows = [sum(outflows) * ((1 + outflow_growth_rate) ** year) for year in range(1, forecast_years + 1)]
forecast_net_cash_flow = [inflow - outflow for inflow, outflow in zip(forecast_inflows, forecast_outflows)]

# Display forecasting results
forecast_df = pd.DataFrame({
    'Year': range(1, forecast_years + 1),
    'Projected Inflows ($)': forecast_inflows,
    'Projected Outflows ($)': forecast_outflows,
    'Projected Net Cash Flow ($)': forecast_net_cash_flow
})

st.markdown("### Cash Flow Forecasting Results")
st.dataframe(forecast_df)

# Visualization
st.markdown("### Cash Flow Visualization")
cash_flow_data = pd.DataFrame({
    'Category': ['Inflows', 'Outflows', 'Net Cash Flow'],
    'Amount': [sum(inflows), sum(outflows), net_cash_flow]
})

st.bar_chart(cash_flow_data.set_index('Category'))

# Forecast Visualization
st.markdown("### Forecast Visualization")
st.line_chart(forecast_df.set_index('Year'))
