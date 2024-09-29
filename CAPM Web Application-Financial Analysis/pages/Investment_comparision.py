import streamlit as st
import pandas as pd
import yfinance as yf

# Page Configuration
st.set_page_config(
    page_title="Investment Comparison",
    page_icon="💰",
    layout="wide"
)

st.title("Investment Comparison Dashboard")
st.subheader("Compare Different Investment Options Side-by-Side")

# Getting user input for stocks
investment_options = st.multiselect(
    "Select Investment Options:",
    options=['AAPL', 'AMZN', 'GOOGL', 'TSLA', 'MSFT', 'NFLX'],
    default=['AAPL', 'AMZN']
)

# Define a function to get stock data
def get_stock_data(tickers):
    stock_data = {}
    for ticker in tickers:
        data = yf.download(ticker, period="1y")  # Get 1 year of data
        dividends = data['Dividends'].sum() if 'Dividends' in data.columns else 0  # Check for dividends
        stock_data[ticker] = {
            'Close': data['Close'],
            'Dividend': dividends  # Total dividends over the period
        }
    return stock_data

# Display the selected investment options
if investment_options:
    stock_data = get_stock_data(investment_options)

    # Create a DataFrame for comparison
    comparison_df = pd.DataFrame({
        'Investment Option': investment_options,
        'Total Dividends': [stock_data[ticker]['Dividend'] for ticker in investment_options],
        'Latest Price': [stock_data[ticker]['Close'].iloc[-1] for ticker in investment_options],
    })

    # Calculate ROI (Return on Investment) assuming an investment of $1000
    comparison_df['ROI (%)'] = (comparison_df['Total Dividends'] / 1000) * 100  # as percentage

    # Display the comparison DataFrame
    st.markdown("### Investment Comparison Table")
    st.dataframe(comparison_df)

    # Plotting investment performance
    st.markdown("### Price Performance Over the Last Year")
    
    # Create a combined DataFrame for line chart
    combined_df = pd.DataFrame({ticker: stock_data[ticker]['Close'] for ticker in investment_options})

    # Display line chart
    st.line_chart(combined_df, use_container_width=True)

else:
    st.warning("Please select at least one investment option to compare.")

# Additional Enhancements
st.markdown("---")
st.markdown("### Insights:")
st.markdown(
    "This dashboard allows you to compare different stocks based on their dividends and price performance over the last year. "
    "You can select multiple stocks to view their comparative performance."
)
