# import streamlit as st
# import pandas as pd
# import pandas_datareader.data as web
# import yfinance as yf
# import datetime
# import capm_functions  # Ensure you have the necessary functions in capm_functions.py

# # Configure the Streamlit page
# st.set_page_config(
#     page_title="Stock Expected Return Calculator",
#     page_icon="💹",  # Icon related to stock market
#     layout="wide"
# )

# # Title and description
# st.title("📊 Stock Expected Return Calculator")
# st.subheader("Calculate Expected Returns for Selected Stocks Using the CAPM Model")
# st.markdown("""
# This tool allows you to calculate the expected returns for selected stocks based on the **Capital Asset Pricing Model (CAPM)**.
# Choose your stocks and the number of years of historical data you would like to analyze.
# """)

# # Get user input for stock selection and time period
# col1, col2 = st.columns([1, 1])
# with col1:
#     # Allow users to select stocks from a predefined list
#     stocks_list = st.multiselect("Select up to 4 stocks", 
#                                  options=['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'],
#                                  default=['TSLA', 'AAPL', 'AMZN', 'GOOGL'])
# with col2:
#     # Input for the number of years of data to use for analysis
#     year = st.number_input('Select the number of years for historical data', 
#                            min_value=1, max_value=10, value=5)

# # Set the date range for fetching historical data
# end = datetime.date.today()
# start = datetime.date(end.year - year, end.month, end.day)

# # Exception handling to avoid app crashes due to bad inputs or connection issues
# try:
#     # Fetching S&P 500 data as a market benchmark for CAPM calculations
#     SP500 = web.DataReader('sp500', 'fred', start, end)

#     # Initialize an empty DataFrame to store stock prices
#     stocks_df = pd.DataFrame()

#     # Download stock data for each selected stock from Yahoo Finance
#     for stock in stocks_list:
#         st.write(f"Fetching data for {stock}...")
#         stock_data = yf.download(stock, start=start, end=end)
#         stocks_df[stock] = stock_data['Close']

#     # Reset the index and prepare to merge with S&P 500 data
#     stocks_df.reset_index(inplace=True)
#     SP500.reset_index(inplace=True)
#     SP500.columns = ['Date', 'sp500']

#     # Ensure the date columns are in datetime format for merging
#     stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
#     stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

#     # Display the data
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         st.markdown("### Stock Prices Data (First 5 Rows)")
#         st.dataframe(stocks_df.head(), use_container_width=True)
#     with col2:
#         st.markdown("### S&P 500 Data (First 5 Rows)")
#         st.dataframe(SP500.head(), use_container_width=True)

#     # Call a function to compute daily returns for stocks and S&P 500
#     stocks_daily_return = capm_functions.daily_returns(stocks_df)

#     # Dictionary to store calculated Beta and Alpha values for each stock
#     beta = {}
#     alpha = {}

#     # Loop through each selected stock to calculate Beta and Alpha using CAPM functions
#     for stock in stocks_list:
#         st.write(f"Calculating Beta and Alpha for {stock}...")
#         b, a = capm_functions.calculate_beta(stocks_daily_return, stock)
#         beta[stock] = b
#         alpha[stock] = a

#     # Display Beta values in a DataFrame
#     beta_df = pd.DataFrame(list(beta.items()), columns=['Stock', 'Beta'])
#     beta_df['Beta'] = beta_df['Beta'].apply(lambda x: round(x, 2))

#     col1, col2 = st.columns([1, 1])
#     with col1:
#         st.markdown("### Calculated Beta Values for Selected Stocks")
#         st.dataframe(beta_df, use_container_width=True)

#     # CAPM formula: E(R_i) = R_f + Beta_i * (R_m - R_f)
#     rf = 0.01  # Risk-free rate (set as a constant, adjust if needed)
#     rm = stocks_daily_return['sp500'].mean() * 252  # Market return, annualized from daily data

#     # Calculate the expected return for each stock using CAPM
#     expected_returns = []
#     for stock in stocks_list:
#         expected_return = rf + beta[stock] * (rm - rf)
#         expected_returns.append(round(expected_return, 2))

#     # Display the expected returns in a DataFrame
#     return_df = pd.DataFrame({
#         'Stock': stocks_list,
#         'Expected Return (%)': [f"{er * 100:.2f}" for er in expected_returns]
#     })

#     with col2:
#         st.markdown("### Expected Returns (Based on CAPM)")
#         st.dataframe(return_df, use_container_width=True)

#     # Additional visualizations (if needed)
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         st.markdown("### Stock Price Trend Over Time")
#         st.line_chart(stocks_df.set_index('Date')[stocks_list])
    
