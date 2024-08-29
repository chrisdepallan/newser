from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from app.utils import NewsAPIClient, datetime_filter
from flask_mail import Mail
from flask_cors import CORS
import redis

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
app.config.from_object('config.Config')

# Configure Redis for session management
redis_host = 'redis-11738.c244.us-east-1-2.ec2.redns.redis-cloud.com'
redis_port = 11738
redis_password = 'X51UKTJVjgI2727qmgGyEHegLLTkPNSQ'  # Replace with your actual Redis password

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    ssl=True  # Enable SSL/TLS connection
)

# Initialize extensions
Session(app)

bcrypt = Bcrypt(app)
oauth = OAuth(app)
mail = Mail(app)
CORS(app)

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
collection_subscriptions=db.newser_subscriptions
collection_articles=db.newser_articles
# Initialize NewsAPI client within the application context
with app.app_context():
    news_api_client = NewsAPIClient(app.config['NEWSAPI_KEYS'])

# Register custom filter
app.jinja_env.filters['datetime'] = datetime_filter

# Import routes
from app import routes, auth,utils,dashboard,user
# Register recommendation_engine blueprint
# app.register_blueprint(recommendation_bp)