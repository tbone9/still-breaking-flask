from flask import Blueprint, jsonify, request

article = Blueprint('articles', 'article')

@article.route('/', methods=['GET'])
def get_all_articles():
    return 'Here are the articles!'