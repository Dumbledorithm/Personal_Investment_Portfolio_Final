import os
import streamlit as st
import mysql.connector
import bcrypt
from mysql.connector import Error
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify a password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Create a new portfolio for the user
def create_portfolio(user_id):
    connection = get_db_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO Portfolio (UserID)
        VALUES (%s);
        """
        cursor.execute(insert_query, (user_id,))
        connection.commit()
        return True
    except Error as e:
        st.error(f"Error creating portfolio: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Register a new user
def register_user(username, email, password):
    connection = get_db_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        insert_query = """
        INSERT INTO Users (Username, Email, PasswordHash)
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (username, email, hashed_password))
        connection.commit()

        # Get the newly created user's ID
        cursor.execute("SELECT LAST_INSERT_ID();")
        user_id = cursor.fetchone()[0]

        # Create a new portfolio for the user
        if create_portfolio(user_id):
            st.success("Registration successful! Please log in.")
            return True
        else:
            st.error("Failed to create portfolio. Please try again.")
            return False
    except Error as e:
        st.error(f"Error registering user: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Authenticate a user
def authenticate_user(username, password):
    connection = get_db_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        select_query = """
        SELECT UserID, PasswordHash FROM Users WHERE Username = %s;
        """
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result and verify_password(password, result[1]):
            st.session_state['user_id'] = result[0]  # Store user_id in session state
            return True
        else:
            st.error("Invalid username or password.")
            return False
    except Error as e:
        st.error(f"Error authenticating user: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()