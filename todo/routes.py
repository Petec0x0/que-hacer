from todo import app, db
from flask import request, jsonify, make_response
import todo
from todo.models import User, Todo
from werkzeug.security import generate_password_hash, check_password_hash
import uuid # for generating users unique public ID
import jwt
import datetime
from functools import wraps
from flask_cors import cross_origin


# decorator for authorization
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # check if the token exists in the request header
        if 'X-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return an error message if there is no token
        if not token:
            return jsonify({'error':True, 'message' : 'Token is missing!'}), 401
        # decode the token if it exists in a try except
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'error':True, 'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



"""
   THE USER ROUTES 
"""
# this route gets all the available users in the database
@app.route('/users', methods=['GET'])
@token_required
def all_user(current_user):
    # make sure only the admin has access to this endpoint
    if not current_user.is_admin:
        return jsonify({'message':'Unauthorized Access', 'error':True}), 401

    # get all user 
    users = User.query.all()
    
    # jsonify user data
    output = []
    for user in users:
        each_user = {}
        each_user['public_id'] = user.public_id
        each_user['username'] = user.username
        each_user['email'] = user.email
        each_user['password'] = user.password
        each_user['is_admin'] = user.is_admin
        output.append(each_user)

    return jsonify({'users':output, 'error':False})

# get a particular user
@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user, public_id):
    # get a particular user data
    user = User.query.filter_by(public_id=public_id).first()
    # jsonify user data
    each_user = {}
    each_user['public_id'] = user.public_id
    each_user['username'] = user.username
    each_user['email'] = user.email
    each_user['password'] = user.password
    each_user['is_admin'] = user.is_admin

    return jsonify({'user':each_user, 'error':False})

# this route promotes a user to admin
@app.route('/user/promote/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    # make sure only the admin has access to this endpoint
    if not current_user.is_admin:
        return jsonify({'message':'Unauthorized Access', 'error':True}), 401

    # get a particular user data
    user = User.query.filter_by(public_id=public_id).first()
    # make sure the exists before proceding
    if not user:
        return jsonify({'message':'User Not Found', 'error':True})
    
    # promote user to admin
    user.is_admin = True

    # commit the changes made
    db.session.commit()

    return jsonify({'message':'User Promoted Successfully', 'error':False})


"""
    THE TODOS ROUTES
"""
# route for creating a todo
@app.route('/todo/create', methods=['POST'])
@token_required
def create_todo(current_user):
    # get request data
    data = request.get_json(force=True)

    # create a todo object
    new_todo = Todo(body=data['body'], reminder=data['reminder'], creator=current_user.id)

    # add todo to the database and commit
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message':'Todo Created Successfully', 'error':False})


# route for todos of a particular user
@app.route('/todo/get', methods=['GET'])
@token_required
def get_todo(current_user):
    todos = Todo.query.filter_by(creator=current_user.id)

    if not todos:
        return jsonify({'message':'Todos Not Found', 'error':True})

    # iterate through all todos if available
    output = []
    for todo in todos:
        each_todo = {}
        each_todo['id'] = todo.id
        each_todo['body'] = todo.body
        each_todo['completed'] = todo.completed
        each_todo['reminder'] = todo.reminder
        output.append(each_todo)
    
    # return the available todos
    return jsonify({'todos':output, 'error':False})

# route for marking a todo as complete
@app.route('/todo/complete', methods=['PUT'])
@token_required
def complete_todo(current_user):
    # get PUT request data
    data = request.get_json(force=True)

    # get the todo object
    todo = Todo.query.filter_by(id=data['todo_id'], creator=current_user.id).first()
    # check if todo exists
    if not todo:
        return jsonify({'message':'Todo Not Found', 'error':True})

    # update and commit changes
    todo.completed = True
    db.session.commit()

    return jsonify({'message':'Todo Marked as Complete', 'error':False})

# route for deleting a todo
@app.route('/todo/delete', methods=['DELETE'])
@token_required
def delete_todo(current_user):
    # get DELETE request data
    data = request.get_json(force=True)

    # get the todo object
    todo = Todo.query.filter_by(id=data['todo_id'], creator=current_user.id).first()
    # check if todo exists
    if not todo:
        return jsonify({'message':'Todo Not Found', 'error':True})

    # delete todo and commit
    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message':'Todo Deleted Successfully', 'error':False})


"""
    THE AUTHENTICATION ROUTES
"""
# the signup route
@app.route('/auth/signup', methods=['POST'])
@cross_origin()
def signup():
    # fetch post request data
    data = request.get_json(force=True)
    # create an object for a new user
    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], email=data['email'], 
                    password=generate_password_hash(data['password']))
    # add the user to the database and commit
    db.session.add(new_user)
    db.session.commit()

    # return a success message after commit
    # response = make_response(jsonify({'error':False, 'message':'User Created Sucessfully'}))
    # response.headers["Access-Control-Allow-Origin"] = "*"
    # return response
    return jsonify({'error':False, 'message':'User Created Sucessfully'})


# the login route
@app.route('/auth/login', methods=['POST'])
def login():
    # get login data from Authorization header
    auth = request.authorization
    # making the username and password exists on the authorization header
    if not auth or not auth.username or not auth.password:
        # return an error message
        return make_response(
            {'error':True,'message':'Could not verify 1'}, 
            401, 
            {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    # fetch user with the provided username
    user = User.query.filter_by(username=auth.username).first()

    if not user:
        # return an error message if user does not exist
        return make_response(
            {'error':True,'message':'Could not verify 2'}, 
            401, 
            {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # create a JWT token if user password is correct
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
            'public_id' : user.public_id, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.config['SECRET_KEY'], "HS256")

        return jsonify({'token' : token, 'error':False, 'message':'Login Success'})

    # return an error message if the password is incorrect
    return make_response(
            {'error':True,'message':'Could not verify 3'}, 
            401, 
            {'WWW-Authenticate' : 'Basic realm="Login required!"'})