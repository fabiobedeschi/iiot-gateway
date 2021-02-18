from flask import Flask, request
from flask.helpers import send_from_directory

from .database import Database

app = Flask(__name__)
db = Database()


@app.route('/users/<string:user_id>', methods=['GET'])
def check_user(user_id):
    result = db.find_user(user_id)
    return user_id, (200 if result else 404)


@app.route('/users/<string:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    data = request.json
    result = None
    if data:
        result = db.update_user(user_id, data.get('delta', 0))
    return user_id, (200 if result else 404)


@app.route('/waste_bins/<string:waste_bin_id>', methods=['PUT', 'PATCH'])
def update_waste_bin(waste_bin_id):
    # TODO: Update new value in DB to track
    return waste_bin_id, 201


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
    return user_id, (201 if result else 409)


# TODO: remove this before delivery
@app.route('/users/<string:user_id>', methods=['DELETE'])
def remove_user(user_id):
    result = None
    if check_user(user_id)[1] == 200:
        result = db.delete_user(user_id)
    return user_id, (200 if result else 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
