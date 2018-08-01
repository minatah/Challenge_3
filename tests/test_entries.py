import unittest
from tests import MyTestCase
import json
import datetime
class Tests_Requests(MyTestCase):

    def test_signing_up_users(self):
        """Tests when user signs up"""
        with self.client:
            response = self.signUp('huzaifah','aminah@gmail.com', '123456')
            """getting the response  from data"""
            self.assertEqual(response.status_code, 201)


            

  







