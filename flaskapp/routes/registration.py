from flask import Flask, request, jsonify
import random
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flaskapp.config import con_mongodb
from flaskapp.utils import send_gmail
import os
import threading

load_dotenv()

myClient = con_mongodb.con()
myCol = myClient['users']

#route to register user and send otp
def registration():
    try:

        # Get the JSON data
        _json = request.json
        name = _json.get('name')
        username = _json.get('username')
        email = _json.get('email')
        password = _json.get('password')

        # Validate the JSON data
        if not name:
            return jsonify({'error': 'Name is required', 'status': False}), 400
        if not username:    
            return jsonify({'error': 'Username is required', 'status': False}), 400
        if not email:
            return jsonify({'error': 'Email is required', 'status': False}), 400
        if not password:
            return jsonify({'error': 'Password is required', 'status': False}), 400
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters', 'status': False}), 400
        
        # Check if the user already exists
        try:
            query1 = {'email': email}
            existing_email = myCol.find_one(query1)
            if existing_email:
                resp = jsonify({'message': 'email already existing', 'status': False}), 400
                return resp
        except (ValueError, TypeError) as e:
            # Handle multiple exceptions
            resp = jsonify(f"Exception: {e}")
            return resp
        
        try:
            query2 = {'username': username}
            existing_username = myCol.find_one(query2)
            if existing_username:
                resp = jsonify({'message': 'Username already existing', 'status': False}), 400
                return resp
        except (ValueError, TypeError) as e:
            # Handle multiple exceptions
            resp = jsonify(f"Exception: {e}")
            return resp
        
        # Send the OTP to the user's email
        else:
            sender_email = os.getenv("sender_email")
            mailpassword = os.getenv("email_password")
            otp = random.randint(1000, 10000)

            send = send_gmail.send_otp_email(sender_email, mailpassword, email, otp)

            if send:
                hash_password = generate_password_hash(password)
                countD = myCol.count_documents({})
                
                #Check if Id is already present in db
                isId = True
                while isId:
                    if not myCol.find_one({'_id': countD}):
                        isId = False
                    else:
                        isId = True
                        countD = countD + 1
                        
                #Insert the user data into the database
                myCol.insert_one({"_id": countD, "name": name, "username": username ,"email": email, "password": hash_password, "otp": otp, "isEmailVerify": False})

                #Start the timer thread to check the OTP verification
                timer_thread = threading.Timer(300.00,checkVerify,args=(countD,None))
                timer_thread.start()

                resp =  jsonify({'message': 'OTP sent successfully! ', "status": True}), 200
                return resp
            else:
                return jsonify({'message': 'Failed to send OTP', "status": False}), 400
            
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def checkVerify():
    pass