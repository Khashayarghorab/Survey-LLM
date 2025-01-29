import streamlit as st
import re

st.set_page_config(page_title="User Information", page_icon="📝")

st.title("User Information")

st.markdown("Please fill out the form below to provide your details.")

# Function to validate email
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# User Information Form
with st.form("user_info_form"):
    name = st.text_input("Name")
    email = st.text_input("Email", help="Please enter a valid email address.")
    gender = st.radio("Gender", ["Male", "Female", "Other"], index=0)
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    experience = st.selectbox(
        "Please select the number of years of experience in the AEC industry",
        ["0-1 years", "1-3 years", "3-5 years", "5+ years"]
    )
    role = st.selectbox(
        "Please select your current project role",
        ["Project Manager", "Engineer", "Architect", "Contractor", "Other"]
    )
    ai_usage = st.text_area(
        "In your day-to-day activities, how do you use generative AI? Have you used it before in the AEC industry?"
    )
    familiarity_jsa = st.slider(
        "How familiar are you with JSA and risk management?",
        0, 10, 5, help="Rate your familiarity from 0 (not familiar) to 10 (very familiar)"
    )
    comments = st.text_area(
        "Please comment on how your experience was and anything else you'd like to share."
    )
    submit_user_info = st.form_submit_button("Submit")

# Display User Information After Submission
if submit_user_info:
    if name.strip() == "":
        st.error("Please provide your name.")
    elif email.strip() == "" or not is_valid_email(email):
        st.error("Please provide a valid email address.")
    else:
        st.success("Thank you for providing your information!")
        user_info = {
            "Name": name,
            "Email": email,
            "Gender": gender,
            "Age": age,
            "Experience": experience,
            "Role": role,
            "AI Usage": ai_usage,
            "Familiarity with JSA": familiarity_jsa,
            "Comments": comments
        }

        # Store user info in session state
        st.session_state.user_info = user_info

        # Navigation Buttons with Beautiful Styling
        st.markdown("### What would you like to do next?")
        col1, col2 = st.columns(2)


                
        

        with col1:
            st.page_link("pages/App.py", label="Go to Task Page", icon="📝")

        with col2:
            st.page_link("pages/AppLive.py", label="Go to Home Page", icon="🏠")

        # Add some styles to make the buttons look more appealing
        st.markdown(
            """
            <style>
            div.stButton > button:first-child {
                background-color: #4CAF50; /* Green */
                color: white;
                font-size: 16px;
                margin: 5px;
                padding: 10px 24px;
                border-radius: 8px;
            }
            div.stButton > button:hover {
                background-color: #45a049;
                color: white;
            }
            div.stButton + div.stButton > button:first-child {
                background-color: #008CBA; /* Blue */
                color: white;
                font-size: 16px;
                margin: 5px;
                padding: 10px 24px;
                border-radius: 8px;
            }
            div.stButton + div.stButton > button:hover {
                background-color: #007bb5;
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
