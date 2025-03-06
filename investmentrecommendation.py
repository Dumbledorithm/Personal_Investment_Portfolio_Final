import streamlit as st
import numpy as np

def calculate_recommendation(user_goals):
    risk_profile = {
        'conservative': {'return': 0.04, 'bonds': 70, 'stocks': 30},
        'moderate': {'return': 0.06, 'bonds': 50, 'stocks': 50},
        'aggressive': {'return': 0.08, 'bonds': 30, 'stocks': 70}
    }

    profile = risk_profile[user_goals['risk_tolerance']]
    years = user_goals['time_horizon']
    future_value = user_goals['target_amount'] - user_goals['current_savings']

    if future_value <= 0:
        return {
            'status': "Goal already achieved! 🎉",
            'asset_allocation': "",
            'monthly_savings': 0,
            'tips': ["Consider maintaining your current savings strategy"]
        }

    # Calculate required monthly contribution
    monthly_rate = profile['return'] / 12
    months = years * 12
    monthly_savings = (future_value * monthly_rate) / ((1 + monthly_rate)**months - 1)

    recommendation = {
        'asset_allocation': f"{profile['stocks']}% stocks, {profile['bonds']}% bonds",
        'monthly_savings': round(monthly_savings, 2),
        'tips': []
    }

    # Add goal-specific tips
    if user_goals['goal_type'] == "Retirement":
        recommendation['tips'].extend([
            "💰 Consider maxing out IRA/401(k) contributions",
            "📈 Increase stock allocation for long-term growth"
        ])
    elif user_goals['goal_type'] == "House":
        recommendation['tips'].append("🏡 Consider a high-yield savings account for short-term goals")

    return recommendation

def show():
    st.title("💡 Investment Recommendations")

    if 'user_goals' not in st.session_state:
        st.warning("⚠️ Please set your financial goals in the 🎯 Goal Setting section first")
        return

    user_goals = st.session_state['user_goals']
    recommendation = calculate_recommendation(user_goals)

    st.subheader(f"Personalized Recommendation for {user_goals['goal_type']} Goal")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Target Amount", f"${user_goals['target_amount']:,.2f}")
        st.metric("Monthly Savings Needed", f"${recommendation['monthly_savings']:,.2f}")

    with col2:
        st.metric("Recommended Portfolio", recommendation['asset_allocation'])
        st.metric("Time Horizon", f"{user_goals['time_horizon']} years")

    if recommendation['tips']:
        st.subheader("Optimization Tips")
        for tip in recommendation['tips']:
            st.markdown(f"- {tip}")

    # Show progress visualization
    current = user_goals['current_savings']
    target = user_goals['target_amount']
    progress = min(current / target, 1.0)  # Ensure value is between 0.0 and 1.0
    st.progress(progress)
    st.caption(f"Current progress: {progress * 100:.1f}% of target achieved")