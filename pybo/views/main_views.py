from flask import Blueprint, url_for, render_template, jsonify,request
# models.py에 Question 클래스를 가져와서 사용
from werkzeug.utils import redirect
from pybo.models import Question
from pybo import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

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

# get 방식 (생략가능)
@bp.route('/load_question')
def load_question():
    # 1. DB에서 값을 읽어오기
    # Question.query.~~~
    # [클래스] 쿼리 쿼리종류
    # 모델
    # Question.query.all() # 모든 레코드 조회
    # QUestion.query.first() # 첫 번째 레코드 조회
    # QUestion.query.get(id) # 특정 id로 조회
    # QUestion.query.filter_by(field=value) # 단순 조건 필터링
    # QUestion.query.filter(Question.field == value) # 보다 복잡한 조건 필터링
     # QUestion.query.order_by(Question.create_date.desc()) 정렬

    question_list = Question.query.all()
    # 확인을 위해서 question_list 출력
    print("question 리스트:",question_list)
    # 2. json 변환
    question_list_dict = [question.to_dict() for question in question_list]
   
    # 3. 변환 결과를 return
    
    return jsonify(question_list_dict)

# 생략이 되어 있지만 GET방식이지만 query 가져올 수 있음
# http://<주소>/load_question_id?id=<번호>

@bp.route('/load_question_id', methods=['GET'])
def load_question_id():
    # 1. 쿼리 파라미터 가져오기
    # request 맨 위에 from flask import request
    # 클라이언트에서
    # http://<ip주소>/load_question_id?id=3
    # 위 주소에서 id 값을 추출해서 가져옴
    id = request.args.get('id')

    # 2. 기본 조회: 모든 데이터
    if not id:
        return "id 값이 없습니다."
    else:
        # id 값을 기준으로 필터링
        question = Question.query.get(id)

    return jsonify(question.to_dict())

# GET이 아닌 POST 방식으로 값을 가져옴
# 엔드포인트(주소)는 같아도 상관이 없음.
@bp.route('/load_question_id', methods=['POST'])
# POST 방식은 JSON으로 데이터를 가져옴
# GET 방식과는 다르게 id 값을 가져와야 함
def load_question_id_post():
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "id" 필드를 가져옴
    print("request : ", request)
    data = request.get_json()
    print("data : " ,data)
    id = data.get('id') if data else None

    # 2. 기본 조회: 모든 데이터
    if not id:
        return jsonify({"error":"id 값이 없습니다."}), 400
    
    # 3. 데이터 조회
    question = Question.query.get(id)
    if not question:
        return jsonify({"error":f"id {id}에 해당하는 데이터가 없습니다."}),400
   

    return jsonify(question.to_dict())

# 엔드포인트(주소)는 같아도 방식이 다르면 다르게 인식
# 문제는 없음. 단, 많이 앤드포인트가 겹치다보면
# 헷갈릴수가 있음
@bp.route('/add_question', methods=['POST'])
# POST 방식은 JSON으로 데이터를 가져옴
# GET 방식과는 다르게 id 값을 가져와야 함
def add_question_post():
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "subject,content" 필드를 가져옴
    print("request : ", request)
    data = request.get_json()
    print("data : " ,data)
    subject = data.get('subject') if data else None
    content = data.get('content') if data else None

    # 3. 새로운 Question 객체 생성
    new_question = Question(
        subject = subject,
        content = content,
        #create_date = datetime.now()
    )
    
    # 데이터베이스 세션에 추가
    # db라는 것을 사용하기 위해서 아래코드를 파일 윗부분에 추가
    # from pybo import db
    db.session.add(new_question)
    # 변경사항 커밋
    # db.session.commit() 것이 데이터를 추가한 것을 커밋
    # db.session.commit() 문제가 발생하면?
    # 문제가 발생하면 서버 프로그램이 중단
    # try, except 구문을 사용하면 문제 발생이 되었을때
    # 적절한 코드가 실해잉 되면서 종료되지 않음
    # try, except 구문을 사용하여 처라하여야함
     # 4. 결과 반환
    try:
        db.session.commit()
        print("Commit successful")
        return jsonify("추가가 완료되었습니다."),201
    except SQLAlchemyError as e:
        # SQLaLchemyError를 사용하기 위해
        # 상단에 from sqlalchemy.exc import SQLAlchemyError 추가
        db.session.rollback() # 문제 발생시 롤백
        print(f"Commit failed: {str(e)}")
        return jsonify({"error":"추가 실패"+str(e)}),500
    
# PUT 방식 구현
# http://<주소ip>/change_question/<id>
# request의 본문
#{
# "subject" : 제목,
# "content" : 내용
#}
# id와 subject, content를 가져오는 방식이 약간 다름
@bp.route('/change_question/<int:id>', methods=['PUT'])
# id 값
def change_question(id):
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "subject,content" 필드를 가져옴
    print("request : ", request)
    data = request.get_json()
    print("data : " ,data)
    subject = data.get('subject') if data else None
    content = data.get('content') if data else None

    # id로 DB에 Question 테이블을 조회해서 데이터를 업데이트 하는 것이 목적
    # 2. id로 DB에 Question 테이블에 데이터를 조회
    question = Question.query.get(id)
    
    # question 없을때
    if not question:
        return jsonify({"error":f"id {id}에 해당하는 데이터가 없습니다."}),404
    
    # 데이터 존재하면
    # 데어터를 업데이트
    if subject: # request에 subject
        question.subject = subject
    
    if content: # request에 content
        question.content = content

    try:
        db.session.commit()
        print("Commit successful")
        return jsonify({"message":f"Question {id}이 업데이트 되었습니다."}),200
    except SQLAlchemyError as e:
        # SQLaLchemyError를 사용하기 위해
        # 상단에 from sqlalchemy.exc import SQLAlchemyError 추가
        db.session.rollback() # 문제 발생시 롤백
        print(f"Update failed: {str(e)}")
        return jsonify({"error":"업데이트 중 문제가 발생하였습니다."+str(e)}),500
   

@bp.route('/delete_question/<int:id>', methods=['DELETE'])
# id 값
def delete_question(id):
    # id로 DB에 Question 테이블을 조회해서 데이터를 삭제 하는 것이 목적
    # 2. id로 DB에 Question 테이블에 데이터를 조회
    question = Question.query.get(id)
    
    # question 없을때
    if not question:
        return jsonify({"error":f"id {id}에 해당하는 데이터가 없습니다."}),404
    
    # 데이터 존재하면
    # 데어터를 삭제
    try:
        db.session.delete(question)
        db.session.commit()
        print(f"Question {id} has been deleteed.")
        return jsonify({"message":f"Question {id}이 삭제 되었습니다."}),200
    except SQLAlchemyError as e:
        # SQLaLchemyError를 사용하기 위해
        # 상단에 from sqlalchemy.exc import SQLAlchemyError 추가
        db.session.rollback() # 문제 발생시 롤백
        print(f"Update failed: {str(e)}")
        return jsonify({"error":"삭제 중 문제가 발생하였습니다."+str(e)}),500