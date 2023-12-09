
import streamlit as st 
import requests
import pandas as pd 
import sys 
sys.path.append('../')
from config import * 
from datetime import datetime
import shortuuid
import time 

def user_login():
    st.markdown("Please Login To Continue")
    with st.form("Login", clear_on_submit=True):
        username = st.text_input("Username")
        st.session_state['username'] = username
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

    if submit_button:    
        response = requests.post(API_URL + "/login", \
                                    json = {'username': username, 
                                            'password': password})
        result = len(response.json())

        if result==0:
            st.error("Invalid username or password")

        else:
            with st.spinner('Logging In...'):
                time.sleep(3)
            st.success("Login Sucessful.")
            st.session_state['user_id'] = response.json()[0].get('User_ID')
            st.session_state['logged_in'] = True
            

def flight_overview():

    st.write('Enter Your Travel Plans')

    # Show all avaliable origins to user 
    origin_response = requests.get(API_URL + "/departure")
    origins = pd.DataFrame(origin_response.json()).Departure_City.to_list()
    selected_origin = st.selectbox("🛫 Select your Origin", options=origins)

    # Show all avaliable flight company 
    destination_response = requests.post(API_URL + "/destination",
                                        json = {
                                        'selected_origin': selected_origin})
    
    destinatons = pd.DataFrame(destination_response.json()).Arrival_City.to_list()
    selected_destination = st.selectbox("🛬 Select your Destination", options=destinatons )

    # Show all avaliable destinations to user 
    company_response = requests.post(API_URL + "/companies",
                                     json = {
                                        'selected_origin': selected_origin,
                                        'selected_destination': selected_destination
                                        })
    companies = pd.DataFrame(company_response.json()).Flight_Company.to_list()
    selected_company = st.selectbox("Select your desired airlines", options=companies)
    
    # date selection
    # lets initialize a starting window 
    start_date = datetime.strptime("2023-09-10 00:00:00", "%Y-%m-%d %H:%M:%S")

    # lets also initialize an end date 
    end_date = datetime.strptime("2023-12-31 00:00:00", "%Y-%m-%d %H:%M:%S")

    date_selection = st.date_input(
        "📅 Select a date range",
        (start_date, end_date),
        start_date,
        end_date,
        format="MM.DD.YYYY")
    
    try:
        json = {
            'selected_origin': selected_origin, 
            'selected_destination': selected_destination,
            'selected_company': selected_company,
            'start_date': str(date_selection[0]),
            'end_date': str(date_selection[1])
            }
    except:
        st.warning('Please Select a Range')
        json = None 
        
    st.markdown("""---""")

    if json:
        search_results = requests.post(API_URL + '/search',json=json)
        st.write('Search Results')
        with st.spinner('Refreshing Flights...'):
            time.sleep(1.5)
        search_results = pd.DataFrame(search_results.json())
        st.table(search_results)  

        if len(search_results)>0 :
            
            flight_id = st.selectbox('Select A Flight to purchase',search_results['Flight_ID'])
            purchase = st.button('🛒 Purchase')
            reference_number = shortuuid.uuid()
            
            if purchase: 
                with st.spinner('Processing Your Request...'):
                    time.sleep(5)
                
                purchase_response = requests.put(API_URL + '/purchase', json={
                                                'flight_id' : flight_id, 
                                                'reference_number': reference_number,
                                                'user_id': int(st.session_state['user_id'])
                                                })
                if purchase_response.json().get('status') == 200:
                    st.success('Purchase Sucessful. Reference Number: {}'.format(reference_number))

                else:
                    st.warning('Error Occured. Please try again later.')
    else:
        pass 
                                            
def create_account():
    st.markdown("Please enter your information to register an account")
    with st.form("Create Account", clear_on_submit=True):
        username = st.text_input("Username")
        email = st.text_input("Email", key='email')
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        submit_button = st.form_submit_button("Create")

        if submit_button and password == confirm_password:
             response = requests.put(API_URL + "/create", 
                                     json = {'username': username, 
                                             'password':password,
                                             'email':email})
             result = response.json().get('status')

             if result==200:
                with st.spinner('Creating Account'):
                    time.sleep(3)
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
            response = requests.put(API_URL + "/reset_password", 
                                                json = {'username': username, 
                                                        'password': password,
                                                        'email': email})
            try:
                result = response.json().get('status')
            except:
                result = 500

            if result==200:
                with st.spinner('Resetting Password...'):
                    time.sleep(3)
                st.success("Password has been reset.")

            else:
                st.error("Username or Email not recognized")
       
def orders():
    st.info(
        """📎 Attention all customers: We kindly remind you that in order to receive a refund for your purchase,
        okease make the refund request a minimum of two weeks before the
        designated event or activity. This policy ensures sufficient time for processing
        and allows us to accommodate your needs effectively. Thank you for your cooperation and understanding."""
        )
    
    purchased_tickets = requests.post(API_URL + '/purchased_tickets',
                                      json={'user_id': st.session_state['user_id']})
    results = pd.DataFrame(purchased_tickets.json())
    st.table(results)

    st.markdown("---")

    st.write("Ticket Refunds")
    
    try:
        ticket_id = st.selectbox('Select a Ticket to Refund',results.Reference_Number.to_list())
        reason = st.text_input('Reason for the refund')
        refund = st.button('Refund')

        if reason and refund:
            with st.spinner('Processing your request.'):
                    time.sleep(3)
            reference_number = shortuuid.uuid()
            purchase_response = requests.put(API_URL + '/refund', json={
                                            'ticket_id' : ticket_id, 
                                            'reference_number': reference_number,
                                            'reason': reason
                                            })
            if purchase_response.json().get('status') == 200:
                st.success('Request Sucessful. Reference Number: {}'.format(reference_number))
            
            else:
                st.warning('Error Has Occured. Please try again later')

        elif refund:
            st.warning('Please enter the reason of your refund request.')
          
    except:
        st.text('No Tickets to refund')
    
    
def special_offers():
    st.markdown('Special Offers')
    purchased_tickets = requests.get(API_URL + '/offers')
    results = pd.DataFrame(purchased_tickets.json())
    st.table(results)

def refund_tickets():
    st.markdown('Refund Requests')
    st.info("All Pending Refund Tickets Will be Listed down below.")

    tickets  = requests.post(API_URL + '/refund_view',
                                      json={'user_id': st.session_state['user_id']})
    results = pd.DataFrame(tickets.json())
    st.table(results)