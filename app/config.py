import psycopg2
import sys
import os
import datetime
import jwt
from datetime import datetime, timedelta
from flask import current_app
from app.models import usertable,entrytable

#conn = psycopg2.connect(
    #"host='localhost' dbname='MyDiary' user='postgres' password='1234'")
def configconnection():
    
    if current_app.config["TESTING"] is not True:
        conn = psycopg2.connect("host='localhost' dbname='MyDiary' user='postgres' password='1234'")
        cur=conn.cursor()
        cur.execute(usertable)
        conn.commit()
        cur.execute(entrytable)
        conn.commit()
        
    else:
        
        conn = psycopg2.connect("host='localhost' dbname='testDB' user='postgres' password='1234'")
        cur =conn.cursor()
        cur.execute(usertable)
        conn.commit()
        cur.execute(entrytable)
        conn.commit()
        
    return conn

def generate_token(username):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'username': username
        }
        # create the byte string token using the payload and the SECRET key

        jwt_string = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):
    """Decode the access token to get the payload 
    and return user_id and  field results"""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {"username": payload['username'],
                "status": "Success"}
    except jwt.ExpiredSignatureError:
        return {"status": "Failure",
                "message": "Expired token. Please log in to get a new token"}
    except jwt.InvalidTokenError:
        return {"status": "Failure",
                "message": "Invalid token. Please register or login"}

