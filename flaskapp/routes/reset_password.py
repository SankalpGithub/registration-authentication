"""
This module contains verify_reset_pass and reset_password to reset the 
password of user in case user forgot their password
"""

import os
from werkzeug.security import generate_password_hash
from flask import request, jsonify, render_template
from flaskapp.utils import generate_authtoken, send_gmail
from flaskapp.config import con_mongodb


securityKey = os.getenv("SECURITY_KEY")

myClient = con_mongodb.con()
myCol = myClient['users']

#route to reset password
def reset_user_password():
    """
    This method reset the password by changing password in database
    """
    try:
        token = request.args.get('token')
        data= generate_authtoken.decode_token(token,securityKey)
        _id = data['id']
        password = data['password']
        user = myCol.find_one({'_id': id})
        is_email_verify = user['isEmailVerify']
        if user and is_email_verify:
            hash_password = generate_password_hash(password)
            filter_criteria = {"_id": _id}
            update_query = {"$set": {"password": hash_password}}
            myCol.update_one(filter_criteria, update_query)
            return render_template('resetpass.html')
        else:
            return jsonify({'message': 'something wents wrong', 'status': False})

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
            sender_email = os.getenv("sender_email")
            gmailpassword = os.getenv("email_password")
            recipient_email = email
            subject = 'Reset password'
            body = f'Click 127.0.0.1:5000/reset_user_password?token={token} to reset password.'
            send = send_gmail.send_otp_email(sender_email, gmailpassword, recipient_email,
                                              body, subject)
            if send:
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
    