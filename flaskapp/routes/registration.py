from flask import request, jsonify
import random
from werkzeug.security import generate_password_hash
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

            html = """<html>
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
            
            send = send_gmail.send_otp_email(sender_email, mailpassword, email, html, "OTP Verification")

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
    
def checkVerify(id,arg2):
    user = myCol.find_one({'_id': id})
    if user['isEmailVerify']:
        pass
    elif not user['isEmailVerify']:
        print(deleteUserbyId(id))


#delete user by delete method
def deleteUserbyId(id):
    try:
        if myCol.find_one({'_id': id}):
            # Delete the user with the custom ID
            myCol.delete_one({'_id': id})
            resp = jsonify({'message': 'User deleted successfully', 'status': True})
            resp.status_code = 200
            return resp
        else:
            pass # return jsonify({'message': 'User not found', 'status': False}),404

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
