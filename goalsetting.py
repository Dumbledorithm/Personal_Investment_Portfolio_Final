import streamlit as st
import mysql.connector
from mysql.connector import Error

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

# Save goals to the database
def save_goals_to_db(user_id, age, current_savings, risk_tolerance, time_horizon, target_amount, goal_type):
    connection = get_db_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO UserGoals (UserID, Age, CurrentSavings, RiskTolerance, TimeHorizon, TargetAmount, GoalType)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (user_id, age, current_savings, risk_tolerance, time_horizon, target_amount, goal_type))
        connection.commit()
        return True
    except Error as e:
        st.error(f"Error saving goals to the database: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Fetch user's saved goals
def fetch_user_goals(user_id):
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT Age, CurrentSavings, RiskTolerance, TimeHorizon, TargetAmount, GoalType
        FROM UserGoals
        WHERE UserID = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.fetchall()  # Ensures no unread results remain
        return result
    except Error as e:
        st.error(f"Error fetching goals: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Display goal-setting page
def show():
    st.title("🎯 Goal Setting")
    st.write("Set and track your financial goals.")

    if 'user_id' in st.session_state and st.session_state['user_id']:
        saved_goals = fetch_user_goals(st.session_state['user_id'])
        if saved_goals:
            st.write("### Your Saved Goals")
            st.write(f"- **Age**: {saved_goals['Age']}")
            st.write(f"- **Current Savings**: ${saved_goals['CurrentSavings']:,.2f}")
            st.write(f"- **Risk Tolerance**: {saved_goals['RiskTolerance']}")
            st.write(f"- **Time Horizon**: {saved_goals['TimeHorizon']} years")
            st.write(f"- **Target Amount**: ${saved_goals['TargetAmount']:,.2f}")
            st.write(f"- **Goal Type**: {saved_goals['GoalType']}")

    with st.form("goal_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
            current_savings = st.number_input("Current Savings ($)", min_value=0.0, value=5000.0)
            risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])

        with col2:
            time_horizon = st.number_input("Years to Goal", min_value=1, max_value=60, value=10)
            target_amount = st.number_input("Target Amount ($)", min_value=100.0, value=100000.0)
            goal_type = st.selectbox("Goal Type", ["Retirement", "House", "Education", "Other"])

        if st.form_submit_button("Save Goal"):
            if save_goals_to_db(st.session_state['user_id'], age, current_savings, risk_tolerance, time_horizon, target_amount, goal_type):
                st.session_state['user_goals'] = {
                    'age': age,
                    'current_savings': current_savings,
                    'risk_tolerance': risk_tolerance.lower(),
                    'time_horizon': time_horizon,
                    'target_amount': target_amount,
                    'goal_type': goal_type
                }
                st.success("Goals saved successfully!")
                st.write("Navigate to 💡 Investment Recommendations for personalized advice")
            else:
                st.error("Failed to save goals. Please try again.")
