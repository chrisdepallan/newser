from flask import render_template, redirect, url_for, session
from app import app, collection_user_registration, collection_login_credentials

@app.route("/")
def hello_world():
    return render_template("login/index.html")

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
