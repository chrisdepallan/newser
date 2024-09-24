from flask import Blueprint, render_template, session, redirect, url_for,request
from flask import jsonify,flash
from app import collection_user_registration,collection_articles,collection_login_credentials
from app.utils import get_weather_data,send_mass_email
from functools import wraps
from . import app
from bson import ObjectId
from .utils import get_image_url
from app import redis_client
import json,os
from werkzeug.utils import secure_filename

from .auth import get_current_user,is_admin
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
 
@app.route('/dashboard')
@login_required
def dashboard_view():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin privileges (you'll need to implement this logic)
    if not is_admin(user):
        return redirect(url_for('hello_world'))
    
    return render_template('admin/template/index.html', user=user)

from datetime import datetime

@app.route('/get_users')
@login_required
def get_users():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin privileges (you'll need to implement this logic)
    if not is_admin(user):
        return redirect(url_for('hello_world'))

    page = int(request.args.get('page', 1))
    per_page = 16  # 8x2 grid
    skip = (page - 1) * per_page

    users = list(collection_user_registration.find({}, {
        '_id': 1,
        'full_name': 1,
        'avatar': 1,
        'phone_number': 1,
        'address': 1,
        'dob': 1,
        'status': 1,
        'newser_user_roles': 1  # Include the roles field
    }).skip(skip).limit(per_page))

    for user in users:
        user['_id'] = str(user['_id'])
        # Convert DOB to age
        if user['dob']:
            try:
                dob = datetime.strptime(user['dob'], '%Y-%m-%d')
                today = datetime.now()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                user['age'] = age
            except ValueError:
                user['age'] = 'N/A'
        else:
            user['age'] = 'N/A'
        
        # Rename 'newser_user_roles' to 'roles' for frontend consistency
        user['roles'] = user.pop('newser_user_roles', [])
        
        # Remove the 'dob' field as we no longer need it
        user.pop('dob', None)

    total_users = collection_user_registration.count_documents({})
    total_pages = (total_users + per_page - 1) // per_page

    return jsonify({
        'users': users,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/users', methods=['GET'])
@login_required
def users_view():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin privileges (you'll need to implement this logic)
    if not is_admin(user):
        return redirect(url_for('hello_world'))
    
    return render_template('admin/template/users.html', user=user)

# @app.route('/temp')
# @login_required
# def temp_view():
#     return render_template('admin/template/temp.html')

from bson import ObjectId
from flask import jsonify

@app.route('/ban_user/<user_id>', methods=['POST'])
@login_required
def ban_user(user_id):
    try:
        result = collection_user_registration.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'status': 'banned'}}
        )
        
        if result.modified_count > 0:
            return jsonify({'message': 'User banned successfully'}), 200
        else:
            return jsonify({'error': 'User not found or already banned'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/unban_user/<user_id>', methods=['POST'])
@login_required
def unban_user(user_id):
    try:
        result = collection_user_registration.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'status': 'active'}}
        )
        
        if result.modified_count > 0:
            return jsonify({'message': 'User unbanned successfully'}), 200
        else:
            return jsonify({'error': 'User not found or already active'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_role', methods=['POST'])
@login_required
def add_role():
    data = request.json
    user_id = data.get('user_id')
    role = data.get('role')

    if not user_id or not role:
        return jsonify({'error': 'Missing user_id or role'}), 400

    try:
        result = collection_user_registration.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'newser_user_roles': role}}
        )

        if result.modified_count > 0:
            return jsonify({'message': 'Role added successfully'}), 200
        else:
            return jsonify({'error': 'User not found or role already assigned'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/remove_role', methods=['POST'])
@login_required
def remove_role():
    data = request.json
    user_id = data.get('user_id')
    role = data.get('role')

    if not user_id or not role:
        return jsonify({'error': 'Missing user_id or role'}), 400

    try:
        result = collection_user_registration.update_one(
            {'_id': ObjectId(user_id)},
            {'$pull': {'newser_user_roles': role}}
        )

        if result.modified_count > 0:
            return jsonify({'message': 'Role removed successfully'}), 200
        else:
            return jsonify({'error': 'User not found or role not assigned'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<user_id>')
@login_required
def user_profile(user_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin privileges (you'll need to implement this logic)
    if not is_admin(user):
        return redirect(url_for('hello_world'))

    # Fetch user data from the database
    user = collection_user_registration.find_one({'_id': ObjectId(user_id)})
   
    if user:
        # Convert ObjectId to string for JSON serialization
        user['_id'] = str(user['_id'])
        
        # Calculate age if DOB is available
        if 'dob' in user and user['dob']:
            try:
                dob = datetime.strptime(user['dob'], '%Y-%m-%d')
                today = datetime.now()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                user['age'] = age
            except ValueError:
                user['age'] = 'N/A'
        else:
            user['age'] = 'N/A'

        # Fetch login credentials to get the author_id
        login_credentials = collection_login_credentials.find_one({'registration_id': ObjectId(user_id)})
        if login_credentials:
            author_id = login_credentials['_id']
            
            # Fetch user's posts using the author_id from login credentials
            user_posts = list(collection_articles.find({'author_id': author_id}).sort('created_at', -1))
            
            # Process posts to add image_url and format dates
            for post in user_posts:
                post['_id'] = str(post['_id'])
                if 'image_public_id' in post:
                    post['image_url'] = get_image_url(post['image_public_id'])
                post['created_at'] = post['created_at'].strftime('%B %d, %Y')
            
            return render_template('admin/template/user_profile.html', user=user, posts=user_posts)
        else:
            return "User login credentials not found", 404
    else:
        return "User not found", 404

@app.route('/compose_mail')
@login_required
def compose_mail():
    user = get_current_user()
    if not user or not is_admin(user):
        return redirect(url_for('hello_world'))
    
    # Fetch all users grouped by their roles
    users = collection_login_credentials.find({}, {'_id': 1, 'email': 1, 'newser_user_roles': 1})
    for user in users:
        print(user['email'])
    # print(users)
    user_groups = {
        'admin': [],
        'moderator': [],
        'normal_user': []
    }
    
    for user in users:
        roles = user.get('newser_user_roles', ['normal_user'])
        email = user.get('email')
        if email:
            if 'admin' in roles:
                user_groups['admin'].append(email)
            elif 'moderator' in roles:
                user_groups['moderator'].append(email)
            else:
                user_groups['normal_user'].append(email)
    
    return render_template('admin/template/compose_mail.html', user_groups=user_groups,user=user)

@app.route('/send_email', methods=['POST'])
@login_required
def send_email():
    user = get_current_user()
    if not user or not is_admin(user):
        return redirect(url_for('hello_world'))

    subject = request.form.get('subject')
    recipient_groups = request.form.getlist('recipient_groups')
    quill_content = request.form.get('content')
    attachments = request.files.getlist('attachments')

    # Fetch all users' emails based on selected groups
    all_emails = []
    users = collection_login_credentials.find({}, {'_id': 1, 'email': 1, 'newser_user_roles': 1})
    for user in users:
        if user.get('email'):
            all_emails.append(user['email'])

    # Remove duplicates
    all_emails = list(set(all_emails))
    print(all_emails,"all_emails")
    # Save attachments temporarily
    temp_files = []
   

    try:
        send_mass_email(all_emails, subject, quill_content, temp_files)
        flash('Emails sent successfully!', 'success')
    except Exception as e:
        flash(f'Error sending emails: {str(e)}', 'error')
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)

    return redirect(url_for('compose_mail'))

@app.route('/posts')
@login_required
def posts_view():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin or moderator privileges
    # if not is_admin(user) and 'moderator' not in user.get('newser_user_roles', []):
    #     return redirect(url_for('hello_world'))
    
    return render_template('admin/template/posts.html', user=user)

@app.route('/get_posts')
@login_required
def get_posts():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin or moderator privileges
    # if not is_admin(user) and 'moderator' not in user.get('newser_user_roles', []):
    #     return redirect(url_for('hello_world'))

    page = int(request.args.get('page', 1))
    per_page = 16  # 4x4 grid
    skip = (page - 1) * per_page

    posts = list(collection_articles.find({}, {
        '_id': 1,
        'title': 1,
        'content': 1,
        'author': 1,
        'created_at': 1,
        'image_public_id': 1
    }).sort('created_at', -1).skip(skip).limit(per_page))

    for post in posts:
        post['_id'] = str(post['_id'])
        if 'image_public_id' in post:
            post['image_url'] = get_image_url(post['image_public_id'])
        post['created_at'] = post['created_at'].isoformat()

    total_posts = collection_articles.count_documents({})
    total_pages = (total_posts + per_page - 1) // per_page

    return jsonify({
        'posts': posts,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin or moderator privileges
    # if not is_admin(user) and 'moderator' not in user.get('newser_user_roles', []):
    #     return jsonify({'error': 'Unauthorized'}), 403

    try:
        result = collection_articles.delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Post deleted successfully'}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add routes for edit_post and view_post as needed



