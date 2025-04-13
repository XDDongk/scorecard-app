
import streamlit as st
import pandas as pd
from score_model import score_card, A, calculate_score_with_card, explain_score_breakdown

st.set_page_config(page_title="Credit Scorecard App", layout="centered")

st.markdown("<h1 style='text-align: center;'>📊 Credit Scoring Application</h1>", unsafe_allow_html=True)
st.markdown("Please input customer information below:")

# Input fields
input_data = {}
input_data['RevolvingUtilizationOfUnsecuredLines'] = st.number_input("Revolving Utilization of Unsecured Lines", min_value=0.0, step=0.01)
input_data['NumberOfTimes90DaysLate'] = st.number_input("Number of Times 90 Days Late", min_value=0, step=1)
input_data['NumberOfTime30-59DaysPastDueNotWorse'] = st.number_input("Number of Times 30-59 Days Past Due", min_value=0, step=1)
input_data['age'] = st.number_input("Age", min_value=0, step=1)
input_data['NumberOfTime60-89DaysPastDueNotWorse'] = st.number_input("Number of Times 60-89 Days Past Due", min_value=0, step=1)

if st.button("Calculate Score"):
    input_df = pd.DataFrame([input_data])
    result = calculate_score_with_card(input_df, score_card, A)
    score = result['score'].iloc[0]

    if score < 530:
        decision = '❌ Reject'
        color = 'red'
    elif score <= 620:
        decision = '⚠️ Manual Review'
        color = 'orange'
    else:
        decision = '✅ Accept'
        color = 'green'

    st.markdown(f"<h3 style='color:{color};'>Decision: {decision}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4>Score: <span style='color:{color};'>{score}</span></h4>", unsafe_allow_html=True)

    # Breakdown explanation only
    st.markdown("### 🧮 Score Breakdown")
    breakdown = explain_score_breakdown(input_df.iloc[0], score_card)
    st.table(breakdown)
