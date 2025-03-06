import streamlit as st

# 🛑 Ensure this is the first Streamlit command!
st.set_page_config(page_title="CapLens : Personal Investment Portfolio Management Tool", layout="wide")

import homepage
import portfoliomanagement
import marketdata
import investmentrecommendation
import goalsetting
import auth

# Session state for authentication and navigation
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "🏠 Home"

# Custom CSS for blue buttons and navbar
st.markdown(
    """
    <style>
    .navbar {
        display: flex;
        justify-content: space-around;
        background-color: #2C3E50;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        transition: background-color 0.3s, transform 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .navbar a:hover {
        background-color: #1ABC9C;
        transform: translateY(-2px);
    }
    .navbar .active {
        background-color: #1ABC9C;
    }
    .stButton button {
        background-color: #007BFF !important;
        color: white !important;
        padding: 12px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #0056b3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Authentication Form
def auth_form():
    st.sidebar.title("🔐 Authentication")
    tab1, tab2 = st.sidebar.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if auth.authenticate_user(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()

    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose a Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Choose a Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Register"):
                if new_password == confirm_password:
                    if auth.register_user(new_username, new_email, new_password):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = new_username
                        st.rerun()
                else:
                    st.error("Passwords do not match.")

# Navbar for Navigation
def navbar():
    pages = {
        "🏠 Home": homepage.show,
        "📊 Portfolio Management": portfoliomanagement.show,
        "📈 Market Data": marketdata.show,
        "💡 Investment Recommendations": investmentrecommendation.show,
        "🎯 Goal Setting": goalsetting.show,
    }

    # Create a row of buttons for navigation
    cols = st.columns(len(pages))
    for idx, (page_name, page_function) in enumerate(pages.items()):
        if cols[idx].button(page_name):
            st.session_state['current_page'] = page_name
            st.rerun()

    # Render the selected page
    if st.session_state['current_page'] in pages:
        pages[st.session_state['current_page']]()

# Main App Logic
if st.session_state['authenticated']:
    navbar()
    
    # Sidebar for User Info & Logout
    st.sidebar.title(f"👤 Welcome, {st.session_state['username']}")
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['user_id'] = None
        st.session_state['current_page'] = "🏠 Home"
        st.rerun()
else:
    auth_form()
    st.stop()
