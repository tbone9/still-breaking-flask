import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

topic = Blueprint('topics', 'topic')

@topic.route('/', methods=['GET'])
def get_all_topics():
    return 'Here are the topics!'

#create topic
@topic.route('/', methods=['POST'])
def create_topic():
    print('topic create route')
    payload = request.get_json()
    created_topic = models.Topic.create(**payload)
    created_topic_dict = model_to_dict(create_topic)
    return jsonify(status={'code': 201, 'msg': 'success'}, data=created_topic_dict)
    
