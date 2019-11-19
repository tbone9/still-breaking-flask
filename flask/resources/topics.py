import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

topic = Blueprint('topics', 'topic')

@topic.route('/', methods=['GET'])
def get_all_topics():
    return 'Here are the topics!'