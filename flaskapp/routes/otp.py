"""
This module contain all task regarding to otp handling
it verify otp and resend otp using the methods veriyf_otp
and resend_otp respectively
"""

import os
from flask import request, jsonify
from flaskapp.config import con_mongodb
from flaskapp.utils import generate_authtoken

securityKey = os.getenv('SECURITY_KEY')

myClient = con_mongodb.con()
myCol = myClient['users']

#route for virefy otp
def verify_otp():
    """
    This method verify the otp we generated and otp given by user to verify it's email
    """
    try:
        _json = request.json
        email = _json.get('email')
        user_otp = _json.get('user_otp')
        user = myCol.find_one({'email': email})

        if not user['isEmailVerify']:
            if user['otp'] == user_otp:
                filter_criteria = {"_id": user['_id']}
                update_query = {"$unset": {"otp": 1},
                                "$set": {"isEmailVerify": True}}
                myCol.update_one(filter_criteria, update_query)
                _id = user['_id']
                auth_token = generate_authtoken.generate_token(_id,securityKey,None)
                data ={
                        "authToken": auth_token,
                        "status": True
                        }

                resp = jsonify(data)
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'message': 'OTP incorrect', "status": False})
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'User already verified', "status": False})
            resp.status_code = 200
            return resp

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
