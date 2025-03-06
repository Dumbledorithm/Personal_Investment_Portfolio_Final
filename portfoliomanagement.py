''' import streamlit as st
import plotly.express as px
import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

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

# Fetch user's portfolio data
def fetch_portfolio_data(user_id):
    connection = get_db_connection()
    if connection is None:
        return pd.DataFrame()

    try:
        query = """
        SELECT a.AssetID, a.TickerSymbol, a.AssetType, a.Quantity, a.CurrentValue, m.CurrentPrice
        FROM Assets a
        JOIN MarketData m ON a.TickerSymbol = m.TickerSymbol
        WHERE a.PortfolioID IN (
            SELECT PortfolioID FROM Portfolio WHERE UserID = %s
        );
        """
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        # Convert to DataFrame
        columns = ["AssetID", "TickerSymbol", "AssetType", "Quantity", "CurrentValue", "CurrentPrice"]
        df = pd.DataFrame(result, columns=columns)
        return df
    except Error as e:
        st.error(f"Error fetching portfolio data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Add a new investment to the portfolio
def add_investment(user_id, ticker_symbol, asset_type, quantity, current_value):
    connection = get_db_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return False

    try:
        cursor = connection.cursor()

        # Fetch the user's PortfolioID
        cursor.execute("SELECT PortfolioID FROM Portfolio WHERE UserID = %s;", (user_id,))
        portfolio_id_result = cursor.fetchone()
        if not portfolio_id_result:
            st.error("No portfolio found for the user. Please create a portfolio first.")
            return False

        portfolio_id = portfolio_id_result[0]

        # Insert the new investment
        insert_query = """
        INSERT INTO Assets (PortfolioID, TickerSymbol, AssetType, Quantity, CurrentValue)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (portfolio_id, ticker_symbol, asset_type, quantity, current_value))
        connection.commit()
        st.success("Investment added successfully!")
        return True
    except Error as e:
        st.error(f"Error adding investment: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Show portfolio management page
def show():
    st.title("📊 Portfolio Management")

    # Check if user is logged in
    if 'user_id' not in st.session_state or not st.session_state['user_id']:
        st.error("Please log in to view your portfolio.")
        return

    user_id = st.session_state['user_id']
    st.write(f"Debug: User ID = {user_id}")  # Debug statement

    # Add new investment form
    st.subheader("Add New Investment")
    with st.form("add_investment_form"):
        col1, col2 = st.columns(2)

        with col1:
            ticker_symbol = st.text_input("Ticker Symbol (e.g., AAPL)", placeholder="AAPL")
            asset_type = st.selectbox("Asset Type", ["Stock", "Bond", "ETF", "Other"])

        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            current_value = st.number_input("Current Value ($)", min_value=0.0, value=0.0)

        if st.form_submit_button("Add Investment"):
            if ticker_symbol and asset_type and quantity and current_value:
                if add_investment(user_id, ticker_symbol, asset_type, quantity, current_value):
                    st.success("Investment added successfully!")
                else:
                    st.error("Failed to add investment. Please try again.")
            else:
                st.error("Please fill in all fields.")

    # Fetch and display portfolio data
    portfolio_data = fetch_portfolio_data(user_id)

    if portfolio_data.empty:
        st.warning("Your portfolio is empty. Add investments to get started.")
        return

    # Display portfolio summary
    total_value = portfolio_data['CurrentValue'].sum()
    st.metric("Total Portfolio Value", f"${total_value:,.2f}")

    # Display all assets in a table
    st.subheader("Your Portfolio Assets")
    st.dataframe(portfolio_data)

    # Visualizations
    st.subheader("Portfolio Visualizations")

    # Pie Chart: Asset Allocation by Type
    st.write("### Asset Allocation by Type")
    asset_allocation = portfolio_data.groupby('AssetType')['CurrentValue'].sum().reset_index()
    fig1 = px.pie(asset_allocation, values='CurrentValue', names='AssetType', title="Asset Allocation by Type")
    st.plotly_chart(fig1)

    # Bar Chart: Current Value of Each Asset
    st.write("### Current Value of Each Asset")
    fig2 = px.bar(portfolio_data, x='TickerSymbol', y='CurrentValue', color='AssetType', title="Current Value of Each Asset")
    st.plotly_chart(fig2)'''

import streamlit as st
import plotly.express as px
import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np
from alpha_vantage.timeseries import TimeSeries

