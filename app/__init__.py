from flask import Flask
from flask_restful import Api

from app.views import SignUp,Login,Entry,SingleEntry

app = Flask(__name__)

app.secret_key = "aminah"

"""Am initializing an API for my application"""
api = Api(app)

api.add_resource(SignUp,'/api/v1/auth/signup')
api.add_resource(Login,'/api/v1/auth/login')
api.add_resource(Entry,'/api/v1/entries')
api.add_resource(SingleEntry,'/api/v1/entries/<int:entryId>')