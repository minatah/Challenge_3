from flask import Flask, jsonify, make_response
from flask_restful import Resource, reqparse
import json
from app.config import generate_token,decode_token,configconnection
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

        conn=configconnection()
        cur = conn.cursor()

        cur.execute("SELECT username from users where username=%s",[username])
        rows = cur.fetchone()

        if rows:
        
            return make_response(jsonify({
                "message":'Username is used'
            }), 400)
        else:
            cur.execute("INSERT INTO users (username,email,password) VALUES ('"+username+"','"+email+"','"+password+"')")
            conn.commit()
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

        conn=configconnection()
        cur = conn.cursor()
        cur.execute("select username from users where username=%s and password=%s ", (username,password))

        rows = cur.fetchone()

        if rows:
            token = generate_token(username)
            return make_response(jsonify({
                "message":'User signed in successfully',
                'token':token
            }), 200)
            
        else:
            return make_response(jsonify({
                   "message":'invalid username or password'
                    }), 400)
            
        
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
        conn=configconnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO entries (title,content,date) VALUES ('"+title+"','"+content+"','"+date+"')")
        conn.commit()

        return make_response(jsonify({
            'message':'Created an entry successfully.'
        }),201) 
    
    def post(self):
        conn=configconnection()
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
        parser = reqparse.RequestParser()
        """collecting args"""
        parser.add_argument('token', location='headers')

        """getting specific args"""
        args = parser.parse_args()
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

        conn=configconnection()
        cur=conn.cursor()
        cur.execute("SELECT * from entries where id=%s",(entryId,))
        result=cur.fetchall()
        
        lst=[]
        for info in result:
            dic={}
            dic["id"]=info[0]
            dic["title"]=info[1]
            dic["content"]=info[2]
            dic["date"]=info[3]
            lst.append(dic)
        return {'entry': str(lst).replace('[','').replace(']','')}, 200



class viewEntries(Resource):
    

    def get(self):
        parser = reqparse.RequestParser()
        """collecting args"""
        parser.add_argument('token', location='headers')

        """getting specific args"""
        args = parser.parse_args()
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
        conn=configconnection()
        cur=conn.cursor()
        cur.execute("SELECT * from entries")
        result=cur.fetchall()
            
        lst=[]
        for info in result:
            
            dic={}
            dic["id"]=info[0]
            dic["title"]=info[1]
            dic["content"]=info[2]
            dic["date"]=info[3]
            lst.append(dic)
        return lst, 200

class UpdateEntries(Resource):
    def put(self, entryId):
        
        parser = reqparse.RequestParser()
        """collecting args"""

        parser.add_argument('title', type=str,required=True)
        parser.add_argument('content', type=str,required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('token', location='headers')

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



        try:
            conn=configconnection()
            cur=conn.cursor()
            cur.execute("UPDATE entries SET title=%s,content=%s,date=%s where id=%s",(title,content,date,entryId))
            conn.commit()
            return make_response(jsonify({
        'message': 'entry updated successfully'
        }), 200)
        except:
            return make_response(jsonify({
        'message': 'entry not found'
        }), 404)

        
            
        
      
    
 
       


    

        
    



    