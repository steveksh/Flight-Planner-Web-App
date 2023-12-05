from flask import Flask
from flask import request
from flask import jsonify
from modules.utils import * 

app = Flask(__name__)

# End points for logging in 
@app.route('/login', methods=["POST"])
def user():
    if request.method == "POST": 
        username = request.json.get('username')
        password = request.json.get('password')
        response = login(username, password)

        if len(response)>0:
            last_login(response[0].get('User_ID'))
            
        return jsonify(response)
    
# End point for checking avaliable flights 
@app.route('/overview', methods=["GET"])
def overview():
    if request.method == "GET":
        response = all_flights()
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


if __name__ == "__main__":
    app.run()