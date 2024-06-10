import jwt

def generate_token(id,securitykey,*args):
    
    payload = {
            'id': id,
            'password': args[0]
    }
    token = jwt.encode(payload,securitykey, algorithm='HS256')
    return token

def decode_token(token,securitykey):

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
    