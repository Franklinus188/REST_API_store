from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.store import Store, StoreList
from resources.user import UserRegister
from resources.item import Item, ItemList


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret_key"
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate,  identity)  # /auth
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
