"""
This module contains Login method which handles authenticatin part of user
"""

import os
from flask import request, jsonify
from werkzeug.security import check_password_hash
from flaskapp.config import con_mongodb
from flaskapp.utils import generate_authtoken

securityKey = os.getenv('SECURITY_KEY')

myClient = con_mongodb.con()
myCol = myClient['users']

#rout for authenticating a user
def login():
    """
    This method is to handle user authentication and send auth token for user 
    """
    try:
        _json = request.json
        email_or_username = _json.get('data')
        password = _json.get('password')

        if '@' in email_or_username:
            user = myCol.find_one({'email': email_or_username})
        else:
            user = myCol.find_one({'username': email_or_username})

        is_email_verify = user['isEmailVerify']

        if user:
            if is_email_verify:
                if check_password_hash(user['password'], password):
                    _id = user['_id']
                    auth_token = generate_authtoken.generate_token(_id,securityKey,None)
                    data = {
                        "authToken": auth_token,
                        'status': True
                    }
                    resp = jsonify(data)
                    resp.status_code = 200
                    return resp
                else:
                    resp = jsonify({'message': 'Authentication failed (incorrect password)',
                                     "status": False})
                    resp.status_code = 200
                    return resp

            elif not is_email_verify:
                resp = jsonify({'message': 'Authentication failed (user is not verified)',
                                 "status": False})
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'Authentication failed (user not found)', "status": False})
            resp.status_code = 200
            return resp

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
