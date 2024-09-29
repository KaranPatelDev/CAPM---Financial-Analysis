import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

# Set up the page configuration
st.set_page_config(
    page_title="Dividend Analysis",
    page_icon="💰",  # Icon representing dividends
    layout="wide"
)

# Title and description
st.title("💰 Dividend Analysis")
st.subheader("Evaluate the Dividend History and Yield of Stocks")

# Getting user input
stocks_list = st.multiselect(
    "Choose stocks to analyze dividends:",
    ('AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOGL', 'JNJ', 'PG', 'VZ', 'KO', 'PFE'),
    ['AAPL', 'MSFT']
)

# Function to fetch dividend history and yield
def fetch_dividend_data(stock):
    try:
        stock_data = yf.Ticker(stock)
        dividends = stock_data.dividends
        return dividends
    except Exception as e:
        st.error(f"Error fetching data for {stock}: {e}")
        return None

# Store dividend data
dividend_data = {}

for stock in stocks_list:
    dividends = fetch_dividend_data(stock)
    if dividends is not None:
        dividend_data[stock] = dividends

# Create a DataFrame to display
if dividend_data:
    dividend_df = pd.DataFrame.from_dict(dividend_data, orient='index').transpose()
    
    # Calculate dividend yield
    for stock in stocks_list:
        if stock in dividend_data:
            latest_dividend = dividend_data[stock].iloc[-1] if not dividend_data[stock].empty else 0
            current_price = yf.Ticker(stock).info['currentPrice']
            dividend_yield = (latest_dividend / current_price) * 100 if current_price > 0 else 0
            dividend_df[f"{stock} Yield (%)"] = dividend_yield
            
    # Display dividend data
    st.markdown("### Dividend History")
    st.dataframe(dividend_df, use_container_width=True)

    # Plotting dividend history for visualization
    if dividend_df.notnull().any().any():
        st.markdown("### Dividend History Plot")
        st.line_chart(dividend_df)

    # Displaying additional information
    st.markdown("### Summary of Dividends and Yield")
    for stock in stocks_list:
        if stock in dividend_data:
            st.markdown(f"**{stock}**: Latest Dividend: ${latest_dividend:.2f}, Yield: {dividend_yield:.2f}%")

else:
    st.warning("Please select stocks to analyze dividends.")
