import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

article = Blueprint('articles', 'article')

# index route
@article.route('/<topicId>/', methods=['GET'])
def index_articles(topicId):
    #if not current_user.is_authenticated: # Checks if user is logged in
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to view articles'})
    try:
        all_articles = [model_to_dict(a) for a in models.Article.select().where(models.Article.topic_id == topicId)]
        return jsonify(data=all_articles, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

# working/not tested
# show route
@article.route('/show/<articleId>/',methods=['GET'])
def show_article(articleId):
    #if not current_user.is_authenticated: # Checks if user is logged in
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to view this article'})
    try:
        found_article = models.Article.get(id=articleId)
        article_dict = model_to_dict(found_article)
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
        return jsonify(data=article_dict,status={"code":"201","message":"article found"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Article to show does not exist'})

#working/not tested
# create route
@article.route('/<topicId>/', methods=['POST'])
def create_article(topicId):
    print(topicId)
    topic = models.Topic.get_by_id(topicId)
    topic_dict = model_to_dict(topic)
    #if not current_user.is_authenticated:
        #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
    #if topic_dict.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only add articles to your own topics'})
    payload = request.get_json()
    payload['topic'] = topicId
    created_article = models.Article.create(**payload)
    article_dict = model_to_dict(created_article)
    return jsonify(data=article_dict,status={"code": "201", "message": "article saved"})
    print(create_article)
# working/not tested
# delete route
@article.route('/<articleId>/', methods=['DELETE'])
def delete_article(articleId):
    try:
        article_to_delete = models.Article.get(id=articleId)
        #if not current_user.is_authenticated:
            #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
        #if article_to_delete.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only delete your own articles'})
        article_to_delete.delete_instance()
        return jsonify(data='article successfully deleted', status={"code": 200, "message": "article deleted successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Article to delete does not exist'})
# working/not tested
# update route
@article.route('/<articleId>/', methods=['PUT'])
def update_article(articleId):
    try:
        payload = request.get_json()
        article = models.Article.get_by_id(articleId)
        article_dict = model_to_dict(article)
        #if not current_user.is_authenticated:
            #return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to save an article'})
        #if article_dict.topic.user.id is not current_user.id: 
            #return jsonify(data={}, status={'code': 401, 'message': 'You can only delete your own articles'})
        updated_article = models.Article.update(
            #topic=payload['topic'],
            source=payload['source'],
            title=payload['title'],
            description=payload['description'],
            url=payload['url'],
            urlToImage=payload['urlToImage'],
            publishedAt=payload['publishedAt'],
        ).where(models.Article.id==articleId).execute()
        updated_article_dict = model_to_dict(models.Article.get(id=articleId))
        return jsonify(data=updated_article_dict, status={"code": 201, "message": "Article updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Article to update does not exist'})