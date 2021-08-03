from todo import app, db
from flask import request, jsonify
import todo
from todo.models import User, Todo
from werkzeug.security import generate_password_hash, check_password_hash
import uuid # for generating users unique public ID
from sqlalchemy import and_

"""
   THE USER ROUTES 
"""
# route for adding new user
@app.route('/user/create', methods=['POST'])
def create_user():
    # fetch post request data
    data = request.get_json(force=True)
    # create an object for a new user
    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], email=data['email'], 
                    password=generate_password_hash(data['password']))
    # add the user to the database and commit
    db.session.add(new_user)
    db.session.commit()

    # return a success message after commit
    return jsonify({'error':False, 'message':'User Created Sucessfully'})

# this route gets all the available users in the database
@app.route('/users', methods=['GET'])
def all_user():
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
def get_user(public_id):
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
def promote_user(public_id):
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
def create_todo():
    # get request data
    data = request.get_json(force=True)

    # create a todo object
    new_todo = Todo(body=data['body'], reminder=data['reminder'], creator=data['creator'])

    # add todo to the database and commit
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message':'Todo Created Successfully', 'error':False})


# route for todos of a particular user
@app.route('/todo/get/<user_id>', methods=['GET'])
def get_todo(user_id):
    todos = Todo.query.filter_by(creator=user_id)

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
def complete_todo():
    # get PUT request data
    data = request.get_json(force=True)

    # get the todo object
    todo = Todo.query.filter_by(id=data['id'], creator=data['user_id']).first()
    # check if todo exists
    if not todo:
        return jsonify({'message':'Todo Not Found', 'error':True})

    # update and commit changes
    todo.completed = True
    db.session.commit()

    return jsonify({'message':'Todo Marked as Complete', 'error':False})

# route for deleting a todo
@app.route('/todo/delete', methods=['DELETE'])
def delete_todo():
    # get DELETE request data
    data = request.get_json(force=True)

    # get the todo object
    todo = Todo.query.filter_by(id=data['id'], creator=data['user_id']).first()
    # check if todo exists
    if not todo:
        return jsonify({'message':'Todo Not Found', 'error':True})

    # delete todo and commit
    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message':'Todo Deleted Successfully', 'error':False})

