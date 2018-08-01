from flask import Flask
from flask_restful import Api

from app.views import SignUp,Login,Entry,SingleEntry,viewEntries,UpdateEntries

app = Flask(__name__)

app.secret_key = "aminah"

"""Am initializing an API for my application"""
api = Api(app)

api.add_resource(SignUp,'/API/v1/auth/signup')
api.add_resource(Login,'/API/v1/auth/login')
api.add_resource(Entry,'/API/v1/entries')
api.add_resource(SingleEntry,'/API/v1/entries/<int:entryId>')
api.add_resource(viewEntries,'/API/v1/entries')
api.add_resource(UpdateEntries,'/API/v1/entries/<int:entryId>')
