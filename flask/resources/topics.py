import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

topic = Blueprint('topics', 'topic')

@topic.route('/', methods=['GET'])
def get_user_topics():
    try:
        this_users_topics = models.Topic.select().where(models.Topic.user_id == current_user.id)

        this_users_topics = [model_to_dict(topic) for topic in this_users_topics
        ]
        print(this_users_topics)
        return jsonify(data=this_users_topics, status={'code': 200, 'message': 'Success'})
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
    create_topic_dict = model_to_dict(created_topic)
    return jsonify(status={'code': 201, 'msg': 'success'}, data=create_topic_dict)


# delete route
@topic.route('/<id>/', methods=['DELETE'])
# @login_required
def delete_topic(id):
    
    topic_to_delete = models.Topic.get_by_id(id)

    if topic_to_delete.user.id != current_user.id:
        return jsonify(data="Forbidden", status={'code': 403, 'message': "User can only delete their own dogs."})
    else:
        topic_name = topic_to_delete.name
        topic_to_delete.delete_instance()
        return jsonify(data='Topic successfully deleted', status={"code": 200, "message": "{} deleted successfully".format(topic_name)})
