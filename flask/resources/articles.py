import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

article = Blueprint('articles', 'article')

@article.route('/', methods=['GET'])
def get_all_articles():
    return 'Here are the articles!'