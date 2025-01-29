import streamlit as st
import pandas as pd
import random
import json
import os
from google.oauth2 import service_account
import gspread
from utils import display_response, log_to_google_sheet
from models import generate_jsa_response_A, generate_jsa_response_B

st.set_page_config(layout="wide", page_title="Task-Based LLM Response Comparison", page_icon="🔎")

st.title("LLM Response Comparison")


# Check if user info is available
if "user_info" not in st.session_state:
    st.error("Please provide your user information on the previous page!")
    st.stop()

# Display user info
user_info = st.session_state.user_info

# Display user's name using select_slider
st.sidebar.title("User Information")
st.sidebar.write(f"**Name:** {user_info['Name']}")
st.sidebar.write(f"**Email:** {user_info['Email']}")
st.sidebar.write("Thank you for participating!")

# How it works section
st.markdown(
    """
    ## 📜 How It Works
    - **Blind Test:** Below are the responses of two LLM models. One is a single-agent system, and the other is a multi-agent system.
    - **Vote for the Best:** We ask you to vote on which model generates a better JSA (Job Safety Analysis) report. 
    - **Play Fair:** For fairness, their places are shuffled randomly between Response A and Response B. You can select either of them, a tie, or indicate that both are bad.

    
    """
)

# Task Input Section
st.subheader("Input Your Task")
task_input = st.text_input("🚀 Get started by entering your task below and comparing the results!")
generate_responses = st.button("Generate Responses")

# Initialize session state variables
if "response_mapping" not in st.session_state:
    st.session_state.response_mapping = {"A": "", "B": ""}
if "responses_shuffled" not in st.session_state:
    st.session_state.responses_shuffled = False
if "selection_made" not in st.session_state:
    st.session_state.selection_made = False

# Generate and shuffle responses
if generate_responses and task_input:
    with st.spinner("Generating responses. Please wait."):
        responses = [      
            {"response": generate_jsa_response_A(task_input), "model": "Model 1"},
            {"response": generate_jsa_response_B(task_input), "model": "Model 2"}
        ]

        random.shuffle(responses)
        st.session_state.response_mapping = {
            "A": responses[0],
            "B": responses[1]
        }
        st.session_state.responses_shuffled = True
        st.session_state.selection_made = False

# Display responses if available
if st.session_state.responses_shuffled:
    st.subheader("Choose the Better LLM Response")
    with st.form("response_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("Response A")
            display_response(st.session_state.response_mapping["A"]["response"])

        with col2:
            st.subheader("Response B")
            display_response(st.session_state.response_mapping["B"]["response"])

        # User interaction buttons
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            a_better = st.form_submit_button("👈 A is better")
        with col_b2:
            b_better = st.form_submit_button("👉 B is better")
        with col_b3:
            tie = st.form_submit_button("🤝 Tie")
        with col_b4:
            both_bad = st.form_submit_button("👎 Both are bad")

    

        # Log selection and display result
        if not st.session_state.selection_made:
            if a_better:
                log_to_google_sheet("A is better", st.session_state.response_mapping['A']['model'], task_input," ", user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success("You selected: A is better")
            elif b_better:
                log_to_google_sheet("B is better", st.session_state.response_mapping['B']['model'], task_input," ", user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success("You selected: B is better")
            elif tie:
                log_to_google_sheet("Tie", "Model 1 and Model 2", task_input," ", user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success("You selected: It's a tie")
            elif both_bad:
                log_to_google_sheet("Both are bad", "None", task_input," ", user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success("You selected: Both are bad")
        