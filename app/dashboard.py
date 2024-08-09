from flask import Blueprint, render_template, session, redirect, url_for,request
from flask import jsonify
from app import collection_user_registration
from app.utils import get_weather_data
from functools import wraps
from . import app
from bson import ObjectId

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
 
@app.route('/dashboard')
@login_required
def dashboard_view():
   
  
    # print(user['address'])
    # weather_data = get_weather_data(user['address'])
    return render_template('admin/template/index.html')
from datetime import datetime

@app.route('/get_users')
@login_required
def get_users():
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
        'status': 1
    }).skip(skip).limit(per_page))

    for user in users:
        user['_id'] = str(user['_id'])
        # Convert DOB to age
        if user['dob']:
            print(user['dob'])
            try:
                dob = datetime.strptime(user['dob'], '%Y-%m-%d')
                today = datetime.now()

                # print(int(today.year)-int(dob.year))
               
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                print(age)
                user['age'] = age
            except ValueError:
                user['age'] = 'N/A'
        else:
            user['age'] = 'N/A'
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
    return render_template('admin/template/users.html')

@app.route('/temp')
@login_required
def temp_view():
    return render_template('admin/template/temp.html')

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

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        # Handle the POST request to save the new post
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.getlist('category')  # Assuming multiple categories can be selected
        post_type = request.form.get('post_type')
        
        # Here you would typically save this data to your database
        # For example:
        # new_post = {
        #     'title': title,
        #     'content': content,
        #     'category': category,
        #     'type': post_type,
        #     'author_id': session['user_id'],
        #     'created_at': datetime.now()
        # }
        # collection_posts.insert_one(new_post)
        
        # After saving, redirect to a success page or back to the post list
        return redirect(url_for('dashboard_view'))
    
    # If it's a GET request, just render the add_post template
    return render_template('admin/template/add_post.html')