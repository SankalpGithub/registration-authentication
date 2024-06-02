from flask import Flask, request, jsonify

def registration():
    
    name = request.json.get('name')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    confrim_password = request.json.get('confirm_password')

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if not username:    
        return jsonify({'error': 'Username is required'}), 400
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    if not confrim_password:
        return jsonify({'error': 'Confirm Password is required'}), 400
    
    if password != confrim_password:
        return jsonify({'error': 'Password and Confirm Password do not match'}), 400 
    
