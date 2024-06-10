from flask import request, jsonify
from flaskapp.config import con_mongodb
from flaskapp.utils import generate_authtoken
import os

securityKey = os.getenv('SECURITY_KEY')

myClient = con_mongodb.con()
myCol = myClient['users']

#route for virefy otp
def verifyOtp():
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
                id = user['_id']
                authToken = generate_authtoken.generate_token(id,securityKey,None)
                data = {
                        "authToken": authToken,
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
            
    except:
        resp = jsonify({"message": 'Authentication failed (user not found)', "status": False})
        resp.status_code = 200
        return resp