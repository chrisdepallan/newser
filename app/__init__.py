from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object('config.Config')

Session(app)
bcrypt = Bcrypt(app)
oauth = OAuth(app)

oauth.register(
    "myApp",
    client_id=app.config["OAUTH2_CLIENT_ID"],
    client_secret=app.config["OAUTH2_CLIENT_SECRET"],
    client_kwargs={"scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read"},
    server_metadata_url=app.config["OAUTH2_META_URL"],
)

client = MongoClient(app.config["MONGO_URI"])
db = client.newser
collection_user_registration = db.newser_user_registration
collection_login_credentials = db.newser_login_credentials

from app import routes, auth
    