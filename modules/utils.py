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

def transform(cursor):
     columns = [d[0] for d in cursor.description]
     result = [dict(zip(columns, row)) for row in cursor.fetchall()]
     return result 

# Function for user login 
def login(username, password):
    cursor = connection.cursor()
    # naive error handling 
    try:
        cursor.execute("""SELECT User_ID FROM Users WHERE User_Name='{}' AND Password = '{}' """.format(username, password))
        result = transform(cursor)
    except: 
        result = []
    return result

# Function to record last_login
def last_login(user_id):
    cursor = connection.cursor()    
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
    cursor = connection.cursor()
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
    cursor = connection.cursor()
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
    

# Function for users 
def all_flights():
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT * FROM flights")
        result = transform(cursor)
    except:
        result = []
    return result

# Function to show all avaliable origin
def origin(): 
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT DISTINCT Departure_City FROM flights")
        result = transform(cursor)
    except:
        result = []
    return result

# Function to show avaliable destinations 
def destination(): 
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT DISTINCT Arrival_City FROM flights")
        result = transform(cursor)
    except:
        result = []
    return result

def flight_company():
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT DISTINCT Flight_Company FROM flights")
        result = transform(cursor)
    except:
        result = []
    return result

# Function for user to buy a ticket 
def flight_search():
    cursor = connection.cursor()
    try: 
        cursor.execute(""""SELECT * FROM flights
                       WHERE""")
        result = transform(cursor)
    except:
        result = []
    return result

# Function to show the tickets currently owned by the user 
# uuid need reference 


