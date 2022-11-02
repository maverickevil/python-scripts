import flask_restful
from src.views import Test


api = flask_restful.Api(default_mediatype='application/json')

# Setup the Api resource routing
api.add_resource(Test, '/api/test')

