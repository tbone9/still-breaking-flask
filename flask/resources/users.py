import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
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