# import streamlit as st
# import pandas as pd
# import numpy as np
# import pandas_datareader.data as web
# import yfinance as yf
# import datetime
# import capm_functions  # Assuming capm_functions.py contains necessary utility functions

# # Set up the page
# st.set_page_config(page_title="Beta Calculator",
#                    page_icon="💹",
#                    layout="wide")

# st.title("📊 Calculate Beta for Selected Stocks")
# st.subheader("Analyze the risk of stocks compared to the market")

# # Input from user: stock selection and number of years
# col1, col2 = st.columns([1, 1])
# with col1:
#     stocks_list = st.multiselect("Select stocks to analyze", 
#                                  ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'],
#                                  ['TSLA', 'AAPL', 'AMZN', 'GOOGL'])  # Default stocks
# with col2:
#     year = st.number_input('Number of years of historical data', 1, 10, value=5)  # Default to 5 years

# # Download stock data and SP500 data
# try:
#     # Define time range for data collection
#     end = datetime.date.today()
#     start = datetime.date(end.year - year, end.month, end.day)

#     # Get S&P 500 data
#     SP500 = web.DataReader(['sp500'], 'fred', start, end)

#     # Get stock data from Yahoo Finance
#     stocks_df = pd.DataFrame()
#     for stock in stocks_list:
#         data = yf.download(stock, period=f'{year}y')
#         stocks_df[f'{stock}'] = data['Close']

#     # Reset index to merge by date
#     stocks_df.reset_index(inplace=True)
#     SP500.reset_index(inplace=True)
#     SP500.columns = ['Date', 'sp500']
#     stocks_df['Date'] = pd.to_datetime(stocks_df['Date'].apply(lambda x: str(x)[:10]))
#     stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

#     # Display stock data
#     st.markdown("### Stock Data")
#     st.dataframe(stocks_df.head(), use_container_width=True)

#     # Calculate daily returns
#     stocks_daily_return = capm_functions.daily_returns(stocks_df)

#     # Calculate beta and alpha for each stock
#     beta = {}
#     alpha = {}

#     for stock in stocks_list:
#         b, a = capm_functions.calculate_beta(stocks_daily_return, stock)
#         beta[stock] = b
#         alpha[stock] = a

#     # Display Beta values
#     beta_df = pd.DataFrame({
#         'Stock': beta.keys(),
#         'Beta Value': [round(b, 2) for b in beta.values()],
#         'Alpha Value': [round(a, 2) for a in alpha.values()]
#     })

#     st.markdown("### Beta and Alpha Values")
#     st.dataframe(beta_df, use_container_width=True)

# except Exception as e:
#     st.error(f"Error fetching or processing data: {e}")




import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import yfinance as yf
import datetime
import capm_functions  # Assuming capm_functions.py contains necessary utility functions
import plotly.express as px

# Set up the page configuration
st.set_page_config(page_title="Beta & Alpha Calculator",
                   page_icon="💹",
                   layout="wide")

# Title and description
st.title("📊 Stock Beta & Alpha Calculator")
st.subheader("Evaluate the risk and return of stocks compared to the overall market (S&P 500)")

# Collect user input for stock selection and historical period
col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect("Select stocks to analyze", 
                                 ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'],
                                 ['TSLA', 'AAPL', 'AMZN', 'GOOGL'])  # Default stock selection
    if not stocks_list:
        st.warning("Please select at least one stock to analyze.")
        
with col2:
    year = st.number_input('Number of years of historical data', min_value=1, max_value=10, value=5)
    st.write(f"Analyzing {len(stocks_list)} stocks over the last {year} years.")

# Function to fetch stock data and S&P 500 data
def get_stock_data(stocks_list, years):
    # Define the date range
    end = datetime.date.today()
    start = datetime.date(end.year - years, end.month, end.day)
    
    # Fetch stock data from Yahoo Finance
    stock_data = pd.DataFrame()
    for stock in stocks_list:
        data = yf.download(stock, start=start, end=end)
        stock_data[stock] = data['Close']
    
    # Fetch S&P 500 index data
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']
    
    return stock_data, SP500

# Attempt to fetch and process stock data
if stocks_list:
    try:
        stock_data, SP500 = get_stock_data(stocks_list, year)

        # Merge stock data with SP500 data on the Date column
        stock_data.reset_index(inplace=True)
        stock_data['Date'] = pd.to_datetime(stock_data['Date'].apply(lambda x: str(x)[:10]))
        merged_data = pd.merge(stock_data, SP500, on='Date', how='inner')

        # Display merged stock data
        st.markdown("### Merged Stock & S&P 500 Data")
        st.dataframe(merged_data.head(), use_container_width=True)

        # Visualize stock prices over time
        st.markdown("### Stock Price Over Time")
        stock_fig = px.line(merged_data, x='Date', y=stocks_list, title='Stock Prices')
        st.plotly_chart(stock_fig, use_container_width=True)

        # Calculate daily returns
        st.markdown("### Daily Returns of Stocks")
        daily_returns = capm_functions.daily_returns(merged_data)
        st.dataframe(daily_returns.head(), use_container_width=True)

        # Visualize daily returns
        returns_fig = px.line(daily_returns, x='Date', y=stocks_list, title='Daily Stock Returns')
        st.plotly_chart(returns_fig, use_container_width=True)

        # Calculate beta and alpha values for each selected stock
        beta = {}
        alpha = {}
        for stock in stocks_list:
            b, a = capm_functions.calculate_beta(daily_returns, stock)
            beta[stock] = b
            alpha[stock] = a

        # Create a DataFrame for displaying beta and alpha values
        beta_alpha_df = pd.DataFrame({
            'Stock': beta.keys(),
            'Beta Value': [round(b, 2) for b in beta.values()],
            'Alpha Value': [round(a, 2) for a in alpha.values()]
        })

        # Display beta and alpha values
        st.markdown("### Calculated Beta & Alpha Values")
        st.dataframe(beta_alpha_df, use_container_width=True)

        # Visualize beta values in a bar chart
        st.markdown("### Beta Value Bar Chart")
        beta_fig = px.bar(beta_alpha_df, x='Stock', y='Beta Value', title='Stock Beta Values', color='Beta Value')
        st.plotly_chart(beta_fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching or processing data: {e}")
