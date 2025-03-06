import streamlit as st

# Custom CSS for homepage buttons (without conflicting with navbar)
st.markdown(
    """
    <style>
    .homepage-button {
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
        height: 50px;  /* Fixed height */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .homepage-button:hover {
        background-color: #0056b3 !important;
    }
    .button-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;  /* Adjust the gap between buttons */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show():
    st.title("🏠 Welcome to Your Investment Portfolio")
    st.write("Track and manage your investments efficiently.")

    # Create a grid of buttons
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Portfolio Management", key="portfolio_button", help="Manage your investment portfolio"):
            st.session_state['current_page'] = "📊 Portfolio Management"
            st.rerun()
        if st.button("📈 Market Data", key="market_data_button", help="View real-time market data"):
            st.session_state['current_page'] = "📈 Market Data"
            st.rerun()

    with col2:
        if st.button("💡 Investment Recommendations", key="recommendations_button", help="Get personalized investment recommendations"):
            st.session_state['current_page'] = "💡 Investment Recommendations"
            st.rerun()
        if st.button("🎯 Goal Setting", key="goal_setting_button", help="Set and track your financial goals"):
            st.session_state['current_page'] = "🎯 Goal Setting"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)