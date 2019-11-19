from flask import Blueprint, jsonify, request

user = Blueprint('users', 'user')

@user.route('/', methods=['GET'])
def get_user():
    print('hey there')
    return 'Hey There'