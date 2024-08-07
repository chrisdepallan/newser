from flask import render_template, redirect, url_for, session, request, current_app, flash, jsonify
from app import app, collection_user_registration, collection_login_credentials, news_api_client
from app.utils import *
import pyotp
from werkzeug.utils import secure_filename
from app import app, mail, bcrypt
import random
from flask_mail import Message
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from . import app
from .utils import upload_image, setup_cloudinary, get_image_url
SECRET = 'base32secret3232'

@app.route('/generate-avatar')
def generate_avatar():
    # Get options from query string
    style = request.args.get('style', random.choice(current_app.config['PFP_STYLE']))
    seed = request.args.get('seed')
    hair = request.args.getlist('hair')
    flip = request.args.get('flip')
    
    if flip is not None:
        flip = flip.lower() == 'true'
    
    avatar_url = generate_avatar_url(style, seed, hair, flip)
   
    return avatar_url


@app.route("/")
def hello_world():
    return render_template("Newsers/index.html")
@app.route('/news')
def news():
    # query = request.args.get('query', 'latest')
    # news_data = news_api_client.make_request('everything', {'q': query})
    # # return render_template('Newsers/news.html', news=news_data)
    return render_template('admin/template/search.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        # Fetch search results using the query
        search_results = get_search_results(query)
        return render_template('admin/template/search.html', query=query, search_results=search_results)
    return redirect(url_for('news'))

# def get_search_results(query):
    # Mock search results or fetch from your source
    # This is a placeholder. Replace with actual logic to fetch search results.
    # results = [
    #     {
    #         'title': 'PixelStrap - Portfolio | ThemeForest',
    #         'url': 'https://themeforest.net/user/pixelstrap/portfolio/',
    #         'description': "2024's Best Selling Creative WP Template. The #1 Source of Premium WP Template! ThemeForest 45,000+ WP Template & Website Templates From $2. Check it Out!",
    #         'stars': 3,
    #         'votes': 590,
    #         'type': 'Template'
    #     },
    #     {
    #         'title': 'PixelStrap - Portfolio | ThemeForest',
    #         'url': 'https://themeforest.net/user/pixelstrap/portfolio/',
    #         'description': 'The #1 marketplace for premium website templates, including Template for WordPress, Magento, Drupal, Joomla, and more. Create a website, fast.',
    #         'stars': 3,
    #         'votes': 590,
    #         'type': 'Theme'
    #     }
    # ]
    # return results
@app.route("/profile")
def profile():
    user = session.get("user_id")
    if not user:
        return redirect(url_for("login")) 
    weather_data = session.get('weather_data', {})
    return render_template("Newsers/profile.html", weather_data=weather_data)

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    user = session.get("user_id")
    if not user:
        return redirect(url_for("login"))
    
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        dob = request.form.get('dob')
        address = request.form.get('address')
        new_avatar_url = request.form.get('new_avatar_url')
        
        # Update user data in the database
        update_data = {
            'full_name': full_name,
            'phone_number': phone_number,
            'dob': dob,
            'address': address
        }
        if new_avatar_url:
            update_data['avatar_url'] = new_avatar_url
        
        collection_user_registration.update_one(
            {'_id': user},
            {'$set': update_data}
        )
        
        # Update session data
        session['full_name'] = full_name
        session['phone_number'] = phone_number
        session['dob'] = dob
        session['address'] = address
        if new_avatar_url:
            session['avatar_url'] = new_avatar_url
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    return render_template("Newsers/edit_profile.html")
@app.route("/update-avatar", methods=['POST'])
def update_avatar():
    user = session.get("user_id")
    if not user:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    data = request.json
    new_avatar_url = data.get('new_avatar_url')

    if not new_avatar_url:
        return jsonify({"success": False, "message": "No avatar URL provided"}), 400

    try:
        print(new_avatar_url)
        collection_user_registration.update_one(
            {'_id': user},
            {'$set': {'avatar': new_avatar_url}}
        )
        session['avatar'] = new_avatar_url
        return jsonify({"success": True, "message": "Avatar updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
@app.route("/newser")
def newser():
    return render_template("Newsers/index.html")

@app.route('/home')
def home():
    if not session.get("user_id"):
        return redirect("/")
    return render_template('Newsers/index.html')

@app.route('/home_test')
def home_test():
    return render_template('Newsers/index.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('hello_world'))

@app.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        user = collection_login_credentials.find_one({'email': email})
        if user:
            totp = pyotp.TOTP(SECRET)
            otp = totp.now()

            msg = Message('Password Reset OTP', recipients=[email])
            msg.html = render_template('login/otp_design.html', 
                                       fname=user.get('username', ''),
                                       lname='',
                                       otp_code=otp)
            mail.send(msg)

            session['reset_email'] = email
            return redirect(url_for('verify_otp'))

        flash('Email not found')
    return render_template('login/forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        print(otp)
        totp = pyotp.TOTP(SECRET)
        if totp.verify(otp,valid_window=1):
            return redirect(url_for('reset_password'))
        flash('Invalid OTP')
    return render_template('login/otp_verify.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        password = request.form.get('password')
        email = session.get('reset_email')
        if email:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            collection_login_credentials.update_one({'email': email}, {'$set': {'password': hashed_password}})
            flash('Password reset successfully')
            return redirect(url_for('login'))
        flash('Session expired, please request a new OTP')
    return render_template('login/reset_password.html')
@app.route('/sample')
def sample():
    return render_template('joell/sample.html')



@app.route('/upload_image', methods=['POST'])
def upload_image_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        try:
            # Ensure Cloudinary is set up
            setup_cloudinary()
            # Upload to Cloudinary
            public_id = upload_image(file)
            # Get the URL of the uploaded image
            image_url = get_image_url(public_id)
            return jsonify({'success': True, 'public_id': public_id, 'url': image_url}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Newsers/404.html'), 404