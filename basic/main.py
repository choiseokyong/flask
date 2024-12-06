# flask => 파이썬용 서버구축 모듈
# jsonify => 텍스트를 JSON 형태로 변경
# request : 클라이언트가 서버로 보낸 HTTP요청에 접근하기 위한 객체
from flask import Flask, jsonify, request
app = Flask(__name__)

menus = [
    {"id": 1, "name": "Espresso", "price": 3800},
    {"id": 2, "name": "Americano", "price": 4100},
    {"id": 3, "name": "CageLatte", "price": 4600},
]


@app.route('/')
def hello_flask():
    return "Hello World!!"

#GET /menus | 자료를 가지고 온다.
@app.route('/menus',methods = ['POST'])
def get_menus():
    return jsonify(menus)

#POST /menus
@app.route('/menus', methods = ['POST'])
def create_menu():
    # 전달받은 자료를 menus 자원에 추가
    request_data = request.get_json()   #{"name": ..., "price": ...}
    new_menu = {
        "id" : 4,
        "name" : request_data['name'],
        "price" : request_data['price'],
    }
    menus.append(new_menu)
    return jsonify(new_menu)

if __name__ == '__main__':
    app.run()