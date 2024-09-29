import streamlit as st
import pandas as pd
import yfinance as yf

# Set up the page configuration
st.set_page_config(
    page_title="Financial Ratios Dashboard",
    page_icon="💰",
    layout="wide"
)
# st.error("🚨 This web page is under maintenance")
st.title("💰 Financial Ratios Analysis")

# User input for stock selection
stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, GOOGL):", "AAPL").upper()

# Button to fetch data
if st.button("Get Financial Ratios"):
    # Fetch stock data from Yahoo Finance
    try:
        stock = yf.Ticker(stock_symbol)

        # Fetch relevant financial data
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        info = stock.info  # Use info instead of key_metrics

        # Calculate key financial ratios
        try:
            # P/E Ratio
            pe_ratio = info.get('trailingPE', None)

            # Debt-to-Equity Ratio
            total_debt = balance_sheet.loc['Total Debt'][0] if 'Total Debt' in balance_sheet.index else 0
            total_equity = balance_sheet.loc['Total Stockholder Equity'][0] if 'Total Stockholder Equity' in balance_sheet.index else 1  # Avoid division by zero
            debt_to_equity = total_debt / total_equity

            # Return on Equity (ROE)
            net_income = financials.loc['Net Income'][0] if 'Net Income' in financials.index else 0
            roe = net_income / total_equity

            # Current Ratio
            current_assets = balance_sheet.loc['Total Current Assets'][0] if 'Total Current Assets' in balance_sheet.index else 1  # Avoid division by zero
            current_liabilities = balance_sheet.loc['Total Current Liabilities'][0] if 'Total Current Liabilities' in balance_sheet.index else 1
            current_ratio = current_assets / current_liabilities

            # Return on Assets (ROA)
            total_assets = balance_sheet.loc['Total Assets'][0] if 'Total Assets' in balance_sheet.index else 1
            roa = net_income / total_assets

            # Create a DataFrame for displaying results
            ratios_data = {
                "Ratio": ["P/E Ratio", "Debt-to-Equity Ratio", "Return on Equity (ROE)", "Current Ratio", "Return on Assets (ROA)"],
                "Value": [
                    pe_ratio,
                    debt_to_equity,
                    roe,
                    current_ratio,
                    roa
                ]
            }
            ratios_df = pd.DataFrame(ratios_data)

            # Display financial ratios
            st.subheader(f"Financial Ratios for {stock_symbol}")
            st.write("### Key Financial Ratios")
            st.dataframe(ratios_df, use_container_width=True)

        except Exception as ratio_error:
            st.error(f"Error calculating financial ratios: {ratio_error}")

    except Exception as e:
        st.error(f"Error fetching data for {stock_symbol}: {e}")

# Additional information and explanation
st.markdown(""" 
### Explanation of Financial Ratios:
- **P/E Ratio**: Measures the price investors are willing to pay for a dollar of earnings. A high P/E indicates high growth expectations.
- **Debt-to-Equity Ratio**: Indicates the relative proportion of shareholders' equity and debt used to finance a company's assets. A lower ratio suggests less risk.
- **Return on Equity (ROE)**: Measures profitability by revealing how much profit a company generates with the money shareholders have invested.
- **Current Ratio**: Indicates a company's ability to pay short-term obligations. A ratio above 1 means the company can cover its short-term liabilities.
- **Return on Assets (ROA)**: Indicates how efficient management is at using its assets to generate earnings. A higher ROA indicates better asset efficiency.
""")
