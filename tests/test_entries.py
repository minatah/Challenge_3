import unittest
from tests.mytests import MyTestCase
import json
import datetime
class Tests_Requests(MyTestCase):

    def test_signing_up_users(self):
        """Tests when user signs up"""
        with self.client:
            """auto generate usernames with the help of system  date time"""
            autogenerate_usernames = str(datetime.datetime.now())
            response = self.signUp('aminah'+autogenerate_usernames,'aminah@gmail.com', '123456')
            """getting the response  from data"""
            self.assertEqual(response.status_code, 201)

    def test_login_user(self):
         """Tests user when logging in"""
         """first signup"""
         self.signUp('aminah','aminah@gmail.com', '12345')
         """Then login"""
         response = self.Login('aminah','12345')
         """getting the response  from data"""
         self.assertEqual(response.status_code, 200)

    def test_inserting_entry(self):
        """Tests when entering an entry."""
        token = self.get_token()
        response = self.add_entry("BD","My  birthday","12-2-2018",token)
        self.assertEqual(response.status_code, 201)

    def test_get_all_entries(self):
        """Tests get all entries"""
        token = self.get_token()
        
        response = self.get_all_entries(token)
        self.assertEqual(response.status_code, 200)

    def test_get_single_entry(self):
        """Tests get single entry """
        token = self.get_token()
        """first insert any entry"""
        self.add_entry("BD","My  birthday","12-2-2018",token)
        """then get a single entry"""
        response = self.get_single_entry(1,token)
        self.assertEqual(response.status_code, 200)

    def test_update_entry(self):
        """Tests get update entry """
        token = self.get_token()
        """first insert any entry """
        self.add_entry("BD","My  birthday","12-2-2018",token)
        """then update the above  entry"""
        response = self.update_entry(1,"My Birthday","It was fun","12-2-2018",token)
        self.assertEqual(response.status_code, 200)


            

  







