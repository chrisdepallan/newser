from flask import render_template, request, redirect, url_for, flash, session, current_app
from app import app, collection_user_registration,collection_articles
from functools import wraps
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
from app.utils import setup_cloudinary, upload_image, get_image_url
import os
import cloudinary


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
        
        result = collection_articles.insert_one(new_article)
        
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
    user_articles = collection_articles.find({'author_id': ObjectId(session['user_id'])}).sort('created_at', -1)
    setup_cloudinary()
    # Add image URLs to the articles
    articles_with_images = []
    for article in user_articles:
        if article.get('image_public_id'):
            article['image_url'] = get_image_url(article['image_public_id'])
        articles_with_images.append(article)
    
    return render_template('Newsers/my_articles.html', articles=articles_with_images)

@app.route('/view-articles')
@login_required
def view_articles():
    user_id = ObjectId(session['user_id'])
    articles = collection_articles.find({'author_id': user_id}).sort('created_at', -1)
 
    # Process articles to add image_url and format dates
    processed_articles = []
    for article in articles:
        article['_id'] = str(article['_id'])  # Convert ObjectId to string
        if 'image_public_id' in article:
            article['image_url'] = get_image_url(article['image_public_id'])
        processed_articles.append(article)
    
    return render_template('Newsers/view_articles.html', articles=processed_articles)

# You'll also need to add routes for viewing and editing individual articles
@app.route('/article/<article_id>')
def view_article(article_id):
    article = collection_articles.find_one({'_id': ObjectId(article_id)})
    if not article:
        flash('Article not found', 'error')
        return redirect(url_for('hello_world'))
    
    # Add image URL to the article if it exists
    if article.get('image_public_id'):
        article['image_url'] = get_image_url(article['image_public_id'])
    
    # Format the date
    article['created_at'] = article['created_at'].strftime('%B %d, %Y')
    
    return render_template('Newsers/detail-page.html', article=article)

@app.route('/edit-article/<article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = collection_articles.find_one({'_id': ObjectId(article_id)})
    if not article:
        flash('Article not found', 'error')
        return redirect(url_for('view_articles'))

    if article['author_id'] != ObjectId(session['user_id']):
        flash('You do not have permission to edit this article', 'error')
        return redirect(url_for('view_articles'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        categories = request.form.getlist('category')  # Changed from 'category' to 'categories'
        image = request.files.get('image')

        if not title or not content:
            flash('Title and content are required', 'error')
        else:
            update_data = {
                'title': title,
                'content': content,
                'categories': categories,  # Changed from 'category' to 'categories'
                'updated_at': datetime.utcnow()
            }

            if image and allowed_file(image.filename):
                if article.get('image_public_id'):
                    cloudinary.uploader.destroy(article['image_public_id'])
                result = upload_image(image)
                update_data['image_public_id'] = result

            collection_articles.update_one({'_id': ObjectId(article_id)}, {'$set': update_data})
            flash('Article updated successfully', 'success')
            return redirect(url_for('view_article', article_id=article_id))

    return render_template('Newsers/edit_post.html', article=article)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS