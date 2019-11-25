import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

note = Blueprint('notes', 'note')

# working/not tested
# index route
@note.route('/<articleId>/', methods=['GET'])
def index_note(articleId):
    print('indexing notes')
    all_notes = [model_to_dict(n) for n in models.Note.select().where(models.Note.article_id == articleId)]
    return jsonify(data=all_notes, status={'code': 200, 'message': 'Success'})
    try:
        all_notes = [model_to_dict(n) for n in models.Note.select().where(models.Note.article_id == articleId)]
        return jsonify(data=all_notes, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'error getting notes'})

# working/not tested
# show route
@note.route('/show/<noteId>/', methods=['GET'])
def show_note(noteId):
    print('showing note')
    print(noteId)
    #if not current_user.is_authenticated: # Checks if user is logged in
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to view this article'})
    try:
        found_note = models.Note.get(id=noteId)
        note_dict = model_to_dict(found_note)
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
        return jsonify(data=note_dict,status={"code":"201","message":"note found"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Note to show does not exist'})

# working/not tested
# create route
@note.route('/<articleId>/', methods=['POST'])
def create_note(articleId):
    print(articleId)
    #if not current_user.is_authenticated:
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
    #if topic_dict.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
    #if not current_user.is_authenticated:
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
    #if topic_dict.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
    payload = request.get_json()
    payload['article'] = articleId
    created_note = models.Note.create(**payload)
    note_dict = model_to_dict(created_note)
    return jsonify(data=note_dict,status={"code": "201", "message": "note saved"})
    print(create_note)

# TODO not working
# delete route
@note.route('/<noteId>/', methods=['DELETE'])
def delete_note(noteId):
    print('deleting note')
    try:
        note_to_delete = models.Note.get(id=noteId)
        #if not current_user.is_authenticated:
            #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
        #if article_to_delete.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only delete your own articles'})
        note_to_delete.delete_instance()
        return jsonify(data='note successfully deleted', status={"code": 200, "message": "note deleted successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Note to delete does not exist'})

@note.route('/<noteId>/', methods=['PUT'])
def update_note(noteId):
    print('updating note')
    try:
        payload = request.get_json()
        note = models.Note.get_by_id(noteId)
        note_dict = model_to_dict(note)
        #if not current_user.is_authenticated:
            #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only delete your own articles'})
        updated_note = models.Note.update(
            #topic=payload['topic'],
            title=payload['title'],
            text=payload['text'],
        ).where(models.Note.id==noteId).execute()
        updated_note_dict = model_to_dict(models.Note.get(id=noteId))
        return jsonify(data=updated_note_dict, status={"code": 201, "message": "Note updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Note to update does not exist'})