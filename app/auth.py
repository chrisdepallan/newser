from flask import redirect, url_for, request, session, render_template, jsonify
from app import app, bcrypt, oauth, collection_user_registration, collection_login_credentials
from authlib.integrations.flask_client import OAuthError

@app.route("/google_login")
def google_login():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("newser_signin_google", _external=True))

@app.route("/newser-signin-google")
def newser_signin_google():
    try:
        token = oauth.myApp.authorize_access_token()
    except OAuthError as error:
        error_description = error.description if hasattr(error, 'description') else 'Unknown error'
        return redirect(url_for("login"))
    if token is None:
        return "Google authentication failed: no token received."

    session["user"] = token
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

    return redirect(url_for("newser"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber')
        address = request.form.get('address')
        dob = request.form.get('dob')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user_registration = {
            "full_name": full_name,
            "phone_number": phone_number,
            "address": address,
            "dob": dob
        }
        result = collection_user_registration.insert_one(user_registration)
        id = result.inserted_id

        user_login_credentials = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "registration_id": id
        }
        collection_login_credentials.insert_one(user_login_credentials)
        return redirect(url_for('hello_world'))
    return render_template("login/register.html")

@app.route('/login', methods=['POST', 'GET'])
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
