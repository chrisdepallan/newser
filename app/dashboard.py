from flask import Blueprint, render_template, session, redirect, url_for,request
from flask import jsonify,flash
from app import collection_user_registration,collection_articles,collection_login_credentials,collection_subscriptions
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




#ai agent function imports
from app import openai
from datetime import datetime
from bson import ObjectId
# Define a function to retrieve data from the database using username
def get_user_data(username):
    # Fetch login credentials using the username
    login_data = collection_login_credentials.find_one({"username": username})
    if not login_data:
        return {"status": "error", "message": "User not found"}

    # Convert ObjectId fields to strings
    login_data['_id'] = str(login_data['_id'])
    login_data['registration_id'] = str(login_data['registration_id'])

    # Fetch user details from the registration table using registration_id
    registration_data = collection_user_registration.find_one({'_id': ObjectId(login_data['registration_id'])}, {
        '_id': 1,
        'full_name': 1,
        'phone_number': 1,
        'address': 1,
        'dob': 1,
        'avatar': 1,
        'status': 1,
        'newser_user_roles': 1
    })

    if not registration_data:
        return {"status": "error", "message": "User registration details not found"}

    # Convert ObjectId to string for JSON serialization
    registration_data['_id'] = str(registration_data['_id'])

    # Combine login and registration data
    user_data = {
        'username': login_data.get('username', 'N/A'),
        'email': login_data.get('email', 'N/A'),
        'registration_id': login_data['registration_id'],
        'full_name': registration_data.get('full_name', 'N/A'),
        'phone_number': registration_data.get('phone_number', 'N/A'),
        'address': registration_data.get('address', 'N/A'),
        'dob': registration_data.get('dob', 'N/A'),
        'avatar': registration_data.get('avatar', 'https://via.placeholder.com/150'),
        'status': registration_data.get('status', 'N/A'),
        'roles': registration_data.get('newser_user_roles', [])
    }

    # Convert DOB to age if available
    if user_data['dob'] != 'N/A':
        try:
            dob = datetime.strptime(user_data['dob'], '%Y-%m-%d')
            today = datetime.now()
            user_data['age'] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except ValueError:
            user_data['age'] = 'N/A'
    else:
        user_data['age'] = 'N/A'

    return {"status": "success", "data": user_data}

# Define a function to retrieve the first or last n users
def get_users(limit, order="asc"):
    sort_order = 1 if order == "asc" else -1  # Ascending or descending order

    # Fetch users from the registration table
    registration_users = list(collection_user_registration.find({}, {
        '_id': 1,
        'full_name': 1,
        'phone_number': 1,
        'address': 1,
        'dob': 1,
        'avatar': 1,
        'status': 1,
        'newser_user_roles': 1
    }).sort("_id", sort_order).limit(limit))

    users = []

    for reg_user in registration_users:
        # Convert ObjectId to string for JSON serialization
        reg_user['_id'] = str(reg_user['_id'])

        # Fetch login credentials using the registration_id
        login_data = collection_login_credentials.find_one({'registration_id': ObjectId(reg_user['_id'])}, {
            'username': 1,
            'email': 1
        })
        print(login_data)

        # Add login data to the user details
        user = {
            '_id': reg_user.get('_id', 'N/A'),
            'full_name': reg_user.get('full_name', 'N/A'),
            'phone_number': reg_user.get('phone_number', 'N/A'),
            'address': reg_user.get('address', 'N/A'),
            'dob': reg_user.get('dob', 'N/A'),
            'avatar': reg_user.get('avatar', 'https://via.placeholder.com/150'),
            'status': reg_user.get('status', 'N/A'),
            'roles': reg_user.get('newser_user_roles', []),
            'username': login_data.get('username', 'N/A') if login_data else 'N/A',
            'email': login_data.get('email', 'N/A') if login_data else 'N/A'
        }

        # Convert DOB to age if available
        if user['dob'] != 'N/A':
            try:
                dob = datetime.strptime(user['dob'], '%Y-%m-%d')
                today = datetime.now()
                user['age'] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            except ValueError:
                user['age'] = 'N/A'
        else:
            user['age'] = 'N/A'

        users.append(user)

    if users:
        return {"status": "success", "data": users}
    else:
        return {"status": "error", "message": "No users found"}


# Define a function to retrieve payment data based on filters
def get_payment_data(username=None, start_date=None, end_date=None, min_amount=None, max_amount=None):
    query = {}

    # Filter by username
    if username:
        # Fetch the user_id from login_credentials using the username
        login_data = collection_login_credentials.find_one({"username": username}, {"_id": 1})
        if not login_data:
            return {"status": "error", "message": "User not found"}
        query["user_id"] = str(login_data["_id"])

    # Filter by date range
    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            date_filter["$lte"] = datetime.strptime(end_date, "%Y-%m-%d")
        query["date"] = date_filter

    # Filter by payment amount
    if min_amount or max_amount:
        amount_filter = {}
        if min_amount:
            amount_filter["$gte"] = min_amount
        if max_amount:
            amount_filter["$lte"] = max_amount
        query["amount"] = amount_filter

    # Fetch payment data from the collection
    payments = list(collection_subscriptions.find(query, {
        "_id": 1,
        "user_id": 1,
        "amount": 1,
        "date": 1,
        "session_id": 1,
        "status": 1
    }))

    # Convert ObjectId to string and format the date
    for payment in payments:
        payment["_id"] = str(payment["_id"])
        payment["user_id"] = str(payment["user_id"])
        payment["date"] = payment["date"].strftime("%Y-%m-%d %H:%M:%S")
    # print(payments,"payments")
    if payments:
        return {"status": "success", "data": payments}
    else:
        return {"status": "error", "message": "No payments found"}

