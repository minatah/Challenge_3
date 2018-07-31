from flask import Flask, jsonify, make_response
from flask_restful import Resource, reqparse
import json
from app.config import conn,generate_token,decode_token
import re
import psycopg2

class SignUp(Resource):
    
    def post(self):
        
        parser = reqparse.RequestParser()
        """collecting args"""
        parser.add_argument('username', type=str,required=True)
        parser.add_argument('email', type=str,required=True)
        parser.add_argument('password', type=str, required=True)

        """getting specific args"""
        args = parser.parse_args()
        username = args['username']
        email=args['email']
        password=args['password']


        if username.strip() == "" or len(username.strip()) < 3:
            return make_response(jsonify({"message": "invalid username, Enter correct username please"}),
                             400)

        """to ignore symblos in the username by regular expressions"""

        if re.compile('[!@#$%^&*:;?><.0-9]').match(username):
            return make_response(jsonify({"message": "Invalid characters not allowed, numbers and symbols are not allowed"}),
                                    400)
        """to check for a valid email"""
        
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({"message": "Enter valid email"}),
                                    400)

        if password.strip() == "" or password.strip() == " " or password.strip() == "   ":
            return make_response(jsonify({"message": "Password Empty, Enter a valid  password"}),
                                    400)
         
        if len(password.strip()) < 5:
            return make_response(jsonify({"message": "Password is too short, < 5"}),
                                    400)
            
        """creating a sign up  cursor to check for already existing users."""

        cur = conn.cursor()
        cur.callproc('signup', (username,email,password,))
        """fecthing one value in a row """
        row = cur.fetchone()
        conn.commit()
        """formatting the status_value , removong unwanted symbols"""
        status_value = str(row).strip().replace('(','').replace(')','').replace(',','')
        
        if int(status_value)== 0:
            return make_response(jsonify({
                "message":'The username is already in use'
            }), 409)
        return make_response(jsonify({
                "message":'User created successfully'
            }), 201)

class Login(Resource):
    def post(self):
        
        parser = reqparse.RequestParser()
        """collecting args"""
        parser.add_argument('username', type=str,required=True)
        parser.add_argument('password', type=str, required=True)

        """getting specific args"""
        args = parser.parse_args()
        username = args['username']
        password=args['password']


        if username.strip() == "" or len(username.strip()) < 3:
                return make_response(jsonify({"message": "invalid username, Enter correct username please"}),
                             400)

        """to ignore symblos in the username by regular expressions"""

        if re.compile('[!@#$%^&*:;?><.0-9]').match(username):
            return make_response(jsonify({"message": "Invalid characters not allowed, numbers and symbols are not allowed"}),
                                    400)
      
        if password.strip() == "" or password.strip() == " " or password.strip() == "   ":
            return make_response(jsonify({"message": "Password Empty, Enter a valid  password"}),
                                    400)
                            


        cur = conn.cursor()
        cur.callproc('login', (username,password,))
        """fecthing one value in a row """
        row = cur.fetchone()
        conn.commit()
        """formatting the status_value , removong unwanted symbols"""
        status_value = str(row).strip().replace('(','').replace(')','').replace(',','')
        
        token = generate_token(username)

        if int(status_value)== 0:
            return make_response(jsonify({
                "message":'invalid username or password'
            }), 400)
        return make_response(jsonify({
                "message":'User signed in successfully',
                'token':token
            }), 200)
        
class Entry(Resource):
    def insert_entries(self):
        
        parser = reqparse.RequestParser()
        """collecting args"""
        parser.add_argument('token', location='headers')
        parser.add_argument('title', type=str,required=True)
        parser.add_argument('content', type=str,required=True)
        parser.add_argument('date', type=str, required=True)

        """getting specific args"""
        args = parser.parse_args()
        title = args['title']
        content =args['content']
        date = args['date']

        token = args['token']

        if not token:
            return make_response(jsonify({
                'message':'token missing'
            }),400)

        """ implementing token decoding"""
        decoded = decode_token(token)
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)
        

        cur = conn.cursor()
        cur.execute("INSERT INTO entries (title,contents,date_) VALUES ('"+title+"','"+content+"','"+date+"')")
        conn.commit()

        return make_response(jsonify({
            'message':'Created an entry successfully.'
        }),201) 
    
    def post(self):
        try:

           return self.insert_entries()

        except psycopg2.DatabaseError as e:
            if conn:
                print(e)
                conn.rollback()
                return self.insert_entries()
        except psycopg2.InterfaceError as Ie:
             print(Ie)
             return self.insert_entries()
   

class SingleEntry(Resource):
    
    def get(self,entryId):
        cur = conn.cursor()
        cur.execute("SELECT * from entries where entryid=%s",(entryId,))
        result=cur.fetchone()
        print(result)
        return {'entry': result}, 200

       # return make_response(jsonify({
          #  'message':'Sorry the entry does not exist'
        #}),404)

class viewEntries(Resource):
    def get(self):
        cur = conn.cursor()
        cur.execute("SELECT * from entries")
        result=cur.fetchall()
        print(result)
        return {'entry': result}, 200

class UpdateEntries(Resource):
    def put(self, entryId):
        
        parser = reqparse.RequestParser()
        """collecting args"""

        parser.add_argument('title', type=str,required=True)
        parser.add_argument('content', type=str,required=True)
        parser.add_argument('date', type=str, required=True)

        """getting specific args"""
        args = parser.parse_args()
        title = args['title']
        content =args['content']
        date = args['date']
        try:
            cur = conn.cursor()
            cur.execute("UPDATE entries SET title=%s,contents=%s,date_=%s where entryid=%s",(title,content,date,entryId))
            conn.commit()
            return make_response(jsonify({
        'message': 'entry updated successfully'
        }), 200)
        except:
            return make_response(jsonify({
        'message': 'entry not found'
        }), 404)

        
            
        
      
    
 
       


    

        
    



    