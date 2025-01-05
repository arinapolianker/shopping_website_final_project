import streamlit as st
import pandas as pd
from api import register_user, get_jwt_token, get_all_users

# Initialize session state
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if 'show_registration_form' not in st.session_state:
    st.session_state['show_registration_form'] = False

st.title("User Management Application")

if st.button("New User"):
    st.session_state.show_registration_form = not st.session_state.show_registration_form

if st.session_state.show_registration_form:
    st.header("Register a New User")
    first_name = st.text_input("First Name", key="register_firstname")
    last_name = st.text_input("Last Name", key="register_lastname")
    email = st.text_input("Last Name", key="register_email")
    phone = st.text_input("Last Name", key="register_phone")
    address = st.text_input("Last Name", key="register_address")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type='password', key="register_password")

    if st.button("Register"):
        register_response = register_user(first_name, last_name, email, phone, address, username, password)
        if register_response.status_code == 201:
            st.success("Registered successfully!")
        else:
            st.error("Failed to register.")

# Sidebar for existing user login
st.sidebar.header("Existing User Login")
login_username = st.sidebar.text_input("Username", key="login_username")
login_password = st.sidebar.text_input("Password", type='password', key="login_password")

# Adjust button positioning
with st.sidebar:
    col1, _, col3 = st.columns([1, 0.5, 1])
    with col1:
        if st.button("Login"):
            token = get_jwt_token(login_username, login_password)
            if token:
                st.session_state['jwt_token'] = token
                st.sidebar.success("Logged in successfully!")
            else:
                st.sidebar.error("Login failed. Check your credentials.")
    with col3:
        if st.button("Logout"):
            st.session_state['jwt_token'] = None
            st.sidebar.success("Logged out successfully!")

# Display user list if logged in
if st.session_state['jwt_token']:
    st.header("Users List")
    users_data = get_all_users(st.session_state['jwt_token'])
    if users_data:
        users_df = pd.DataFrame(users_data)
        # Set the DataFrame's to use container width
        st.dataframe(users_df, use_container_width=True)
    else:
        st.write("No users found or failed to fetch data.")
else:
    st.write("Please log in to view user data.")
