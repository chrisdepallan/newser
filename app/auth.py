from flask import redirect, url_for, request, session, render_template, jsonify
from app import app, bcrypt, oauth, collection_user_registration, collection_login_credentials,redis_client
from authlib.integrations.flask_client import OAuthError
from app.routes import generate_avatar # Import the generate_avatar function
import uuid
import json

class LoginManager:
    def __init__(self, app, bcrypt, oauth, collection_user_registration, collection_login_credentials, redis_client):
        self.app = app
        self.bcrypt = bcrypt
        self.oauth = oauth
        self.collection_user_registration = collection_user_registration
        self.collection_login_credentials = collection_login_credentials
        self.redis_client = redis_client

 
    def google_login(self):
        return self.oauth.myApp.authorize_redirect(redirect_uri=url_for("newser_signin_google", _external=True))

 
    def newser_signin_google(self):
        try:
            token = self.oauth.myApp.authorize_access_token()
        except OAuthError as error:
            error_description = error.description if hasattr(error, 'description') else 'Unknown error'
            return redirect(url_for("login"))
        if token is None:
            return "Google authentication failed: no token received."

        user_info = token.get("userinfo")
        user_email = user_info.get('email')
        user = self.collection_login_credentials.find_one({'email': user_email})

        if not user:
            # Generate random avatar URL
            avatar_url = generate_avatar()

            # Create new user registration
            user_registration = {
                "full_name": user_info.get('name'),
                "phone_number": "",
                "address": "",
                "dob": "",
                "avatar": avatar_url
            }
            result = self.collection_user_registration.insert_one(user_registration)
            registration_id = result.inserted_id

            # Create new login credentials
            user_login_credentials = {
                "username": user_info.get('name'),
                "email": user_email,
                "password": "",
                "registration_id": registration_id
            }
            result = self.collection_login_credentials.insert_one(user_login_credentials)
            user = user_login_credentials
        else:
            registration_id = user['registration_id']

        user_details = self.collection_user_registration.find_one({'_id': registration_id})
        session_id = str(uuid.uuid4())
        user_data = {
            'user_id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'full_name': user_details['full_name'],
            'phone_number': user_details['phone_number'],
            'address': user_details['address'],
            'dob': user_details['dob'],
            'avatar': user_details.get('avatar')
        }
        self.redis_client.setex(f"session:{session_id}", 3600, json.dumps(user_data))  # Expire in 1 hour

        response = redirect(url_for("hello_world"))
        response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Lax')
        return response

 
    def register(self):
        if request.method == 'POST':
            full_name = request.form.get('fullName')
            username = request.form.get('username')
            email = request.form.get('email')
            
            # Check if email already exists
            existing_user = self.collection_login_credentials.find_one({'email': email})
            if existing_user:
                return jsonify({'error': 'Email already exists', 'field': 'email'}), 400

            phone_number = request.form.get('phoneNumber')
            address = request.form.get('address')
            dob = request.form.get('dob')
            password = request.form.get('password')
            hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')

            # Generate random avatar URL
            avatar_url = generate_avatar()

            user_registration = {
                "full_name": full_name,
                "phone_number": phone_number,
                "address": address,
                "dob": dob,
                "avatar": avatar_url  # Add the avatar URL to the registration data
            }
            print(user_registration)
            result = self.collection_user_registration.insert_one(user_registration)
            id = result.inserted_id

            user_login_credentials = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "registration_id": id
            }
            self.collection_login_credentials.insert_one(user_login_credentials)
            return redirect(url_for('hello_world'))
        return render_template("login/register.html")

 
    def login(self):
        print("Login function called")  # Debug print
        if request.method == 'POST':
            print("POST request received")  # Debug print
            email = request.form.get('email')
            password = request.form.get('password')
            print(f"Email: {email}, Password: {password}")  # Debug print (be cautious with logging passwords in production)
            if not email or not password:
                return jsonify({'error': 'Email and password are required'}), 400

            user = self.collection_login_credentials.find_one({'email': email})
            if user and self.bcrypt.check_password_hash(user['password'], password):
                user_details = self.collection_user_registration.find_one({'_id': user['registration_id']})
                
                session_id = str(uuid.uuid4())
                user_data = {
                    'user_id': str(user['_id']),
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user_details['full_name'],
                    'phone_number': user_details['phone_number'],
                    'address': user_details['address'],
                    'dob': user_details['dob'],
                    'avatar': user_details.get('avatar')
                }
                self.redis_client.setex(f"session:{session_id}", 3600, json.dumps(user_data))  # Expire in 1 hour

                response = redirect(url_for('hello_world'))
                response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Lax')
                return response
            else:
                return jsonify({'error': 'Invalid email or password'}), 401
        return render_template("login/index.html")
    
 
    def logout(self):
        session_id = request.cookies.get('session_id')
        if session_id:
            self.redis_client.delete(f"session:{session_id}")
        response = redirect(url_for('hello_world'))
        response.delete_cookie('session_id')
        return response

 
    def check_email(self):
        email = request.args.get('email')
        existing_user = self.collection_login_credentials.find_one({'email': email})
        if existing_user:
            return jsonify({'exists': True}), 200
        return jsonify({'exists': False}), 200


login_manager = LoginManager(app, bcrypt, oauth, collection_user_registration, collection_login_credentials, redis_client)

@app.route("/google_login")
def google_login():
    return login_manager.google_login()

@app.route("/newser-signin-google")
def newser_signin_google():
    return login_manager.newser_signin_google()
@app.route('/logout')
def logout():
    return login_manager.logout()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return login_manager.register()

@app.route('/login', methods=['POST', 'GET'])
def login():
    return login_manager.login()

@app.route('/check-email')
def check_email():
    return login_manager.check_email()

def get_current_user():
    session_id = request.cookies.get('session_id')
    if session_id:
        user_data = redis_client.get(f"session:{session_id}")
        if user_data:
            return json.loads(user_data)
    return None
def is_admin(user):
    # return user.get('role') == 'admin'
    return True