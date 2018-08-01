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
        app.config.from_object(app_config["testing"])
        
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
                    usersame=username,
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
                    usersame=username,
                    password=password
                )
            ),
            content_type='application/json'
        )


   

    def add_entry(self,id, title, content,date):
        """
        Function to create a request
        """
        return self.client.post(
            '/api/v1/entries',
            data=json.dumps(
                dict(
                    id=id,
                    title=title,
                    content=content,
                    date=date
                )
            ),
            content_type='application/json'
        )

   