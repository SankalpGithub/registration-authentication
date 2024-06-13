
"""
This module defines all the routes for the Flask web application.

Each route is associated with a specific URL endpoint and HTTP method, and 
maps to a view function that handles the logic for processing requests and 
generating responses. 

"""

#imports
import os
from flask import Flask
from flaskapp.routes import otp, registration, authentication, reset_password

#flask app instance
app = Flask(__name__)

#flask app configuration
securityKey = os.getenv('SECURITY_KEY')
app.config['SECURETY_KEY'] = securityKey

#registration route
@app.route('/registration', methods=['POST'])
def register():
    """
    This method is assign to registration route to handle user registration
    """
    return registration.registration()

#verify otp route
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    """
    This method is assign to verify otp route which will verify the otp from user
    """
    return otp.verify_otp()

#login route
@app.route('/login', methods=['POST'])
def login():
    """
    This method is assign to login route to handle user authenticatiton
    """
    return authentication.login()

#resetpassword route
@app.route('/verify_reset_pass', methods=['POST'])
def verify_reset_pass():
    """
    This method is assgin to verify_reset_pass route to verify the user which make the request
    """
    return reset_password.verify_reset_pass()

#verify_reset_pass route
@app.route('/reset_user_password', methods=['GET'])
def reset_user_password():
    """
    This method is assign to verify_reset_password route to reset the user
    password in case user forgot the password
    """
    return reset_password.reset_user_password()

@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    """
    This method is assgin to resend_otp route to resend the otp in case otp failed to send
    """
    return registration.resend_otp()

if __name__ == '__main__':
    app.run(debug=True)
