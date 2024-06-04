import jwt
import datetime

def generate_jwt_auth_token(user_id, secret_key, expiration_minutes=30):
    """
    Generate a JWT auth token.
    
    Parameters:
    - user_id (str): The user ID to include in the token.
    - secret_key (str): The secret key to sign the token.
    - expiration_minutes (int): The token expiration time in minutes. Default is 30 minutes.
    
    Returns:
    - str: The generated JWT token.
    """
    # Define the token payload
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime() + datetime.timedelta(minutes=expiration_minutes)
    }
    
    # Encode the token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return token