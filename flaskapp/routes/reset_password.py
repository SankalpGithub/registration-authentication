"""
This module contains verify_reset_pass and reset_password to reset the 
password of user in case user forgot their password
"""

import os
import random
import threading
from werkzeug.security import generate_password_hash
from flask import request, jsonify, render_template
from flaskapp.utils import generate_authtoken, send_gmail
from flaskapp.config import con_mongodb


securityKey = os.getenv("SECURITY_KEY")

timer_thread = None

myClient = con_mongodb.con()
myCol = myClient['users']

#route to reset password
def reset_user_password():
    """
    This method reset the password by changing password in database
    """
    try:
        data = request.args.get('token')
        token = data[:-4]
        verify_link_code = int(data[-4:])
        requet_data = generate_authtoken.decode_token(token,securityKey)
        _id = requet_data['id']
        password = requet_data['password']
        user = myCol.find_one({'_id': _id})
        is_email_verify = user['isEmailVerify']
        query = {"_id": _id, "verify_link_code": {'$exists': True}}
        is_verify_link_code =  myCol.find_one(query) is not None
        if is_verify_link_code:
            if verify_link_code == user["verify_link_code"]:
                if user and is_email_verify:
                    hash_password = generate_password_hash(password)
                    filter_criteria = {"_id": _id}
                    update_query = {"$unset": {"verify_link_code": 1},
                        "$set": {"password": hash_password}}
                    myCol.update_one(filter_criteria, update_query)
                    global timer_thread
                    if timer_thread is not None:
                        timer_thread.cancel()
                        timer_thread = None
                    return jsonify({"message": "password reset"})
                else:
                    return jsonify({'message': 'something wents wrong', 'status': False})
            else:
                return jsonify({"message": "The link you are trying to access has expired."})
        else:
            return jsonify({"message": "The link you are trying to access has expired."})

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}"),404
        return resp

#route for verify the email for reset password
def verify_reset_pass():
    """
    This method verify and send the email to check user for reset password
    """
    try:
        _json = request.json
        email = _json.get('email')
        password = _json.get('password')
        user = myCol.find_one({'email': email})
        if user and user['isEmailVerify']:
            token = generate_authtoken.generate_token(user['_id'],securityKey,password)
            verify_link_code = random.randint(1000,9999)
            filter_criteria = {"_id": user['_id']}
            update_query = {"$set": {"verify_link_code": verify_link_code}}
            myCol.update_one(filter_criteria, update_query)
            sender_email = os.getenv("sender_email")
            gmailpassword = os.getenv("email_password")
            recipient_email = email
            subject = 'Reset password'
            body = f'Click 127.0.0.1:5000/reset_user_password?token={token+str(verify_link_code)} to reset password.'
            send = send_gmail.send_otp_email(sender_email, gmailpassword, recipient_email,
                                              body, subject)
            if send:
                global timer_thread
                if timer_thread is not None:
                    timer_thread.cancel()
                    timer_thread = None
                timer_thread = threading.Timer(300.0, check_verify, args=(user["_id"], None))
                timer_thread.start()
                resp = jsonify({'message': 'Link sent successfully', "status": True})
                resp.status_code = 200
                return resp
            else:
                return jsonify({'message': 'Failed to send Link', "status": False}), 404
        else:
            return jsonify({'message': 'User not found'})

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}"),404
        return resp
    
def check_verify(_id,_):
    query = {"_id": _id, "verify_link_code": {'$exists': True}}
    is_verify_link_code =  myCol.find_one(query) is not None
    if is_verify_link_code:
        filter_query = {"_id": _id}
        update_query = {"$unset": {"verify_link_code": 1}}
        myCol.update_one(filter_query,update_query)
    else:
        pass
    
    