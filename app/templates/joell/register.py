from flask import Flask, url_for, session, request, jsonify, render_template, redirect, flash
from pymongo import MongoClient
import os
from flask_mail import Mail, Message
import random
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
import json
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.base_client.errors import OAuthError


app = Flask(__name__)

appConf = {
    "OAUTH2_CLIENT_ID": "712817468203-fje586n01jt8n7v0mrf764vq1rl114mq.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "93ab6897-5c7c-40f1-a214-a90d7726b8cb",
    "FLASK_PORT": 5000
}
app.secret_key = appConf.get('FLASK_SECRET')
oauth = OAuth(app)
# list of google scopes - https://developers.google.com/identity/protocols/oauth2/scopes
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

@app.route("/google-login")
def googleLogin():
    try:
        return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))
    except OAuthError as e:
        # Redirect to login page if access is denied or cancelled
        return redirect(url_for('login'))

@app.route("/signin-google")
def googleCallback():
    try:
        token = oauth.myApp.authorize_access_token()

        # Fetch user info from Google API using the token
        user_info = oauth.myApp.parse_id_token(token, nonce=session.get('nonce'))
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')
        email = user_info.get('email')

        # Save user details to registration collection
        user_registration = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
        result = collection_user_registration.insert_one(user_registration)
        id = result.inserted_id

        user_login = {
            "first_name": first_name,
            "email": email,
            # Add other necessary fields
        }
        result_login = collection_login_credentials.insert_one(user_login)

        return redirect(url_for('login'))
    except OAuthError as e:
        # Redirect to login page if access is denied or cancelled
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('register'))

bcrypt = Bcrypt(app)  # Initialize Bcrypt

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://j-baby:j-baby@cluster0.0hfcgrb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(MONGO_URI)
db = client.Rythmix     
collection_user_registration = db.Register
collection_login_credentials = db.Login

@app.route("/")
def hello_world():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first')
        last_name = request.form.get('last')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        password = request.form.get('pass')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a document to insert
        user_registration = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "gender": gender,
            "email": email,
            "password": hashed_password
        }

        result = collection_user_registration.insert_one(user_registration)
        id = result.inserted_id

        user_login_credentials = {
            "first_name": first_name,
            "email": email,
            "password": hashed_password,
            "registration_id": id
        }

        # Insert into login credentials collection
        result = collection_login_credentials.insert_one(user_login_credentials)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        
        # Find user in login credentials collection
        user = collection_login_credentials.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            # Authentication successful
            return "Login successful"
        else:
            # Authentication failed
            return "Login failed"

    return render_template('login.html', session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

@app.route("/forgot_password")
def password():
    return render_template('forgot_password.html')



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'joelpbaby2025@mca.ajce.in'
app.config['MAIL_PASSWORD'] = 'Jo7902697895ajce'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


# Route for forgot password
@app.route("/email_verify", methods=['GET', 'POST'])
def email_verify():
    if request.method == 'POST':
        email = request.form['email']
        user = collection_user_registration.find_one({"email": email})

        if user:
            otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            session['otpcode'] = otp_code
            session['email'] = email

            msg = Message('Forgot Password', sender='joelpbaby2025@mca.ajce.in', recipients=[email])
            msg.html = render_template('otp_design.html', fname=user['first_name'], lname=user['last_name'], otp_code=otp_code)
            try:
                mail.send(msg)
                flash('OTP successfully mailed', 'success')
                return redirect(url_for('otp_verify'))
            except Exception as e:
                print(f"Error sending email: {e}")  
                flash('Email not sent: ' + str(e), 'danger')
        else:
            flash('Email not found', 'danger')
    return render_template('forgot_password.html')

# Route for OTP verification
@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    if request.method == 'POST':
        otp = request.form['otp']
        if otp == session.get('otpcode'):
            flash('OTP verified successfully', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Invalid OTP', 'danger')
    return render_template('otp_verify.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        password = request.form['password']
        email = session.get('email')

        if not email:
            flash('No email in session', 'danger')
            return redirect(url_for('forgot_password'))

        # Hash the new password
        hashed_password = generate_password_hash(password)

        collection_user_registration.update_one({'email': email}, {'$set': {'password': hashed_password}})

        collection_login_credentials.update_one({'email': email}, {'$set': {'password': hashed_password}})

        flash('Your password has been reset successfully', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
