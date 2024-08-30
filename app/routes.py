from flask import render_template, redirect, url_for, session, request, current_app, flash, jsonify
from app import app, collection_user_registration, collection_login_credentials, news_api_client, collection_subscriptions
from app.utils import *
import pyotp
from werkzeug.utils import secure_filename
from app import app, mail, bcrypt
import random
from flask_mail import Message
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from . import app
from .recommendation_engine import get_top_story, get_trending_news, get_popular_news
from .utils import upload_image, setup_cloudinary, get_image_url
SECRET = 'base32secret3232'
import stripe

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = 'sk_test_51MiftOSIxs4ZUV5mMRwCJZPY6Sa5xxQjwNW7j3NZ7Z0uAMdOZpfkJ8z5PXEvGURVzOkilzvmrTPVpn8vkZT7embw00HJuQCUXf'

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
    weather_data = get_weather_data()
    story = get_top_story()
    trending_news = get_trending_news()
    popular_news = get_popular_news()
    
    
    return render_template("Newsers/index.html", story=story, trending_news=trending_news, popular_news=popular_news, weather_data=weather_data)

@app.route('/news')
def news():
    return render_template('admin/template/search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        search_results = get_search_results(query)
        return render_template('admin/template/search.html', query=query, search_results=search_results)
    return redirect(url_for('news'))

from functools import wraps
from flask import session, redirect, url_for
from app.auth import login_manager
from app import redis_client
import json

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return redirect(url_for('login'))
        
        user_data = redis_client.get(f"session:{session_id}")
        if not user_data:
            return redirect(url_for('login'))
        
        # Optionally, you can decode the user data and attach it to the request
        # This allows you to access user information in your route handlers
        request.user = json.loads(user_data)
        
        return f(*args, **kwargs)
    return decorated_function

@app.route("/profile")
@login_required
def profile():
    user_id = session.get('user_id')
    user = collection_user_registration.find_one({'_id': user_id})
    
    
    
    weather_data = session.get('weather_data', {})
    return render_template("Newsers/profile.html", user=user, weather_data=weather_data)

@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
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
            {'_id': session['user_id']},
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
@login_required
def update_avatar():
    data = request.json
    new_avatar_url = data.get('new_avatar_url')

    if not new_avatar_url:
        return jsonify({"success": False, "message": "No avatar URL provided"}), 400

    try:
        print(new_avatar_url)
        collection_user_registration.update_one(
            {'_id': session['user_id']},
            {'$set': {'avatar': new_avatar_url}}
        )
        session['avatar'] = new_avatar_url
        return jsonify({"success": True, "message": "Avatar updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/newser")
@login_required
def newser():
    hello_world()



@app.route('/home_test')
def home_test():
    return render_template('Newsers/index.html')

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


@app.route('/upload_img')
def upload_img():
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

@app.route('/temp')
@login_required
def temp():
    return render_template('Newsers/temp.html')


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    amount = int(data.get('amount', 1000))  # Amount in cents
    user_id = session.get("user_id")  # Assuming you're using Flask-Login

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': amount,
                        'product_data': {
                            'name': 'Custom Payment',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment_cancel', _external=True),
        )
        
        # Insert payment details into collection_subscriptions
        collection_subscriptions.insert_one({
            'user_id': user_id,
            'amount': amount / 100,  # Convert cents to dollars
            'date': datetime.utcnow(),
            'session_id': checkout_session.id
        })
        
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/payment/success')
def payment_success():
    session_id = request.args.get('session_id')
    if session_id:
        # Update the subscription status in the database
        collection_subscriptions.update_one(
            {'session_id': session_id},
            {'$set': {'status': 'completed'}}
        )
    return render_template('Newsers/success.html')

@app.route('/payment/cancel')
def payment_cancel():
    return render_template('Newsers/cancel.html')

counter = 0

@app.route('/count')
def home():
    return render_template('joell/appuz.html')

@app.route('/increment')
def increment():
    global counter
    counter += 1
    return str(counter)
@app.route('/payment')
def payment():
    # amount = request.args.get('amount')  # Default to 1000 (10.00) if no amount is provided
    return render_template('Newsers/payment.html')# @app.route('/create-checkout-session', methods=['POST'])
# @login_required
# def create_checkout_session():
#     data = request.json
#     amount = int(data.get('amount', 1000))  # Amount in cents
#     user_id = session.get("user_id")  # Assuming you're using Flask-Login

#     try:
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': amount,
#                         'product_data': {
#                             'name': 'Custom Payment',
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url=url_for('payment_cancel', _external=True),
#         )
        
#         # Insert payment details into newser_subscriptions
#         newser_subscriptions.insert_one({
#             'user_id': user_id,
#             'amount': amount / 100,  # Convert cents to dollars
#             'date': datetime.utcnow(),
#             'session_id': checkout_session.id
#         })
        
#         return jsonify({'id': checkout_session.id})
#     except Exception as e:
#         return jsonify(error=str(e)), 403

# @app.route('/payment/success')
# def payment_success():
#     session_id = request.args.get('session_id')
#     if session_id:
#         # Update the subscription status in the database
#         newser_subscriptions.update_one(
#             {'session_id': session_id},
#             {'$set': {'status': 'completed'}}
#         )
#     return render_template('Newsers/success.html')

# @app.route('/payment/cancel')
# def payment_cancel():
#     return render_template('Newsers/cancel.html')
