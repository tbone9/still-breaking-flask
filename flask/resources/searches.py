import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

search = Blueprint('searches', 'search')

# working/not tested
# index route
@search.route('/<topicId>/', methods=['GET'])
def index_search(topicId):
    print('indexing search')
    all_searches = [model_to_dict(n) for n in models.Search.select().where(models.Search.topic_id == topicId)]
    return jsonify(data=all_searches, status={'code': 200, 'message': 'Success'})
    try:
        all_searches = [model_to_dict(n) for n in models.Search.select().where(models.Note.topic_id == topicId)]
        return jsonify(data=all_searches, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'error getting notes'})

# working/not tested
# show route
@search.route('/show/<searchId>/', methods=['GET'])
def show_search(searchId):
    print('showing search')
    print(searchId)
    #if not current_user.is_authenticated: # Checks if user is logged in
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to view this article'})
    try:
        found_search = models.Search.get(id=searchId)
        search_dict = model_to_dict(found_note)
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
        return jsonify(data=search_dict,status={"code":"201","message":"search found"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Search to show does not exist'})

# working/not tested
# create route
@search.route('/<topicId>/', methods=['POST'])
def create_search(topicId):
    print('creating search')
    print(topicId)
    #if not current_user.is_authenticated:
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
    #if topic_dict.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
    #if not current_user.is_authenticated:
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
    #if topic_dict.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
    payload = request.get_json()
    payload['topic'] = topicId
    created_search = models.Search.create(**payload)
    print(created_search)
    search_dict = model_to_dict(created_search)
    return jsonify(data=search_dict,status={"code": "201", "message": "search saved"})

# working/not tested
# delete route
@search.route('/<searchId>/', methods=['DELETE'])
def delete_search(searchId):
    print('deleting search')
    try:
        search_to_delete = models.Search.get(id=searchId)
        #if not current_user.is_authenticated:
            #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
        #if article_to_delete.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only delete your own articles'})
        search_to_delete.delete_instance()
        return jsonify(data='note successfully deleted', status={"code": 200, "message": "note deleted successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Note to delete does not exist'})

@search.route('/<searchId>/', methods=['PUT'])
def update_search(searchId):
    print('updating search')
    try:
        payload = request.get_json()
        search = models.Search.get_by_id(searchId)
        search_dict = model_to_dict(search)
        #if not current_user.is_authenticated:
            #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only delete your own articles'})
        updated_search = models.Search.update(
            text=payload['text'],
        ).where(models.Search.id==searchId).execute()
        updated_search_dict = model_to_dict(models.Search.get(id=searchId))
        return jsonify(data=updated_search_dict, status={"code": 201, "message": "Search updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Search to update does not exist'})