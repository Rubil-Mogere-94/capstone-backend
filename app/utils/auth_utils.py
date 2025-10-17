import bcrypt
import jwt
from datetime import datetime, timedelta
import os

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id, secret_key, expires_delta=timedelta(days=7)):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + expires_delta,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')
