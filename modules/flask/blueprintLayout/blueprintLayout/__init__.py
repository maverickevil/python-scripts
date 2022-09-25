# -*- coding: UTF-8 -*-
from flask import Flask, render_template
from .views.bp1 import bp1
from .views.bp2 import bp2

def create_app():
    app = Flask(__name__)
    app.secret_key = "4c6d5a1ba55625a1f6b06195628b7f8b"

    @app.route('/index')
    def index():
        return render_template('index.html')

    app.register_blueprint(bp1, url_prefix='/web')
    app.register_blueprint(bp2, url_prefix='/admin')

    return app
