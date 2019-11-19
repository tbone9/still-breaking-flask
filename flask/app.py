from flask import Flask, request, jsonify, g
from flask_cors import CORS
from resources.users import user
from resources.topics import topic
from resources.articles import article


DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/user')

CORS(topic, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(topic, url_prefix='/api/v1/topic')

CORS(article, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(article, url_prefix='/api/v1/article')

# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)