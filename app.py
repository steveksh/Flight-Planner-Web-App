import streamlit as st 
import streamlit.components.v1 as com
import os
import datetime
import pandas as pd
import numpy as np
from app_modules.utils import * 

# Header 
com.iframe("https://lottie.host/embed/311343e9-b00f-4086-ba19-aa20105a6130/oC9vA7oZDd.json", height= 200)
st.title("Welcome to Our Airline Booking System")

def title():
     st.write(
        f"""
        Welcome! Please login to continue 
        """)
    
def main():
    login = False
    if not login: 
        title()
       
    menu = ["🔐 Login", "📝 Signup"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "📝 Signup":
        with st.sidebar:
            create_account()

    elif choice == '🔐 Login':
        with st.sidebar:
            login = user_login()
   
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





