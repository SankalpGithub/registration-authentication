"""
This module contains the generate_token and decode_token methods,
 which are used to generate and decode JWT tokens, respectively.
"""

import jwt

def generate_token(_id,securitykey,*args):
    """
    This method is use to generate token for user authentication
    """

    payload = {
            'id': _id,
            'password': args[0]
    }
    token = jwt.encode(payload,securitykey, algorithm='HS256')
    return token

def decode_token(token,securitykey):
    """
    This method is use to decode the token and return the data
    """
    try:
        payload = jwt.decode(token,securitykey, algorithms=['HS256'])
        data = {
        'id': payload['id'],
        'password': payload['password'] 
        }
        return data
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'},401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'},401
    