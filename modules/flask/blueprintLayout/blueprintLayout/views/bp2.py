# -*- coding: UTF-8 -*-
from flask import Blueprint

bp2 = Blueprint('admin', __name__)

@bp2.route('/foo3')
def app1():
    return 'foo3'

@bp2.route('/foo4')
def app2():
    return 'foo4'