# Update handle_openai_function_calling to return HTML cards
def handle_openai_function_calling(prompt):
    response = openai.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        functions=[
            {
                "name": "get_user_data",
                "description": "Retrieve user data from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "The username of the user"}
                    },
                    "required": ["username"]
                }
            },
            {
                "name": "get_users",
                "description": "Retrieve the first or last n users from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "The number of users to retrieve"},
                        "order": {
                            "type": "string",
                            "description": "The order of retrieval ('asc' for first n users, 'desc' for last n users)",
                            "enum": ["asc", "desc"]
                        }
                    },
                    "required": ["limit", "order"]
                }
            },
            {
                "name": "get_payment_data",
                "description": "Retrieve payment data for subcriptions based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "The username of the user", "nullable": True},
                        "start_date": {"type": "string", "description": "Start date for filtering payments (YYYY-MM-DD)", "nullable": True},
                        "end_date": {"type": "string", "description": "End date for filtering payments (YYYY-MM-DD)", "nullable": True},
                        "min_amount": {"type": "number", "description": "Minimum payment amount", "nullable": True},
                        "max_amount": {"type": "number", "description": "Maximum payment amount", "nullable": True}
                    }
                }
            }
        ],
        function_call="auto"
    )

    if response.choices[0].finish_reason == "function_call":
        function_call = response.choices[0].message.function_call
        if function_call.name == "get_user_data":
            username = json.loads(function_call.arguments)["username"]
            user_data = get_user_data(username)
            if user_data["status"] == "success":
                user = user_data["data"]
                return f"""
                <div class="card">
                    <img src="{user['avatar']}" class="card-img-top rounded-circle" alt="Avatar" style="width: 50px; height: 50px; object-fit: cover; margin: auto; display: block;">
                    <div class="card-body">
                        <h5 class="card-title">{user['full_name']}</h5>
                        <p class="card-text"><strong>Username:</strong> {user['username']}</p>
                        <p class="card-text"><strong>Email:</strong> {user['email']}</p>
                        <p class="card-text"><strong>Phone:</strong> {user['phone_number']}</p>
                        <p class="card-text"><strong>Address:</strong> {user['address']}</p>
                        <p class="card-text"><strong>Status:</strong> {user['status']}</p>
                        <p class="card-text"><strong>Roles:</strong> {', '.join(user['roles'])}</p>
                        <p class="card-text"><strong>Age:</strong> {user['age']}</p>
                    </div>
                </div>
                """
            else:
                return f"<div class='alert alert-danger'>{user_data['message']}</div>"
        elif function_call.name == "get_users":
            args = json.loads(function_call.arguments)
            limit = args["limit"]
            order = args["order"]
            users_data = get_users(limit, order)
            if users_data["status"] == "success":
                users = users_data["data"]
                cards = ""
                for user in users:
                    cards += f"""
                    <div class="col-md-4">
                        <div class="card">
                            <img src="{user['avatar']}" class="card-img-top rounded-circle" alt="Avatar" style="width: 50px; height: 50px; object-fit: cover; margin: auto; display: block;">
                            <div class="card-body">
                                <h5 class="card-title">{user['full_name']}</h5>
                                <p class="card-text"><strong>Username:</strong> {user['username']}</p>
                                <p class="card-text"><strong>Email:</strong> {user.get('email', 'N/A')}</p>
                                <p class="card-text"><strong>Phone:</strong> {user.get('phone_number', 'N/A')}</p>
                                <p class="card-text"><strong>Address:</strong> {user.get('address', 'N/A')}</p>
                                <p class="card-text"><strong>Status:</strong> {user.get('status', 'N/A')}</p>
                                <p class="card-text"><strong>Roles:</strong> {', '.join(user.get('roles', []))}</p>
                            </div>
                        </div>
                    </div>
                    """
                return f"<div class='row'>{cards}</div>"
            else:
                return f"<div class='alert alert-danger'>{users_data['message']}</div>"
        elif function_call.name == "get_payment_data":
            args = json.loads(function_call.arguments)
            username = args.get("username")
            start_date = args.get("start_date")
            end_date = args.get("end_date")
            min_amount = args.get("min_amount")
            max_amount = args.get("max_amount")
            payments_data = get_payment_data(username, start_date, end_date, min_amount, max_amount)
            if payments_data["status"] == "success":
                payments = payments_data["data"]
                rows = ""
                for payment in payments:
                    rows += f"""
                    <tr>
                        <td>{payment['_id']}</td>
                        <td>{payment['user_id']}</td>
                        <td>{payment['amount']}</td>
                        <td>{payment['date']}</td>
                        <td>{payment['_id']}</td>
                    </tr>
                    """
                return f"""
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Payment ID</th>
                            <th>User ID</th>
                            <th>Amount</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                """
            else:
                return f"<div class='alert alert-danger'>{payments_data['message']}</div>"

    return f"<div class='alert alert-info'>{response.choices[0].message.content}</div>"

# Update /admin/agent to return HTML
@app.route('/admin/agent', methods=['POST'])
def admin_agent():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin privileges
    if not is_admin(user):
        return redirect(url_for('hello_world'))
    
    if request.method == 'POST':
        user_input = request.json.get('message', '').strip()
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        try:
            response_html = handle_openai_function_calling(user_input)
            return jsonify({'html': response_html}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Add routes for edit_post and view_post as needed

@app.route("/agent", methods=['GET', 'POST'])
def agent_view():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Check if user has admin privileges
    if not is_admin(user):
        return redirect(url_for('hello_world'))
    
    return render_template('admin/template/adminagent.html', user=user)

