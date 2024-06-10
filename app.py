from flask import Flask, request, jsonify, render_template
from flaskapp.routes import registration, verify_otp, authentication
import os

app = Flask(__name__)

securityKey = os.getenv('SECURITY_KEY')
app.config['SECURETY_KEY'] = securityKey

#Home page route
@app.route('/')
def home():
    return render_template('index.html')

#registration route
@app.route('/registration', methods=['POST'])
def register():
    return registration.registration()

#verify otp route
@app.route('/verify_otp', methods=['POST'])
def verifyOtp():
    return verify_otp.verifyOtp()

#login route
@app.route('/login', methods=['POST'])
def login():
    return authentication.login()

if __name__ == '__main__':
    app.run(debug=True)