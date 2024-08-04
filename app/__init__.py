from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from app.utils import NewsAPIClient
from flask_mail import Mail

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
Session(app)
bcrypt = Bcrypt(app)
oauth = OAuth(app)
mail = Mail(app)

# Register OAuth client
oauth.register(
    "myApp",
    client_id=app.config["OAUTH2_CLIENT_ID"],
    client_secret=app.config["OAUTH2_CLIENT_SECRET"],
    client_kwargs={"scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read"},
    server_metadata_url=app.config["OAUTH2_META_URL"],
)

# Initialize MongoDB client
client = MongoClient(app.config["MONGO_URI"])
db = client.newser
collection_user_registration = db.newser_user_registration
collection_login_credentials = db.newser_login_credentials

# Initialize NewsAPI client within the application context
with app.app_context():
    news_api_client = NewsAPIClient(app.config['NEWSAPI_KEYS'])

# Import routes
from app import routes, auth,utils,dashboard
    