from flask import Blueprint, url_for
# models.py에 Question 클래스를 가져와서 사용
from werkzeug.utils import redirect

# 객체 bp
bp = Blueprint('main', __name__, url_prefix='/')
# url_prefix = '/'
# 밑에 접속하는 주소의 기본값
# 예) url_prefix = '/main'
# localhost:5000/main

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
   return redirect(url_for('question._list'))


