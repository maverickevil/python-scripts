# -*- coding: UTF-8 -*-
from flask import Blueprint

bp1 = Blueprint('web', __name__)

@bp1.route('/foo1')
def foo1():
    return 'foo1'

@bp1.route('/foo2')
def foo2():
    return 'foo2'
