import models
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from resources.users import user
from resources.topics import topic
from resources.articles import article
from resources.notes import note
from flask_login import LoginManager

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.secret_key = ';laskjfla;skfjower;lksf'
app.cors_headers = 'Content-Type'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(data={
      'error': 'User not logged in.'
    }, status={
      'code': 401,
      'message': "You must be logged in to access that resource."
    }), 401

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

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

CORS(note, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(note, url_prefix='/api/v1/note')

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)