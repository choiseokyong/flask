from flask import Blueprint, url_for, render_template
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


@bp.route('/test')
def test():
    # 관련 웹페이지 주소
    # 1. redirect('페이지url'))
    # 2. render_template() 페이지를 template 사용하는 경우 사용
    # 3. redirect(url_for('다른 라우트에 있는 페이지'))
    return render_template("test.html")

@bp.route('/test2')
def test2():
    return render_template("./test/test2.html")