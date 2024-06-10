from flask import request, jsonify
from werkzeug.security import check_password_hash
from flaskapp.config import con_mongodb
from flaskapp.utils import generate_authtoken
import os

securityKey = os.getenv('SECURITY_KEY')

myClient = con_mongodb.con()
myCol = myClient['users']

#rout for authenticating a user
def login():
    try:
        _json = request.json
        email = _json.get('email')
        password = _json.get('password')
        user = myCol.find_one({'email': email})
        isEmailVerify = user['isEmailVerify']
        if user:
            if isEmailVerify:
                if check_password_hash(user['password'], password):
                    id = user['_id']
                    authToken = generate_authtoken.generate_token(id,securityKey,None)
                    data = {
                        "authToken": authToken,
                        'status': True
                    }
                    resp = jsonify(data)
                    resp.status_code = 200
                    return resp
                else: 
                    resp = jsonify({'message': 'Authentication failed (incorrect password)', "status": False})
                    resp.status_code = 200
                    return resp
            elif not isEmailVerify:
                resp = jsonify({'message': 'Authentication failed (user is not verified)', "status": False})
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'Authentication failed (user not found)', "status": False})
            resp.status_code = 200
            return resp
    except:
        resp = jsonify({"message": 'Authentication failed (user not found)', "status": False})
        resp.status_code = 200
        return resp
