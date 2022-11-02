from flask import Flask
from flask_cors import CORS

from router import api


# ʵ����flask����
app = Flask(__name__)

# ��ӿ������������ͷ���ֶΣ���/�����е�url���������е�origins������
CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'POST'], supports_credentials=True)

# flask_restful init
api.init_app(app)


if __name__ == '__main__':
    app.run()

