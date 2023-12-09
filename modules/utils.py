import os 
import sys 
sys.path.append('../')
from config import * 
import pymysql 
import pandas as pd 

# Creating SQL Connector 
connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             db=db,
                             charset='utf8mb4')

cursor = connection.cursor()

def transform(cursor):
     columns = [d[0] for d in cursor.description]
     result = [dict(zip(columns, row)) for row in cursor.fetchall()]
     return result 

# Function for user login 
def login(username, password):
    # naive error handling 
    try:
        cursor.execute("""SELECT User_ID FROM Users WHERE User_Name='{}' AND Password = '{}' """.format(username, password))
        result = transform(cursor)
    except: 
        result = []
    return result

# Function to record last_login
def last_login(user_id):
    try:
        cursor.execute("""
                UPDATE users
                SET Last_Login = CURRENT_TIMESTAMP
                WHERE User_ID = {};""".format(user_id))
        connection.commit()
    except:
        pass
   

# Function for users to create an account 
def create_account(username, password, email=None):
    try:
        cursor.execute(""" INSERT INTO users (User_Name, Creation_Date, Last_Login, Password, Email)\
                VALUES ('{}',CURRENT_TIMESTAMP,NULL,'{}','{}');
                """.format(username,password,email))
        connection.commit()
        result = True
    except: 
        result = False

    return result 


# Function for users to reset password 
def reset_password(username, email, password): 
    try:
        _result = cursor.execute("""SELECT User_ID FROM Users WHERE User_Name='{}' AND Email = '{}' """.format(username, email))
        user_id = transform(cursor)[0].get('User_ID')
    except: 
        _result = 0

    if _result > 0: 
        cursor.execute("""UPDATE users
            SET Password = '{}'
            WHERE User_ID = {}
                """.format(password, user_id))
        connection.commit()
        result = True
    
    return result
    

# Function to show all avaliable origin
def origin(): 
    try: 
        cursor.execute("SELECT DISTINCT Departure_City FROM flights")
        result = transform(cursor)
    except:
        result = []
    return result

# Function to show avaliable destinations 
def destinations(selected_origin): 
    try: 
        cursor.execute("""SELECT DISTINCT Arrival_City FROM flights 
                       WHERE Departure_City = '{}'
                       """.format(selected_origin))
        result = transform(cursor)
    except:
        result = []
    return result

def flight_companies(selected_origin,selected_destination):
    # cursor = connection.cursor()
    try: 
        cursor.execute("""SELECT DISTINCT Flight_Company FROM flights
                       WHERE Departure_City = '{}'
                       AND
                       Arrival_City = '{}'
                       """.format(selected_origin, selected_destination))
        result = transform(cursor)
    except:
        result = []
    return result

# Function for user to buy a ticket 
def flight_search(selected_origin, selected_destination, selected_company, start_date, end_date):
    try: 
        cursor.execute("""SELECT * FROM flights
                       WHERE Departure_City = '{}' AND Arrival_City = '{}'
                       AND Flight_Company = '{}' AND
                       Departure_Date BETWEEN '{}' AND '{}'
                       """.format(selected_origin,
                                   selected_destination, 
                                   selected_company, 
                                   start_date,
                                   end_date))
        result = transform(cursor)
    except:
        result = []
    
    return result


# Function to check if seats are avaliable 
def check_flights(flight_id):
    try: 
        cursor.execute("""SELECT Available_Seats FROM flights WHERE
                       Flight_ID = {}
                       """.format(flight_id))
        query_result = transform(cursor)
        result = query_result[0].get('Available_Seats') > 0

    except:
       result = False 
    
    return result

# function for user to purchase a ticket 
def purchase_ticket(flight_id, userid, reference_number ): 
    try:
        
        # Available Seats - 1 
        cursor.execute("""UPDATE flights
            SET Available_Seats = (Available_Seats - 1)
            WHERE Flight_ID = {0}""".format(flight_id))
        
        # Purchased tickets + 1 
        cursor.execute("""
                INSERT INTO orders (Flight_ID, User_ID, Reference_Number, Order_Date)
                VALUES({0},{1},'{2}',CURRENT_TIMESTAMP);""".format(flight_id, userid, reference_number))
        connection.commit()

        result = True
    except: 
        result = False 
    
    return result


# Function to show all tickets purchased by user 
def orders(user_id): 
    try: 
        cursor.execute("""SELECT Reference_Number, Order_Date, Flight_ID, Departure_City, 
                       Arrival_City, Departure_Date FROM orders
                       JOIN flights USING(Flight_ID)
                       WHERE User_ID = '{}'
                       """.format(user_id))
        result = transform(cursor)
    except:
        result = []
    return result

# Function to show all special offers
def special_offers(): 
    try: 
        cursor.execute("""SELECT Flight_ID, Departure_City, Arrival_City,
                       Departure_Date, Promotion 
                       FROM special_offers
                       JOIN flights USING(Flight_ID);""")
        result = transform(cursor)
    except:
        result = []
    return result

# Function for ticket refunds
def refunds(ticket_id, reference_number, reason):
    try:
        cursor.execute(""" INSERT INTO refunds\
                VALUES ('{}','{}','{}',CURRENT_TIMESTAMP);
                """.format(reference_number,ticket_id,reason))
        connection.commit()
        result = True
    except: 
        result = False

    return result 

# Function to show all refund requests
def refund_tickets(user_id):
    try:
        cursor.execute("""SELECT Reference_Number, Creation_Date, Flight_ID, 
                       Remarks FROM flights.refunds
                       JOIN orders USING(Reference_Number)
                       WHERE User_ID = {};
                """.format(user_id))
        result = transform(cursor)
    except: 
        result = []

    return result