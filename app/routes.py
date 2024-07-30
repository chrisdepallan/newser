from flask import render_template, redirect, url_for, session, request, current_app, flash
from app import app, collection_user_registration, collection_login_credentials,news_api_client
from app.utils import get_search_results
import pyotp
from app import app, mail,bcrypt
from flask_mail import Message
SECRET = 'base32secret3232'
@app.route("/")
def hello_world():
    return render_template("login/index.html")
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
    return render_template("Newsers/profile.html")

@app.route("/edit_profile")
def edit_profile():
    user = session.get("user_id")
    if not user:
        return redirect(url_for("login"))
    return render_template("Newsers/edit_profile.html")

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello_world'))

@app.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        user = collection_login_credentials.find_one({'email': email})
        if user:
            totp = pyotp.TOTP(SECRET)
            otp = totp.now()

            msg = Message('Password Reset OTP', recipients=[email])
            msg.body = f'Your OTP for password reset is: {otp}'
            mail.send(msg)

            session['reset_email'] = email
            return redirect(url_for('verify_otp'))

        flash('Email not found')
    return render_template('joell/forgot_password.html')


@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        print(otp)
        totp = pyotp.TOTP(SECRET)
        if totp.verify(otp,valid_window=1):
            return redirect(url_for('reset_password'))
        flash('Invalid OTP')
    return render_template('joell/otp_verify.html')


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
    return render_template('joell/reset_password.html')
