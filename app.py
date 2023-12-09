import streamlit as st 
import streamlit.components.v1 as com
import os
import datetime
import pandas as pd
import numpy as np
from app_modules.utils import * 

# Header 
com.iframe("https://lottie.host/embed/b488bb3a-4c39-432e-8e11-ea0692d35560/XdNwCxlslm.json", height= 200)
st.title("Airlines Booking System")

    
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    menu = ["🔐 Login", "📝 Signup", "❓ Reset Password"]
    choice = st.sidebar.selectbox("Menu", menu)

    with st.sidebar:
        if choice == "📝 Signup":
            create_account()

        elif choice == '🔐 Login':
            user_login()
        elif choice == '❓ Reset Password':
                forgot()
   
    if st.session_state['logged_in']: 

        st.markdown(f"Welcome Back {st.session_state['username']} !")

        option = st.selectbox(
        "Select an option:",
        ("🔍 View Flights", "🔥 Special Offers", "🎟️ Purchased Tickets", "📑 Refund Requests"))
        
        st.divider()

        if option=='🔍 View Flights':
            flight_overview()

        elif option=="🔥 Special Offers":
            special_offers()

        elif option=="🎟️ Purchased Tickets":
            orders()

        else: 
            refund_tickets()
            
    elif not st.session_state['logged_in']: 
        st.markdown('Please login with the sidebar to continue')


if __name__ == "__main__":
    main()





