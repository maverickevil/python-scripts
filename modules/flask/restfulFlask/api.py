# -*- coding: utf-8 -*-

# =======================================================================
# FuncName: api.py
# Desc: A simple flask restful api service
# Date: 2022-09-09 18:48
# Author: Pokeya
# =======================================================================

__author__ = 'Mystic'


import logging

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort


BEARER_TOKEN = "026914e3-675f-41d9-853b-a8d9d290f3a8"


# Define a Handler and set a format which output to console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


app = Flask(__name__)
api = Api(app, default_mediatype='application/json')

parser = reqparse.RequestParser()
parser.add_argument('data', required=True, help='Data cannot be blank!')


class Collector(Resource):
    def post(self):
        authorization = request.headers.get("Authorization")
        if authorization != 'Bearer {}'.format(BEARER_TOKEN):
            msg = 'token authentication failed'
            logging.info(f'403 Forbidden: {msg}')
            data = {
                'code': 4000,
                'msg': 'failed',
                'detail': msg,
            }
            abort(http_status_code=403, **data)

        result = parser.parse_args().get('data')
        logging.info(str(result))
        data = {
            'code': 0,
            'msg': 'success',
            'data': eval(result),
        }
        return jsonify(data)


# Setup the Api resource routing
url = '/api/info'
api.add_resource(Collector, url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)


"""
Add dependencies:
➜ pip install flask
➜ pip install flask_restful

Send request: 
➜ curl --location --request POST 'http://127.0.0.1:5000/api/info' \
--header 'Authorization: Bearer 026914e3-675f-41d9-853b-a8d9d290f3a8' \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "xiao cai",
        "age": 26,
        "hobby": ["Sing", "Jump", "Rap"]
    }
}'
{
    "code": 0,
    "msg": "success",
    "data": {
        "name": "xiao cai",
        "age": 26,
        "hobby": [
            "Sing",
            "Jump",
            "Rap"
        ]
    }
}
"""
