from flask import Flask, request, jsonify, render_template
from flaskapp.routes import registration
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

if __name__ == '__main__':
    app.run(debug=True)