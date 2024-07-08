from flask import Flask, request, jsonify,render_template,redirect,url_for,session
from flask_session import Session
from authlib.integrations.flask_client import OAuth
import json
from pymongo import MongoClient
import os

from flask_bcrypt import Bcrypt 

app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.config['SECRET_KEY'] = '1234'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# Replace with your MongoDB Atlas connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://chrisdepallan:chrisdepallan@cluster0.1fiecxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(MONGO_URI)
db = client.newser
collection_user_registration = db.newser_user_registration  
collection_login_credentials = db.newser_login_credentials   
#google sign-in
appConf = {
    "OAUTH2_CLIENT_ID": "563837791779-428mfra3k3klg8vk9f5ai1a5t2pmu6ea.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)

@app.route("/google_login")
def  google_login():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("newser_signin_google",_external=True))



@app.route("/newser-signin-google")
def newser_signin_google():
    token = oauth.myApp.authorize_access_token()
    session["user"]=token
    user_info = token.get("userinfo")
    user_email = user_info.get('email')
    
    user = collection_login_credentials.find_one({'email': user_email})
    session['user_id'] = str(user['_id'])
    session['username'] = user['username']
    session['email'] = user['email']
    user_details = collection_user_registration.find_one({'_id': user['registration_id']})
    if user_details:
        session['full_name'] = user_details['full_name']
        session['phone_number'] = user_details['phone_number']
        session['address'] = user_details['address']
        session['dob'] = user_details['dob']
            
           
    # return user_email
    # return json.dumps(session.get("user"))
    return redirect(url_for("newser"))

@app.route("/profile")
def profile():
    user=session.get("user_id")
    if not user:
        return redirect(url_for("login")) 
    return render_template("Newsers/profile.html") 
@app.route("/edit_profile")
def edit_profile():
    user=session.get("user_id")
    if not user:
        return redirect(url_for("login")) 
    return render_template("Newsers/edit_profile.html") 
       
    
@app.route("/")
def hello_world():
    
    return render_template("login/index.html")
    # return render_template("Newsers/404.html")
# @app.route('/authorize')
# def authorize():
#     token = google.authorize_access_token()
#     user = google.parse_id_token(token)
#     session['email'] = user['email']
#     return redirect('/')
@app.route('/newser')
def newser():
    return  render_template("Newsers/index.html")
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('fullName')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber')
        address = request.form.get('address')
        dob = request.form.get('dob')
        password=request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 


        # Create a document to insert
        user_registration = {
            "full_name": full_name,
            "phone_number": phone_number,
            "address": address,
            "dob": dob
            
        }
        # Insert the document into MongoDB
        result=collection_user_registration.insert_one(user_registration)
        id=result.inserted_id
        user_login_credentials={"username": username,
            "email": email,"password":hashed_password
        ,"registration_id":id
        }
        result=collection_login_credentials.insert_one(user_login_credentials)
        return redirect(url_for('hello_world'))
    
    return render_template("login/register.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
       
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = collection_login_credentials.find_one({'email': email})
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['email'] = user['email']
            user_details = collection_user_registration.find_one({'_id': user['registration_id']})
            if user_details:
                session['full_name'] = user_details['full_name']
                session['phone_number'] = user_details['phone_number']
                session['address'] = user_details['address']
                session['dob'] = user_details['dob']
            
            return redirect(url_for('newser'))
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    return render_template("login/index.html")

@app.route('/home')
def home():
    # Check if session is active
    if not session.get("user_id"):
        return redirect("/")
    
    return render_template('Newsers/index.html')
@app.route('/home_test')
def home_test():
    # Check if session is active
    # if not session.get("user_id"):
    #     return redirect("/")
    
    return render_template('Newsers/index.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('full_name', None)
    session.pop('phone_number', None)
    session.pop('address', None)
    session.pop('dob', None)
    session.pop('user', None)
    return redirect(url_for('hello_world'))
    # return redirect(url_for('hello_world'))  # Redirect to login page after logout

if __name__ == '__main__':
    app.run(debug=True)

