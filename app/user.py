from flask import render_template, request, redirect, url_for, flash, session, current_app
from app import app, collection_user_registration
from functools import wraps
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
from app.utils import setup_cloudinary, upload_image, get_image_url
import os

# Import the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/create-article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.getlist('category')  # Assuming multiple categories can be selected
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('create_article'))
        
        # Handle image upload
        image_public_id = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                try:
                    setup_cloudinary()
                    image_public_id = upload_image(image_file)
                except Exception as e:
                    flash(f'Error uploading image: {str(e)}', 'error')
                    return redirect(url_for('create_article'))
        
        new_article = {
            'title': title,
            'content': content,
            'category': category,
            'author_id': ObjectId(session['user_id']),
            'author_name': session.get('username', 'Unknown'),
            'created_at': datetime.utcnow(),
            'status': 'pending',  # Assuming articles need approval before publishing
            'image_public_id': image_public_id
        }
        
        result = app.db.articles.insert_one(new_article)
        
        if result.inserted_id:
            flash('Your article has been submitted for review!', 'success')
            return redirect(url_for('hello_world'))  # or wherever you want to redirect after creation
        else:
            flash('There was an error submitting your article. Please try again.', 'error')
    
    return render_template('Newsers/create_article.html')

# You might also want to add a route to view user's own articles
@app.route('/my-articles')
@login_required
def my_articles():
    user_articles = app.db.articles.find({'author_id': ObjectId(session['user_id'])}).sort('created_at', -1)
    
    # Add image URLs to the articles
    articles_with_images = []
    for article in user_articles:
        if article.get('image_public_id'):
            article['image_url'] = get_image_url(article['image_public_id'])
        articles_with_images.append(article)
    
    return render_template('Newsers/my_articles.html', articles=articles_with_images)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS