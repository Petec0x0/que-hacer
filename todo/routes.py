from todo import app, db
from flask import request, jsonify
from todo.models import User, Todo
from werkzeug.security import generate_password_hash, check_password_hash
import uuid # for generating users unique public ID



@app.route('/')
def home():
    return jsonify({'error':False, 'message':'Hello'})


# route for adding new user
@app.route('/user/create', methods=['POST'])
def create_user():
    # fetch post request data
    data = request.get_json()
    # create an object for a new user
    new_user = User(public_id=uuid.uuid4(), username=data['username'], email=data['email'], 
                    password=generate_password_hash(data['password']))
    # add the user to the database and commit
    db.session.add(new_user)
    db.session.commit()

    # return a success message after commit
    return jsonify({'error':False, 'message':'User Sucessfully'})

@app.route('/users', methods=['GET'])
def all_user():
    # get all user 
    users = User.query.all()
    
    # jsonify user data
    output = []
    for user in users:
        each_user = {}
        each_user['public_id'] = user['public_id']
        each_user['username'] = user['username']
        each_user['email'] = user['email']
        each_user['password'] = user['password']
        each_user['is_admin'] = user['is_admin']
        output.append(each_user)

    return jsonify({'users':output, 'error':False})

@app.route('/user/<public_id>', methods=['GET'])
def get_user(public_id):
    # get a particular user data
    user = User.query.filter_by(public_id=public_id).first()
    # jsonify user data
    each_user = {}
    each_user['public_id'] = user['public_id']
    each_user['username'] = user['username']
    each_user['email'] = user['email']
    each_user['password'] = user['password']
    each_user['is_admin'] = user['is_admin']

    return jsonify({'user':each_user, 'error':False})
