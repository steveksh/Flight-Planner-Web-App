from flask import Flask
from flask import request
from flask import jsonify
from modules.utils import * 
import pandas as pd 

app = Flask(__name__)

# End points for logging in 
@app.route('/login', methods=["POST"])
def user():
    if request.method == "POST": 
        username = request.json.get('username')
        password = request.json.get('password')
        response = login(username, password)

        # updating the last login column as well 
        if len(response)>0:
            last_login(response[0].get('User_ID'))
            
        return jsonify(response)
    
# End point for getting all origin 
@app.route('/departure', methods=["GET"])
def departure():
    if request.method == "GET":
        response = origin()
        return jsonify(response)

# End point for getting all destination
@app.route('/destination', methods=["POST"])
def destination():
    if request.method == "POST":
        selected_origin = request.json.get('selected_origin')
        response = destinations(selected_origin)
        return jsonify(response)
    
# End point for getting all company names 
@app.route('/companies', methods=["POST"])
def companies():
    if request.method == "POST":
        selected_origin = request.json.get('selected_origin')
        selected_destination = request.json.get('selected_destination')
        response = flight_companies(selected_origin ,selected_destination)
        return jsonify(response)
    
# End point for search results
@app.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        # selected_origin, selected_destination, selected_company, start_date, end_date
        selected_origin = request.json.get('selected_origin')
        selected_destination = request.json.get('selected_destination')
        selected_company = request.json.get('selected_company')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')

        response = flight_search(selected_origin, 
                                 selected_destination, 
                                 selected_company, 
                                 start_date, 
                                 end_date)
        return jsonify(response)
    
# End point for creating a new account 
@app.route('/create', methods = ['PUT'])
def create():
    if request.method == 'PUT':
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        result = create_account(username, password, email)
    if result: 
        response = {'status': 200}
    elif not result: 
        response = {'status': 500}
    
    return jsonify(response)

# End point for resetting the password
@app.route('/reset_password', methods = ['PUT'])
def reset():
    result = None
    if request.method == 'PUT':
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        result = reset_password(username, email, password)
    if result: 
        response = {'status': 200}
    elif not result: 
        response = {'status': 500}

    return jsonify(response)

# End point for ensuring there are seats for purchase 
@app.route('/purchase', methods = ['PUT'])
def purchase():
    result = None
    if request.method == 'PUT':
        flight_id = request.json.get('flight_id')
        user_id = request.json.get('user_id')
        reference_number = request.json.get('reference_number')
        result = check_flights(flight_id)

        if result: 
            try: 
                purchase_ticket(flight_id, user_id, reference_number)
                response = {'status': 200}
            except: 
                response = {'status', 500} 

        elif not result: 
            response = {'status': 500}

        return jsonify(response)

# End point showing all purchase tickets 
@app.route('/purchased_tickets', methods = ['POST'])
def purchased_tickets():
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        response = orders(user_id)

        return jsonify(response)

# End point showing all purchase tickets 
@app.route('/offers', methods = ['GET'])
def offers():
    if request.method == 'GET':
        response = special_offers()
        return jsonify(response)
    
# end point allowing refunds 
@app.route('/refund', methods = ['PUT'])
def refund():
    if request.method == 'PUT':
        ticket_id = request.json.get('ticket_id')
        reference_number = request.json.get('reference_number')
        reason = request.json.get('reason')
        result = refunds(ticket_id, reference_number, reason)
    if result: 
        response = {'status': 200}
    elif not result: 
        response = {'status': 500}
    
    return jsonify(response)

# End point showing all refund tickets 
@app.route('/refund_view', methods = ['POST'])
def refund_view():
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        response = refund_tickets(user_id)

    return jsonify(response)
    
if __name__ == "__main__":
    app.run(debug=True)