
import streamlit as st
import pandas as pd
from score_model import score_card, A, calculate_score_with_card, score_to_decision

st.set_page_config(page_title="Credit Scorecard", layout="centered")
st.title("📊 Credit Scoring Application")
st.markdown("This tool calculates a credit score based on predefined scorecard rules and provides a decision.")

st.sidebar.header("Enter Customer Features")

# Define input fields
input_data = {
    'RevolvingUtilizationOfUnsecuredLines': st.sidebar.number_input('Revolving Utilization of Unsecured Lines', min_value=0.0, step=0.01),
    'NumberOfTimes90DaysLate': st.sidebar.number_input('Number of Times 90 Days Late', min_value=0, step=1),
    'NumberOfTime30-59DaysPastDueNotWorse': st.sidebar.number_input('Number of Times 30-59 Days Past Due', min_value=0, step=1),
    'age': st.sidebar.number_input('Age', min_value=18, step=1),
    'NumberOfTime60-89DaysPastDueNotWorse': st.sidebar.number_input('Number of Times 60-89 Days Past Due', min_value=0, step=1)
}

user_df = pd.DataFrame([input_data])

if st.button("Calculate Score"):
    result_df = calculate_score_with_card(user_df, score_card, A)
    score = result_df['score'].iloc[0]
    decision = score_to_decision(score)

    st.subheader(f"📈 Credit Score: `{score}`")
    st.markdown(f"### Decision: **{decision}**")

    st.markdown("----")
    st.markdown("#### Input Summary")
    st.dataframe(user_df)
