
import streamlit as st 
import requests
import pandas as pd 

def user_login():
    st.markdown("Please Login To Continue")
    with st.form("Login", clear_on_submit=True):
        username = st.text_input("Username")
        st.session_state['username'] = username
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    if submit_button:    
        response = requests.post("http://127.0.0.1:5000/login", \
                                    json = {'username': username, 
                                            'password': password})
        result = len(response.json())

        if result==0:
            st.error("Invalid username or password")

        else:
            st.success("Login Sucessful.")
            st.session_state['logged_in'] = True
    
def flight_overview():
    # response = requests.get("http://127.0.0.1:5000/overview")
    # st.table(pd.DataFrame(response.json()))

    # Show all avaliable origins to user 
    origin_response = requests.get("http://127.0.0.1:5000/departure")
    origins = pd.DataFrame(origin_response.json()).Departure_City.to_list()
    selected_origin = st.multiselect("Select your Origin", options=origins)

    # Show all avaliable destinations to user 
    # destination_response = requests.get("http://127.0.0.1:5000/destination")
    # origins = pd.DataFrame(origin_response.json()).Departure_City.to_list()



def create_account():
    st.markdown("Please enter your information to register an account")
    with st.form("Create Account", clear_on_submit=True):
        username = st.text_input("Username")
        email = st.text_input("Email", key='email')
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        submit_button = st.form_submit_button("Create")

        if submit_button and password == confirm_password:
             response = requests.put("http://127.0.0.1:5000/create", 
                                     json = {'username': username, 
                                             'password':password,
                                             'email':email})
             result = response.json().get('status')

             if result==200:
                st.success("Account Created Successfully!")

             elif result==500:
                st.error("An account has been registered with the email already. Please try again.")

        elif submit_button: 
            st.error("Invalid Password. Please try again.")


def forgot():
    response = None
    st.markdown("Please enter your information")
    with st.form("Create Account", clear_on_submit=True):
        username = st.text_input("Username")
        email = st.text_input("Email", key='email')
        password = st.text_input("New Password", key='password')
        submit_button = st.form_submit_button("Submit")
        
        if submit_button and username and email:
            response = requests.put("http://127.0.0.1:5000/reset_password", 
                                                json = {'username': username, 
                                                        'password': password,
                                                        'email': email})
            result = response.json().get('status')

            if result==200:
                st.success("Password has been reset.")

            else:
                st.error("Username or Email not recognized")
       

