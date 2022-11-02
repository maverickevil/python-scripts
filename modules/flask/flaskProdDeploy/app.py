from flask import Flask
from flask_cors import CORS

from router import api


# 实例化flask对象
app = Flask(__name__)

# 添加跨域请求允许的头部字段：对/下所有的url，允许所有的origins来访问
CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'POST'], supports_credentials=True)

# flask_restful init
api.init_app(app)


if __name__ == '__main__':
    app.run()

