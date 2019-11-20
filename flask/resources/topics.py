import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

topic = Blueprint('topics', 'topic')

@topic.route('/', methods=['GET'])
def get_all_topics():
    try:
        all_topics = [model_to_dict(topic) for topic in models.Topic.select()]
        return jsonify(data=all_topics, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

#create topic
@topic.route('/', methods=['POST'])
def create_topic():
    print('topic create route')
    payload = request.get_json()
    if not current_user.is_authenticated: # Check if user is authenticated and allowed to create a new dog
        print(current_user)
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a topic'})
    payload['user'] = current_user.id
    created_topic = models.Topic.create(**payload)
    created_topic_dict = model_to_dict(create_topic)
    return jsonify(status={'code': 201, 'msg': 'success'}, data=created_topic_dict)
    
