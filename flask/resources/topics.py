import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

topic = Blueprint('topics', 'topic')

@topic.route('/', methods=['GET'])
def get_user_topics():
    print('topic index route')
    try:
        this_users_topics = models.Topic.select().where(models.Topic.user_id == current_user.id)

        this_users_topics = [model_to_dict(topic) for topic in this_users_topics]

        print(this_users_topics)
        return jsonify(data=this_users_topics, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

# working/not tested
# show route
@topic.route('/<topicId>/',methods=['GET'])
def show_topic(topicId):
    if not current_user.is_authenticated: # Checks if user is logged in
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to view this topic'})
    try:
        found_topic = models.Topic.get(id=topicId)
        topic_dict = model_to_dict(found_topic)
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
        return jsonify(data=topic_dict,status={"code":"201","message":"topic found"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Topic to show does not exist'})

#create topic
@topic.route('/', methods=['POST'])
def create_topic():
    print('topic create route')
    
    if not current_user.is_authenticated:
        print(current_user, 'NOT ALLOWED')
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a topic'})
    payload = request.get_json()
    payload['user'] = current_user.id
    created_topic = models.Topic.create(**payload)
    create_topic_dict = model_to_dict(created_topic)
    return jsonify(status={'code': 201, 'msg': 'success'}, data=create_topic_dict)
    
# update route
@topic.route('/<topicId>/', methods=['PUT'])
def update_topic(topicId):
    print('topic edit route')
    payload = request.get_json()
    if not current_user.is_authenticated:
        return jsonify(data={}, status={'code': 401, 'message':'You must be logged in to updates topic'})
    try:
        topic = models.Topic.get_by_id(topicId)
        topic_dict = model_to_dict(topic)
        print(topic_dict, 'TOPIC DICT')
        if topic_dict.user.id is not current_user.id: 
            return jsonify(data={}, status={'code': 401, 'message': 'You can only update your own articles'})
        updated_topic = models.Topic.update(
                name=payload['name'],
                description=payload['description'],
            ).where(models.Topic.id==topicId).execute()
        updated_topic_dict = model_to_dict(models.Topic.get(id=topicId))
        return jsonify(data=updated_topic_dict, status={"code": 201, "message": "Topic updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Topic to update does not exist'})
      

# delete route
@topic.route('/<id>/', methods=['DELETE'])
# @login_required
def delete_topic(id):
    
    topic_to_delete = models.Topic.get_by_id(id)

    if topic_to_delete.user.id != current_user.id:
        return jsonify(data="Forbidden", status={'code': 403, 'message': "User can only delete their own topics."})
    else:
        topic_name = topic_to_delete.name
    # articles_to_delete = models.Article.select().where(models.Article.topic.user.id == current_user.id)
    
    # articles_to_delete.delete()
    topic_to_delete.delete_instance(recursive=True)
    return jsonify(data='Topic successfully deleted', status={"code": 200, "message": "{} deleted successfully".format(topic_name)})
