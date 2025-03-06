import streamlit as st
import mysql.connector
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from mysql.connector import Error
import plotly.express as px

# Alpha Vantage API Key
API_KEY = "LILUV0N5VM0009JJ"  # Replace with your Alpha Vantage API key

# Initialize Alpha Vantage TimeSeries object
ts = TimeSeries(key=API_KEY, output_format="pandas")

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysqlroot7",
            database="InvestmentDB"
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Fetch real-time market data for a given ticker symbol
def fetch_real_time_market_data(ticker_symbol):
    try:
        data, _ = ts.get_quote_endpoint(symbol=ticker_symbol)  # Fetch real-time data
        return data
    except Exception as e:
        st.error(f"Error fetching real-time market data for {ticker_symbol}: {e}")
        return None

# Show market data page
def show():
    st.title("📈 Real-Time Market Data")

    # Input for stock symbol
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, GOOGL):", "AAPL")

    if st.button("Get Market Data", key="get_market_data_button"):
        # Fetch real-time market data
        market_data = fetch_real_time_market_data(stock_symbol)

        if market_data is not None:
            # Display real-time market data
            st.write(f"### Real-Time Market Data for {stock_symbol}")

            # Extract relevant fields from the API response
            real_time_data = {
                "Symbol": stock_symbol,
                "Price": market_data["05. price"],
                "Change": market_data["09. change"],
                "Change Percent": market_data["10. change percent"],
                "Volume": market_data["06. volume"],
                "Latest Trading Day": market_data["07. latest trading day"],
                "Previous Close": market_data["08. previous close"],
            }

            # Convert to DataFrame for better display
            df = pd.DataFrame(list(real_time_data.items()), columns=["Field", "Value"])
            st.dataframe(df)

            # Display additional visualizations (optional)
            st.write("### Additional Visualizations")

            # Bar chart for key metrics
            st.write("#### Key Metrics")
            fig1 = px.bar(
                df[df["Field"].isin(["Price", "Change", "Volume"])],
                x="Field",
                y="Value",
                title=f"Key Metrics for {stock_symbol}",
            )
            st.plotly_chart(fig1)

            # Line chart for price trend (optional, if historical data is also fetched)
            st.write("#### Price Trend (Last 5 Days)")
            try:
                historical_data, _ = ts.get_daily(symbol=stock_symbol, outputsize="compact")
                historical_data = historical_data.head()  # Get the last 5 days
                fig2 = px.line(
                    historical_data,
                    x=historical_data.index,
                    y="4. close",
                    title=f"Price Trend for {stock_symbol} (Last 5 Days)",
                )
                st.plotly_chart(fig2)
            except Exception as e:
                st.error(f"Error fetching historical data for visualization: {e}")
        else:
            st.error("Failed to fetch real-time market data. Please try again.")