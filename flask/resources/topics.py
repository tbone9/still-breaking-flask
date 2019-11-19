from flask import Blueprint, jsonify, request

topic = Blueprint('topics', 'topic')

@topic.route('/', methods=['GET'])
def get_all_topics():
    return 'Here are the topics!'