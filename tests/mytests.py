
import unittest
import os
import sys
import json
sys.path.append(os.getcwd())
from app import app
from app.config import app_config
from flask import current_app


class MyTestCase(unittest.TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        
        return current_app
        
    def setUp(self):
        self.client = app.test_client(self)

    def signUp(self,username, email, password):
        """
        Function to create a request

        """
        return self.client.post(
            'API/v1/auth/signup',
            data=json.dumps(
                dict(
                    username=username,
                    email=email,
                    password=password
                )
            ),
            content_type='application/json'
        )

    def Login(self,username, password):
        """
        Function to create a request
        """
        return self.client.post(
            'API/v1/auth/login',
            data=json.dumps(
                dict(
                    username=username,
                    password=password
                )
            ),
            content_type='application/json'
        )

  
    def get_token(self):
        """Get a token for testing all endpoints"""
        response = self.Login("aminah", "12345")
        data = json.loads(response.data)
        return data['token']

    def add_entry(self, title, content,date, token):
        """
        Function to create a request
        """
        return self.client.post(
            '/API/v1/entries',
            data=json.dumps(
                dict(
                   
                    title=title,
                    content=content,
                    date=date
                )
            ),
            content_type='application/json'
            ,
            headers=({"token": token})
        )

    def get_all_entries(self,token):
        """get all entries"""
        return self.client.get('/API/v1/entries', headers=({"token": token}))

    def get_single_entry(self,id, token):
        """get all entries"""
        return self.client.get('/API/v1/entries/'+str(id), headers=({"token": token}))

    def update_entry(self,id,title, content , date ,token):
        return self.client.put(
            '/API/v1/entries/'+str(id),
            data=json.dumps(
                dict(
                   
                    title=title,
                    content=content,
                    date=date
                )
            ),
            content_type='application/json'
            ,
            headers=({"token": token})
        )