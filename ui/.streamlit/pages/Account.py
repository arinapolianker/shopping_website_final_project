import time
import webbrowser

import streamlit as st

# from api.api import register_user, get_jwt_token

register_user = st.session_state.functions['register_user']
get_jwt_token = st.session_state.functions['get_jwt_token']

if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if 'show_registration_form' not in st.session_state:
    st.session_state['show_registration_form'] = False
if 'show_login_form' not in st.session_state:
    st.session_state['show_login_form'] = False

st.set_page_config(
    page_title="Account",  # Sets the browser tab title
    page_icon="📝",  # Optional: Add a notepad emoji as an icon
    layout="centered",  # Optional: Choose centered layout for forms
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None,
    }
)

st.title("User Management Application")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("Register here", key="toggle_register_form"):
        st.session_state.show_registration_form = not st.session_state.show_registration_form
        st.session_state.show_login_form = False

    if st.session_state.show_registration_form:
        st.header("Register a New User")
        first_name = st.text_input("First Name", key="register_firstname")
        last_name = st.text_input("Last Name", key="register_lastname")
        email = st.text_input("Email", key="register_email")
        phone = st.text_input("Phone", key="register_phone")
        address = st.text_input("Address", key="register_address")
        username = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type='password', key="register_password")

        if st.button("Register", key="submit_register"):
            register_response = register_user(first_name, last_name, email, phone, address, username, password)

            if register_response.status_code == 201:
                st.success("Registered successfully!")
                time.sleep(2)
                # st.rerun()
                jwt_token, user_id = get_jwt_token(username, password)

                if jwt_token:
                    st.session_state['jwt_token'] = jwt_token
                    st.session_state['user_id'] = user_id
                    st.success("Registered successfully!")
                    time.sleep(2)
                    st.switch_page("Home.py")
                else:
                    st.error("Registration succeeded but login failed. Please try logging in manually.")
            else:
                st.error("Registration failed. Please check the provided details.")
with col2:
    if st.button("Login here", key="toggle_login_form"):
        st.session_state.show_login_form = not st.session_state.show_login_form
        st.session_state.show_registration_form = False

    if st.session_state.show_login_form:
        st.header("Log in User")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type='password', key="login_password")
        if st.button("Login", key="submit_login"):
            jwt_token, user_id = get_jwt_token(login_username, login_password)
            if jwt_token:
                st.session_state['jwt_token'] = jwt_token
                st.session_state['user_id'] = user_id
                st.success("Logged in successfully!")
                time.sleep(2)
                st.switch_page("Home.py")
            else:
                st.error("Login failed. Check your credentials.")
with col3:
    if st.button("Logout"):
        st.session_state['jwt_token'] = None
        st.success("Logged out successfully!")
# Adjust button positioning
# with st.sidebar:
#     col1, _, col3 = st.columns([1, 0.5, 1])
#     with col1:
#         if st.button("Login"):
#             token = get_jwt_token(login_username, login_password)
#             if token:
#                 st.session_state['jwt_token'] = token
#                 st.sidebar.success("Logged in successfully!")
#             else:
#                 st.sidebar.error("Login failed. Check your credentials.")
#     with col3:
#         if st.button("Logout"):
#             st.session_state['jwt_token'] = None
#             st.sidebar.success("Logged out successfully!")


# Display user list if logged in
# if st.session_state['jwt_token']:
#     st.header("Users List")
#     users_data = get_all_users(st.session_state['jwt_token'])
#     if users_data:
#         users_df = pd.DataFrame(users_data)
#         # Set the DataFrame's to use container width
#         st.dataframe(users_df, use_container_width=True)
#     else:
#         st.write("No users found or failed to fetch data.")
# else:
#     st.write("Please log in to view user data.")