# Alpha Vantage API Key
API_KEY = "LILUV0N5VM0009JJ"  # Replace with your Alpha Vantage API key

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
def fetch_real_time_price(ticker_symbol):
    try:
        ts = TimeSeries(key=API_KEY, output_format="pandas")
        data, _ = ts.get_quote_endpoint(symbol=ticker_symbol)
        return float(data["05. price"])  # Extract the latest price
    except Exception as e:
        st.error(f"Error fetching real-time price for {ticker_symbol}: {e}")
        return None

# Fetch user's portfolio data
def fetch_portfolio_data(user_id):
    connection = get_db_connection()
    if connection is None:
        return pd.DataFrame()

    try:
        query = """
        SELECT AssetID, TickerSymbol, AssetType, Quantity, CurrentValue
        FROM Assets
        WHERE PortfolioID IN (
            SELECT PortfolioID FROM Portfolio WHERE UserID = %s
        );
        """
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        # Convert to DataFrame
        columns = ["AssetID", "TickerSymbol", "AssetType", "Quantity", "CurrentValue"]
        df = pd.DataFrame(result, columns=columns)

        # Fetch real-time prices for each asset
        df["CurrentPrice"] = df["TickerSymbol"].apply(fetch_real_time_price)
        df["MarketValue"] = df["Quantity"] * df["CurrentPrice"]

        return df
    except Error as e:
        st.error(f"Error fetching portfolio data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Add a new investment to the portfolio
def add_investment(user_id, ticker_symbol, asset_type, quantity, current_value):
    connection = get_db_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return False

    try:
        cursor = connection.cursor()

        # Fetch the user's PortfolioID
        cursor.execute("SELECT PortfolioID FROM Portfolio WHERE UserID = %s;", (user_id,))
        portfolio_id_result = cursor.fetchone()
        if not portfolio_id_result:
            st.error("No portfolio found for the user. Please create a portfolio first.")
            return False

        portfolio_id = portfolio_id_result[0]

        # Insert the new investment
        insert_query = """
        INSERT INTO Assets (PortfolioID, TickerSymbol, AssetType, Quantity, CurrentValue)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (portfolio_id, ticker_symbol, asset_type, quantity, current_value))
        connection.commit()
        st.success("Investment added successfully!")
        return True
    except Error as e:
        st.error(f"Error adding investment: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Show portfolio management page
def show():
    st.title("📊 Portfolio Management")

    # Check if user is logged in
    if 'user_id' not in st.session_state or not st.session_state['user_id']:
        st.error("Please log in to view your portfolio.")
        return

    user_id = st.session_state['user_id']
    st.write(f"Debug: User ID = {user_id}")  # Debug statement

    # Add new investment form
    st.subheader("Add New Investment")
    with st.form("add_investment_form"):
        col1, col2 = st.columns(2)

        with col1:
            ticker_symbol = st.text_input("Ticker Symbol (e.g., AAPL)", placeholder="AAPL")
            asset_type = st.selectbox("Asset Type", ["Stock", "Bond", "ETF", "Other"])

        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            current_value = st.number_input("Current Value ($)", min_value=0.0, value=0.0)

        if st.form_submit_button("Add Investment"):
            if ticker_symbol and asset_type and quantity and current_value:
                if add_investment(user_id, ticker_symbol, asset_type, quantity, current_value):
                    st.success("Investment added successfully!")
                else:
                    st.error("Failed to add investment. Please try again.")
            else:
                st.error("Please fill in all fields.")

    # Fetch and display portfolio data
    portfolio_data = fetch_portfolio_data(user_id)

    if portfolio_data.empty:
        st.warning("Your portfolio is empty. Add investments to get started.")
        return

    # Display portfolio summary
    total_market_value = portfolio_data["MarketValue"].sum()
    st.metric("Total Portfolio Value", f"${total_market_value:,.2f}")

    # Display all assets in a table
    st.subheader("Your Portfolio Assets")
    st.dataframe(portfolio_data)

    # Visualizations
    st.subheader("Portfolio Visualizations")

    # Pie Chart: Asset Allocation by Type
    st.write("### Asset Allocation by Type")
    asset_allocation = portfolio_data.groupby('AssetType')['MarketValue'].sum().reset_index()
    fig1 = px.pie(asset_allocation, values='MarketValue', names='AssetType', title="Asset Allocation by Type")
    st.plotly_chart(fig1)

    # Bar Chart: Market Value of Each Asset
    st.write("### Market Value of Each Asset")
    fig2 = px.bar(portfolio_data, x='TickerSymbol', y='MarketValue', color='AssetType', title="Market Value of Each Asset")
    st.plotly_chart(fig2)
    