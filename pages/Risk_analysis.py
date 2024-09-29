import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import capm_functions  # Ensure you have this module for your calculations

# Set page configurations
st.set_page_config(page_title="Comprehensive Risk Analysis",
                   page_icon="⚖️",
                   layout="wide")

# Page title and subtitle
st.warning("⚠️ This web page is under maintenance")
st.title("⚖️ Comprehensive Risk Analysis for Stock Investments")
st.subheader("Evaluate Key Risk Metrics: Beta, Volatility, Value at Risk (VaR), Sharpe Ratio, and Correlation with Market")

# User inputs for stock selection and analysis period
col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect(
        "Select stocks to analyze",
        ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'],
        default=['TSLA', 'AAPL', 'AMZN', 'GOOGL']
    )
with col2:
    year = st.number_input('Select number of years for analysis', min_value=1, max_value=10, value=5)

# Define date range for stock data retrieval
end_date = datetime.date.today()
start_date = datetime.date(end_date.year - year, end_date.month, end_date.day)

# Initialize DataFrame to store stock data
stocks_df = pd.DataFrame()

# Try downloading stock price data for selected stocks using yfinance
try:
    for stock in stocks_list:
        stock_data = yf.download(stock, start=start_date, end=end_date)
        stocks_df[f'{stock}'] = stock_data['Close']

    # Download data for SP500 using yfinance
    sp500_data = yf.download('^GSPC', start=start_date, end=end_date)
    stocks_df['SP500'] = sp500_data['Close']

    # Reset index to ensure 'Date' is included
    stocks_df.reset_index(inplace=True)

except Exception as e:
    st.error(f"An error occurred during analysis: {e}")

# Check if stocks_df contains data and then calculate daily returns
if not stocks_df.empty:
    try:
        # Calculate daily returns
        stocks_daily_return = capm_functions.daily_returns(stocks_df)

        # Ensure SP500 data exists in daily returns
        if 'SP500' not in stocks_daily_return.columns:
            st.error("SP500 data is missing from daily returns calculation.")
        else:
            # Containers for risk metrics
            beta = {}
            volatility = {}
            VaR = {}
            sharpe_ratios = {}
            correlation_with_market = {}
            risk_free_rate = 0.01  # Assuming 1% annual risk-free rate for Sharpe Ratio

            # Calculating Beta, Volatility, VaR, and Sharpe Ratio
            for stock in stocks_list:
                try:
                    # 1. Beta Calculation
                    b, _ = capm_functions.calculate_beta(stocks_daily_return, stock)
                    beta[stock] = b

                    # 2. Volatility (Standard Deviation)
                    volatility[stock] = np.std(stocks_daily_return[stock]) * np.sqrt(252)  # Annualized volatility

                    # 3. Value at Risk (VaR) at 95% confidence
                    VaR[stock] = np.percentile(stocks_daily_return[stock], 5) * np.sqrt(252)  # 5th percentile

                    # 4. Sharpe Ratio
                    stock_return = stocks_daily_return[stock].mean() * 252  # Annualized return
                    sharpe_ratios[stock] = (stock_return - risk_free_rate) / volatility[stock]  # Risk-adjusted return

                    # 5. Correlation with the market (SP500)
                    correlation_with_market[stock] = stocks_daily_return[stock].corr(stocks_daily_return['SP500'])

                except Exception as e:
                    st.error(f"Error calculating metrics for {stock}: {e}")

            # Display risk metrics in Streamlit
            col1, col2, col3 = st.columns(3)

            # Beta Values
            with col1:
                st.markdown("### Beta Values (Market Risk Sensitivity)")
                beta_df = pd.DataFrame({'Stock': beta.keys(), 'Beta': [round(b, 2) for b in beta.values()]})
                st.dataframe(beta_df, use_container_width=True)
                st.info("**Beta** measures the stock's sensitivity to market movements. A Beta > 1 means the stock is more volatile than the market.")

            # Volatility (Standard Deviation)
            with col2:
                st.markdown("### Annualized Volatility (Standard Deviation)")
                vol_df = pd.DataFrame({'Stock': volatility.keys(), 'Volatility': [round(v, 2) for v in volatility.values()]})
                st.dataframe(vol_df, use_container_width=True)
                st.info("**Volatility** indicates the stock's price fluctuations. Higher values mean greater risk.")

            # VaR (Value at Risk)
            with col3:
                st.markdown("### Value at Risk (VaR) at 95% Confidence")
                var_df = pd.DataFrame({'Stock': VaR.keys(), 'VaR': [round(v, 2) for v in VaR.values()]})
                st.dataframe(var_df, use_container_width=True)
                st.info("**VaR** is the maximum expected loss in a day, with 95% confidence, based on historical data.")

            # Sharpe Ratios
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Sharpe Ratios (Risk-Adjusted Return)")
                sharpe_df = pd.DataFrame({'Stock': sharpe_ratios.keys(), 'Sharpe Ratio': [round(sr, 2) for sr in sharpe_ratios.values()]})
                st.dataframe(sharpe_df, use_container_width=True)
                st.info("**Sharpe Ratio** measures risk-adjusted returns. A higher ratio indicates better risk-adjusted performance.")

            # Correlation with Market
            with col2:
                st.markdown("### Correlation with SP500")
                corr_df = pd.DataFrame({'Stock': correlation_with_market.keys(), 'Correlation': [round(corr, 2) for corr in correlation_with_market.values()]})
                st.dataframe(corr_df, use_container_width=True)
                st.info("**Correlation** shows how closely the stock's returns follow the SP500. A value near 1 indicates strong positive correlation.")
    except Exception as e:
        st.error(f"An error occurred during daily returns calculation: {e}")
else:
    st.error("No stock data retrieved. Please check the selected stocks.")
