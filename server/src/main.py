from typing import Optional

from flask import Flask, request, jsonify
from flask.helpers import send_from_directory

from .database import Database

app = Flask(__name__)
db: Optional[Database] = None


@app.before_request
def init_app():
    global db
    if not db:
        db = Database()


@app.route('/users/<string:user_id>', methods=['GET'])
def check_user(user_id):
    result = db.find_user(user_id)
    return (jsonify(dict(result)), 200) if result else (None, 404)


@app.route('/users/<string:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    result = None
    if data := request.json:
        result = db.update_user(
            uuid=user_id,
            delta=data.get('delta', 0)
        )
    return (jsonify(dict(result)), 200) if result else (None, 404)


@app.route('/waste_bins/<string:waste_bin_id>', methods=['PUT', 'PATCH'])
def update_waste_bin(waste_bin_id):
    result = None
    if data := request.json:
        result = db.update_waste_bin(
            uuid=waste_bin_id,
            fill_level=data.get('fill_level'),
        )
    return (jsonify(dict(result)), 200) if result else (None, 404)


# TODO: remove this before delivery
@app.route('/hello')
def hello_world():
    return send_from_directory(directory='../static', filename='example.html')


# TODO: remove this before delivery
@app.route('/users/<string:user_id>', methods=['POST'])
def create_user(user_id):
    result = None
    if check_user(user_id)[1] == 404:
        result = db.insert_user(user_id)
    return (jsonify(dict(result)), 201) if result else (None, 409)


# TODO: remove this before delivery
@app.route('/users/<string:user_id>', methods=['DELETE'])
def remove_user(user_id):
    result = None
    if check_user(user_id)[1] == 200:
        result = db.delete_user(user_id)
    return (jsonify(dict(result)), 200) if result else (None, 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
