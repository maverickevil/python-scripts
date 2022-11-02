from flask import jsonify
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('data', required=True, help='Data cannot be blank!')

class Test(Resource):
    def get(self):
        result = {
            "code": 0,
            "msg": "success",
            "data": {
                "ok": "≤‚ ‘≥…π¶",
            },
        }
        return jsonify(result)

