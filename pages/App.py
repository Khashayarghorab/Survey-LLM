import streamlit as st
import pandas as pd
import random
import re
import json
import os
from io import StringIO
from google.oauth2 import service_account
import gspread
from utils import display_response, extract_tables, log_to_google_sheet
from questions import initial_questions  # Import the initial questions




st.set_page_config(layout="wide", page_title="LLM Response Comparison", page_icon="🔎")



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

# 📜 How It Works
st.markdown("""
### 📜 How It Works
- **Blind Test:** Below are the responses of two LLM models. One is a single-agent system, and the other is a multi-agent system.
- **Vote for the Best:** We ask you to vote on which model generates a better JSA (Job Safety Analysis) report. 
- **Play Fair:** For fairness, their places are shuffled randomly between Response A and Response B. You can select either of them, a tie, or indicate that both are bad.

Here are 5 predefined tasks where you can see the JSA reports below. Thank you for participating!
""")

# Show both options at the start
st.header("Choose a Task")
# st.header("Choose a Task or Input Your Task")

# # Display task buttons
# st.subheader("Choose from Predefined Tasks")

col1, col2, col3, col4, col5 = st.columns(5)

# Initialize session state variables
if "response_mapping" not in st.session_state:
    st.session_state.response_mapping = {"A": "", "B": ""}
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""
if "final_mapping" not in st.session_state:
    st.session_state.final_mapping = None
if "responses_shuffled" not in st.session_state:
    st.session_state.responses_shuffled = False
if "selection_made" not in st.session_state:
    st.session_state.selection_made = False

# Handle predefined task button presses
if col1.button(initial_questions[0]["question"]):
    st.session_state.current_question = initial_questions[0]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col2.button(initial_questions[1]["question"]):
    st.session_state.current_question = initial_questions[1]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col3.button(initial_questions[2]["question"]):
    st.session_state.current_question = initial_questions[2]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col4.button(initial_questions[3]["question"]):
    st.session_state.current_question = initial_questions[3]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col5.button(initial_questions[4]["question"]):
    st.session_state.current_question = initial_questions[4]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False

# Randomize responses if a question is selected and responses are not shuffled
if st.session_state.current_question and not st.session_state.responses_shuffled:
    original_mapping = {
        "Model 1": st.session_state.current_question["A"],
        "Model 2": st.session_state.current_question["B"]
    }

    shuffled = list(original_mapping.items())
    random.shuffle(shuffled)
    st.session_state.response_mapping = {
        "A": {"response": shuffled[0][1], "model": shuffled[0][0]},
        "B": {"response": shuffled[1][1], "model": shuffled[1][0]}
    }
    st.session_state.final_mapping = st.session_state.response_mapping.copy()
    st.session_state.responses_shuffled = True

# Display responses if available
if st.session_state.final_mapping and st.session_state.final_mapping["A"] and st.session_state.final_mapping["B"]:
    st.subheader("Choose the Better LLM Response")
    with st.form("response_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("Response A")
            display_response(st.session_state.final_mapping["A"]["response"])

        with col2:
            st.subheader("Response B")
            display_response(st.session_state.final_mapping["B"]["response"])

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

        # Display the user selection result and map back to the model
        if not st.session_state.selection_made:
            if a_better:
                log_to_google_sheet("A is better", st.session_state.final_mapping['A']['model'], st.session_state.current_question['question'], st.session_state.user_prompt, user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success(f"You selected: A is better")
            elif b_better:
                log_to_google_sheet("B is better", st.session_state.final_mapping['B']['model'], st.session_state.current_question['question'], st.session_state.user_prompt, user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success(f"You selected: B is better")
            elif tie:
                log_to_google_sheet("Tie", "Model 1 and Model 2", st.session_state.current_question['question'], st.session_state.user_prompt, user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success("You selected: It's a tie")
            elif both_bad:
                log_to_google_sheet("Both are bad", "None", st.session_state.current_question['question'], st.session_state.user_prompt, user_info['Name'], user_info['Email'], user_info['Gender'], user_info['Age'], user_info['Experience'], user_info['Role'], user_info['AI Usage'], user_info['Familiarity with JSA'], user_info['Comments'])
                st.session_state.selection_made = True
                st.success("You selected: Both are bad")
