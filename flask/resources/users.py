import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

@user.route('/', methods=['GET'])
def get_all_users():
    print('hey there')
    try:
        all_users = [model_to_dict(user) for user in models.User.select()]
        return jsonify(data=all_users, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

@user.route('/<userId>/', methods=['PUT'])
def update_user(userId):
    print('updating users')
    payload = request.get_json()
    if not current_user.is_authenticated:
        return jsonify(data={}, status={'code': 401, 'message':'You must be logged in to updates topic'})
    try:
        updated_user = models.User.update(
            email=payload['email'],
            password=payload['password']
        ).where(models.User.id==userId).execute()
        updated_user_dict = model_to_dict(models.User.get(id=userId))
        return jsonify(data=updated_user_dict, status={"code": 201, "message": "Article updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User to update does not exist'})
@user.route('/<id>/', methods=['GET'])
def get_one_user(id):
    
    if current_user.id != id:
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in!'})
    else:
        user = models.User.get_by_id(id)
        user_dict = model_to_dict(user)
        return jsonify(data=user_dict, status={'code': 200, 'message': 'This is the current user'})

@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()

    if not payload['email'] or not payload['password']:
        return jsonify(status=400)
    
    try:
        models.User.get(models.User.email ** payload['email'])
        return jsonify(data={}, status={'code': 400, 'message': 'A user with that email already exists.'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        new_user = models.User.create(**payload)
        login_user(new_user)

        user_dict = model_to_dict(new_user)
        print(user_dict, 'USER DICT')
        del user_dict['password']

        return jsonify(data=user_dict, status={'code': 201, 'message': 'User created'})

@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email ** payload['email'])
        user_dict = model_to_dict(user)
        if (check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(data=user_dict, status={'code': 200, 'message': 'User authenticated'})
        return jsonify(data=user_dict, status={'code': 401, 'message': 'Email or password are incorrect'})
    
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Email or password are incorrect'})

@user.route('/logout', methods=['GET'])
def logout():
    email = model_to_dict(current_user)['email']
    logout_user()

    return jsonify(data={}, status={'code': 200, 'message': "Successfully logged out {}".format(email)})

@user.route('/<userId>/', methods=['DELETE'])
def delete_user(userId):
    user_to_delete = models.User.get_by_id(userId)
    user_to_delete.delete_instance(recursive=True)
    return jsonify(data='User deleted successfully', status={'code': 200, 'message': 'deleted successfully'})
        
