import streamlit as st

# Custom CSS for blue buttons
st.markdown(
    """
    <style>
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

def show():
    st.title("🏠 Welcome to Your Investment Portfolio")
    st.write("Track and manage your investments efficiently.")

    # Create a grid of buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Portfolio Management", key="portfolio_button"):
            st.session_state['current_page'] = "📊 Portfolio Management"
            st.rerun()
        if st.button("📈 Market Data", key="market_data_button"):
            st.session_state['current_page'] = "📈 Market Data"
            st.rerun()

    with col2:
        if st.button("💡 Investment Recommendations", key="recommendations_button"):
            st.session_state['current_page'] = "💡 Investment Recommendations"
            st.rerun()
        if st.button("🎯 Goal Setting", key="goal_setting_button"):
            st.session_state['current_page'] = "🎯 Goal Setting"
            st.rerun()
