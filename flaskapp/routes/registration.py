"""
This module contains registration method which handles user registration
and send otp using send_gmail method

This module also contains helping methods check_verify and delete_user_by_id

"""

import os
import random
import threading
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from flaskapp.config import con_mongodb
from flaskapp.utils import send_gmail

load_dotenv()

myClient = con_mongodb.con()
myCol = myClient['users']

#route to register user and send otp
def registration():
    """
    This method is to handle user registration and send email for otp
    """
    try:
        # Get the JSON data
        _json = request.json
        name = _json.get('name')
        username = _json.get('username')
        email = _json.get('email')
        password = _json.get('password')

        # Validate the JSON data
        errors = []

        if not name:
            errors.append('Name is required')

        if not username:
            errors.append('Username is required')

        if '@' in username:
            errors.append('Username cannot contain "@"')

        if not email:
            errors.append('Email is required')

        if not password:
            errors.append('Password is required')

        if len(password) < 8:
            errors.append('Password must be at least 8 characters')

        # If there are errors, return them in the response
        if errors:
            return jsonify({'errors': errors, 'status': False}), 400

        # Check if the user already exists
        try:
            query1 = {'email': email}
            existing_email = myCol.find_one(query1)
            if existing_email:
                resp = jsonify({'message': 'email already existing', 'status': False}), 400
                return resp
        except (ValueError, TypeError) as e:
            # Handle multiple exceptions
            resp = jsonify(f"Exception: {e} email")
            return resp
        try:
            query2 = {'username': username}
            existing_username = myCol.find_one(query2)
            if existing_username:
                resp = jsonify({'message': 'Username already existing', 'status': False}), 400
                return resp
        except (ValueError, TypeError) as e:
            # Handle multiple exceptions
            resp = jsonify(f"Exception: {e} username")
            return resp

        # Send the OTP to the user's email
        sender_email = os.getenv("sender_email")
        mailpassword = os.getenv("email_password")
        otp = random.randint(1000, 10000)
        html = f"""<html>
        <head></head>
<body>
    <div style="font-family: Helvetica,Arial,sans-serif;
    min-width:1000px;overflow:auto;line-height:2">
        <div style="margin:50px auto;width:70%;padding:20px 0">
          <div style="border-bottom:1px solid #eee">
            <a href="" style="font-size:1.4em;
            color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
          </div>
          <p style="font-size:1.1em">Hi,</p>
          <p>Thank you for choosing Your Brand. 
          Use the following OTP to complete your Sign Up procedures.
            OTP is valid for 5 minutes</p>
          <h2 style="background: #00466a;margin: 0 auto;
          width: max-content;padding: 0 10px;color: #fff;
          border-radius: 4px;">{otp}</h2>
          <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
          <hr style="border:none;border-top:1px solid #eee" />
          <div style="float:right;padding:8px 0;
          color:#aaa;font-size:0.8em;
          line-height:1;font-weight:300">
            <p>Your Brand Inc</p>
            <p>1600 Amphitheatre Parkway</p>
            <p>California</p>
          </div>
        </div>
      </div>
</body>
        
        </html>""".format(otp=otp)

        send = send_gmail.send_otp_email(sender_email, mailpassword, email, html,
                                          "OTP Verification")
        if send:
            hash_password = generate_password_hash(password)
            count_doc = myCol.count_documents({})

            #Check if Id is already present in db
            is_id = True
            while is_id:
                if not myCol.find_one({'_id': count_doc}):
                    is_id = False
                else:
                    is_id = True
                    count_doc = count_doc + 1

            #Insert the user data into the database
            myCol.insert_one({"_id": count_doc, "name": name, "username": username ,
                              "email": email, "password": hash_password,"otp": otp,
                                "isEmailVerify": False})

            #Start the timer thread to check the OTP verification
            if timer_thread is not None:
                stop_timer()
            start_timer(count_doc)
            resp =  jsonify({'message': 'OTP sent successfully! ', "status": True}), 200
            return resp
        else:
            return jsonify({'message': 'Failed to send OTP', "status": False}), 400

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp

def check_verify(count_doc, _):
    """
    This method check after 5 min when user register, is user verify their email or not
    """
    user = myCol.find_one({'_id': count_doc})
    if user['isEmailVerify']:
        pass
    elif not user['isEmailVerify']:
        delete_user_by_id(count_doc)


#delete user by delete method
def delete_user_by_id(count_doc):
    """
    This method is used by check_verify method to delete 
    the user which is not verify their email after 5 min of registration
    """
    if myCol.find_one({'_id': count_doc}):
        # Delete the user with the custom ID
        myCol.delete_one({'_id': count_doc})
    else:
        pass

timer_thread = None

def start_timer(count_doc):
    """
    This method is to start the timer thread to check the verify the email
    """
    global timer_thread
    timer_thread = threading.Timer(60.0, check_verify, args=(count_doc, None))
    timer_thread.start()

def stop_timer():
    """
    This method is to stop the timer thread
    """
    global timer_thread
    if timer_thread is not None:
        timer_thread.cancel()
        timer_thread = None

def resend_otp():
    """
    This method is to resend otp in case of user not get the otp
    """
    try:
        _json = request.json
        email = _json.get('email')
        user = myCol.find_one({'email': email})
        if user and not user['isEmailVerify']:
            sender_email = os.getenv("sender_email")
            mailpassword = os.getenv("email_password")
            otp = random.randint(1000, 10000)

            filter_criteria = {"_id": user['_id']}
            update_query = {"$set": {"otp": otp}}
            myCol.update_one(filter_criteria, update_query)

            html = f"""<html>
        <head></head>
<body>
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
        <div style="margin:50px auto;width:70%;padding:20px 0">
          <div style="border-bottom:1px solid #eee">
            <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
          </div>
          <p style="font-size:1.1em">Hi,</p>
          <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
          <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
          <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
          <hr style="border:none;border-top:1px solid #eee" />
          <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
            <p>Your Brand Inc</p>
            <p>1600 Amphitheatre Parkway</p>
            <p>California</p>
          </div>
        </div>
      </div>
</body>
        
        </html>""".format(otp=otp)

            send = send_gmail.send_otp_email(sender_email, mailpassword, email, html,
                                              "OTP Verification")
            if send:
                stop_timer()
                start_timer(user['_id'])
                resp =  jsonify({'message': 'OTP sent successfully! ', "status": True}), 200
                return resp
            else:
                return jsonify({'message': 'Failed to send OTP', "status": False}), 400

        else:
            resp = jsonify({"message": 'Authentication failed (user not found)', "status": False})
            resp.status_code = 200
            return resp

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