#     with col2:
#         st.markdown("### S&P 500 Performance")
#         st.line_chart(SP500.set_index('Date')['sp500'])

# except Exception as e:
#     # Handle any errors that occur during data fetching or processing
#     st.error(f"An error occurred: {e}")
#     st.write("Please check your inputs and try again.")

import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import datetime
import capm_functions  # Ensure you have the necessary functions in capm_functions.py

# Configure the Streamlit page
st.set_page_config(
    page_title="Stock Expected Return Calculator",
    page_icon="💹",  # Icon related to stock market
    layout="wide"
)

# Title and description
st.title("📊 Stock Expected Return Calculator")
st.subheader("Calculate Expected Returns for Selected Stocks Using the CAPM Model")
st.markdown("""
This tool allows you to calculate the expected returns for selected stocks based on the **Capital Asset Pricing Model (CAPM)**.
Choose your stocks and the number of years of historical data you would like to analyze.
""")

# Get user input for stock selection and time period
col1, col2 = st.columns([1, 1])
with col1:
    # Allow users to select stocks from a predefined list
    stocks_list = st.multiselect("Select up to 4 stocks", 
                                 options=['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'],
                                 default=['TSLA', 'AAPL', 'AMZN', 'GOOGL'])
with col2:
    # Input for the number of years of data to use for analysis
    year = st.number_input('Select the number of years for historical data', 
                           min_value=1, max_value=10, value=5)

# Set the date range for fetching historical data
end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day)

# Exception handling to avoid app crashes due to bad inputs or connection issues
try:
    # Fetching S&P 500 data as a market benchmark for CAPM calculations
    with st.spinner('Fetching S&P 500 data...'):
        SP500 = web.DataReader('sp500', 'fred', start, end)

    # Initialize an empty DataFrame to store stock prices
    stocks_df = pd.DataFrame()

    # Download stock data for each selected stock from Yahoo Finance
    with st.spinner('Fetching stock data...'):
        for stock in stocks_list:
            stock_data = yf.download(stock, start=start, end=end)
            stocks_df[stock] = stock_data['Close']

    # Reset the index and prepare to merge with S&P 500 data
    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']

    # Ensure the date columns are in datetime format for merging
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # Display the data
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Stock Prices Data (First 5 Rows)")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### S&P 500 Data (First 5 Rows)")
        st.dataframe(SP500.head(), use_container_width=True)

    # Call a function to compute daily returns for stocks and S&P 500
    stocks_daily_return = capm_functions.daily_returns(stocks_df)

    # Dictionary to store calculated Beta and Alpha values for each stock
    beta = {}
    alpha = {}

    # Loop through each selected stock to calculate Beta and Alpha using CAPM functions
    with st.spinner('Calculating Beta and Alpha for selected stocks...'):
        for stock in stocks_list:
            b, a = capm_functions.calculate_beta(stocks_daily_return, stock)
            beta[stock] = b
            alpha[stock] = a

    # Display Beta values in a DataFrame
    beta_df = pd.DataFrame(list(beta.items()), columns=['Stock', 'Beta'])
    beta_df['Beta'] = beta_df['Beta'].apply(lambda x: round(x, 2))

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Calculated Beta Values for Selected Stocks")
        st.dataframe(beta_df, use_container_width=True)

    # CAPM formula: E(R_i) = R_f + Beta_i * (R_m - R_f)
    rf = 0.01  # Risk-free rate (set as a constant, adjust if needed)
    rm = stocks_daily_return['sp500'].mean() * 252  # Market return, annualized from daily data

    # Calculate the expected return for each stock using CAPM
    expected_returns = []
    for stock in stocks_list:
        expected_return = rf + beta[stock] * (rm - rf)
        expected_returns.append(round(expected_return, 2))

    # Display the expected returns in a DataFrame
    return_df = pd.DataFrame({
        'Stock': stocks_list,
        'Expected Return (%)': [f"{er * 100:.2f}" for er in expected_returns]
    })

    with col2:
        st.markdown("### Expected Returns (Based on CAPM)")
        st.dataframe(return_df, use_container_width=True)

    # Additional visualizations (if needed)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Stock Price Trend Over Time")
        st.line_chart(stocks_df.set_index('Date')[stocks_list])
    
    with col2:
        st.markdown("### S&P 500 Performance")
        st.line_chart(SP500.set_index('Date')['sp500'])

except Exception as e:
    # Handle any errors that occur during data fetching or processing
    st.error(f"An error occurred: {e}")
    st.write("Please check your inputs and try again.")
