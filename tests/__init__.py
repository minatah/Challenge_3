import unittest
import os
import sys
import json
sys.path.append(os.getcwd())
from app import app
from app.config import app_config



class MyTestCase(unittest.TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        app.config.from_object(app_config["testing"])
        return app
        
    def setUp(self):
        self.client = app.test_client(self)



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

   