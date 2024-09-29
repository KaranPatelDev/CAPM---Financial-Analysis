import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Economic Indicators Dashboard",
    page_icon="📊",  # Icon for economic indicators
    layout="wide"
)

st.title("📊 Economic Indicators Dashboard")
st.subheader("Track and Analyze Key Economic Indicators Affecting Financial Markets")

# Define a list of economic indicators
indicators = {
    'GDP': 'Gross Domestic Product',
    'CPI': 'Consumer Price Index',
    'Unemployment Rate': 'Unemployment Rate',
    'Interest Rates': 'Federal Funds Rate',
    'PPI': 'Producer Price Index'
}

# User selects indicators to analyze
selected_indicators = st.multiselect("Choose Economic Indicators to Analyze", options=list(indicators.keys()), default=['GDP', 'CPI'])

# Date range for data retrieval
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

# Initialize an empty DataFrame for indicators
indicator_data = pd.DataFrame()

# Download and display selected indicators
for indicator in selected_indicators:
    if indicator == 'GDP':
        data = web.DataReader('GDP', 'fred', start_date, end_date)
    elif indicator == 'CPI':
        data = web.DataReader('CPIAUCNS', 'fred', start_date, end_date)  # Consumer Price Index
    elif indicator == 'Unemployment Rate':
        data = web.DataReader('UNRATE', 'fred', start_date, end_date)
    elif indicator == 'Interest Rates':
        data = web.DataReader('FEDFUNDS', 'fred', start_date, end_date)
    elif indicator == 'PPI':
        data = web.DataReader('PPIACO', 'fred', start_date, end_date)  # Producer Price Index
    
    # Rename columns for clarity
    data.rename(columns={data.columns[0]: indicators[indicator]}, inplace=True)
    indicator_data = pd.concat([indicator_data, data], axis=1)

# Plotting the data
if not indicator_data.empty:
    st.line_chart(indicator_data)
    st.markdown("### Indicator Data")
    st.dataframe(indicator_data)

    # Optional: Show summary statistics
    st.markdown("### Summary Statistics")
    st.write(indicator_data.describe())
else:
    st.write("Please select valid economic indicators and dates.")

