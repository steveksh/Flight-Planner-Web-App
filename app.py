import streamlit as st 
import streamlit.components.v1 as com
import os
import datetime
import pandas as pd
import numpy as np
from app_modules.utils import * 

# Header 
com.iframe("https://lottie.host/embed/b488bb3a-4c39-432e-8e11-ea0692d35560/XdNwCxlslm.json", height= 200)
st.title("Welcome to Our Airline Booking System")


    
def main():
    login = False
       
    menu = ["🔐 Login", "📝 Signup", "❓ Reset Password"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "📝 Signup":
        with st.sidebar:
            create_account()

    elif choice == '🔐 Login':
        with st.sidebar:
            login = user_login()
    elif choice == '❓ Reset Password':
        with st.sidebar:
            forgot()
   
    if login: 
        option = st.selectbox(
        "How would you like to be contacted?",
        ("View Flights", "🔥Special Offers", "🎟️Purchased Tickets"))
        if option=='View Flights':
            st.table(flight_overview())
        elif option=="🔥Special Offers":
            st.markdown('spcial offer')
        elif option=="🎟️Purchased Tickets":
            st.markdown('pruchase tickets')


if __name__ == "__main__":
    main()





