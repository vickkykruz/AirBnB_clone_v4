#!/usr/bin/python3
"""
This script file that contains the principal application
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, render_template
from os import environ
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
# cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(obj):
    """ This is a method that calls methods close() """
    storage.close()


@app.errorhandler(404)
def page_not_foun(error):
    """ This is a method that loads a custom 404 page not found """
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This is the api that was created for the hbnb api project,\
    all the documentation will be shown below',
    'diversion': 3}

Swagger(app)

if __name__ == "__main__":

    host = environ.get('HBNB_API_HOST', default='0.0.0.0')
    port = environ.get('HBNB_API_PORT', default=5000)

    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
