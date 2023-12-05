import streamlit as st
import datetime
import pandas as pd
from PIL import Image


#初始化session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# image = Image.open('C:/Users/ywy28/Downloads/images/sample.jpg')
# st.image(image, width=400)

# 基本页面结构
def main():
    st.title("Airline Booking System")
    menu = ["🏠Home", "🔐Login", "📝Signup", "✈️View Flights", "🔥Special Offers", "🎟️Purchased Tickets"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "🏠Home":
        st.subheader("Welcome to Our Airline Booking System")

    elif choice == "🔐Login":
        user_login()

    elif choice == "📝Signup":
        create_account()

    # 登录后才能访问的部分
    if st.session_state['logged_in']:
        if choice == "✈️View Flights":
            view_flights()
        elif choice == "🔥Special Offers":
            special_offers()
        elif choice == "🎟️Purchased Tickets":
            purchased_tickets()
    else:
        if choice not in ["🏠Home", "🔐Login", "📝Signup"]:
            st.warning("Please login to access this feature.")

# 用户注册
def create_account():
    with st.form("Create Account", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        submit_button = st.form_submit_button("Create")

        if submit_button:
            if password == confirm_password:
                # 创建账户逻辑


                st.success("Account Created Successfully!")
            else:
                st.error("Account Creation Error")

# 用户登录by Username,Password
def user_login():
    with st.form("Login", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

        if submit_button:
            # 假设用户1,密码1
            if username == "1" and password == "1":  
                st.session_state['logged_in'] = True
                st.success("Logged In Successfully!")
            else:
                st.error("Invalid username or password")

# 查看航班by Origin,Destination,Date
def view_flights():
    st.subheader("View and Check Available Flights")

    # 初始化session state
    if 'search_results' not in st.session_state:
        st.session_state['search_results'] = None
    if 'selected_index' not in st.session_state:
        st.session_state['selected_index'] = None
    if 'action' not in st.session_state:
        st.session_state['action'] = None

    # 搜索航班
    with st.form("Flight Search"):
        origin = st.selectbox("Origin", ["Hongkong", "Mainland"])
        destination = st.selectbox("Destination", ["Hongkong", "Mainland"])
        date = st.date_input("Date")
        submit_button = st.form_submit_button("Search Flights")

    if submit_button:
        flights_data = [
            {"flight_id": "flight_id", "origin": origin, "destination": destination, "date": str(date), "price": "price"},
        ]
        st.session_state['search_results'] = pd.DataFrame(flights_data)

    if st.session_state['search_results'] is not None:
        st.write("Available Flights:")
        st.dataframe(st.session_state['search_results'])
        st.session_state['selected_index'] = st.selectbox("Select a Flight", st.session_state['search_results'].index)

    #购买或者预订
    if st.session_state['selected_index'] is not None:
        st.session_state['action'] = st.radio("Choose an action:", ["Purchase Ticket", "Reserve Ticket"])

    if st.session_state['action'] == "Purchase Ticket":
        if st.button("Confirm Purchase"):
            # 购票逻辑

            selected_flight = st.session_state['search_results'].iloc[st.session_state['selected_index']]
            st.success(f"Ticket for Flight ID {selected_flight['flight_id']} Purchased Successfully!")
            # 返回初始状态
            st.session_state['search_results'] = None
            st.session_state['selected_index'] = None
            st.session_state['action'] = None

    elif st.session_state['action'] == "Reserve Ticket":
        if st.button("Confirm Reservation"):
            # 预订逻辑

            selected_flight = st.session_state['search_results'].iloc[st.session_state['selected_index']]
            st.success(f"Ticket for Flight ID {selected_flight['flight_id']} Reserved Successfully!")
            # 返回初始状态
            st.session_state['search_results'] = None
            st.session_state['selected_index'] = None
            st.session_state['action'] = None

# 优惠
def special_offers():
    #优惠逻辑

    st.subheader("Special Offers")
    offer_end_date = datetime.datetime(2023, 12, 31)
    current_date = datetime.datetime.now()
    days_left = (offer_end_date - current_date).days
    st.write(f"🔥🔥🔥 Hurry up! Only {days_left} days left for these amazing deals!")
    

# 退票和客户支持
def purchased_tickets():
    #查询已购票

    st.subheader("Your Purchased Tickets")
    user_tickets = [{"ticket_id": " ", "flight_id": " ", "date": " "}]
    

    for ticket in user_tickets:
        with st.expander(f"Ticket ID: {ticket['ticket_id']} - Flight ID: {ticket['flight_id']}"):
            st.write(f"Flight Date: {ticket['date']}")
            # 退票按钮
            if st.button("Refund Ticket", key=f"refund_{ticket['ticket_id']}"):
                # 添加退票逻辑

                st.success(f"Ticket {ticket['ticket_id']} Refunded Successfully!")

            # 客户支持
            with st.form(f"support_{ticket['ticket_id']}"):
                message = st.text_area("Message for Customer Support", key=f"message_{ticket['ticket_id']}")
                send_button = st.form_submit_button("Send to Customer Support")
                if send_button:
                    #客户支持
                    st.success(f"Message sent for Ticket {ticket['ticket_id']}")

#登出
def logout():
    st.session_state['logged_in'] = False
    st.write("You have been logged out.")


if st.session_state['logged_in']:
    if st.sidebar.button('Logout'):
        logout()


if __name__ == '__main__':
    main()
