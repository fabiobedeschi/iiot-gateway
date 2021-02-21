from typing import Optional

from flask import Flask, jsonify, render_template, request
from flask.helpers import send_from_directory
from flask_accept import accept, accept_fallback

from .database import Database

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config['JSON_SORT_KEYS'] = False
db: Optional[Database] = None


@app.before_request
def init_app():
    global db
    if not db:
        db = Database()


@app.route('/')
@accept('text/html')
def root_page():
    return render_template('root.html')


@app.route('/users', methods=['GET'])
@accept_fallback
def find_all_users():
    result = db.find_all_users()
    return (jsonify(result), 200) if result else (None, 404)


@find_all_users.support('text/html')
def find_all_users_html():
    result = db.find_all_users()
    return render_template('table_collection.html', name='Users', collection=result)


@app.route('/users/<string:user_id>', methods=['GET'])
def find_user(user_id):
    result = db.find_user(user_id)
    return (jsonify(result), 200) if result else (None, 404)


@app.route('/users/<string:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    result = None
    if data := request.json:
        result = db.update_user(
            uuid=user_id,
            delta=data.get('delta', 0)
        )
    return (jsonify(result), 200) if result else (None, 404)


@app.route('/waste_bins', methods=['GET'])
@accept_fallback
def find_all_waste_bins():
    result = db.find_all_waste_bins()
    return (jsonify(result), 200) if result else (None, 404)


@find_all_waste_bins.support('text/html')
def find_all_waste_bins_html():
    result = db.find_all_waste_bins()
    return render_template('table_collection.html', name='Waste bins', collection=result)


@app.route('/waste_bins/<string:waste_bin_id>', methods=['GET'])
def find_waste_bin(waste_bin_id):
    result = db.find_waste_bin(waste_bin_id)
    return (jsonify(result), 200) if result else (None, 404)


@app.route('/waste_bins/<string:waste_bin_id>', methods=['PUT', 'PATCH'])
def update_waste_bin(waste_bin_id):
    result = None
    if data := request.json:
        result = db.update_waste_bin(
            uuid=waste_bin_id,
            fill_level=data.get('fill_level'),
        )
    return (jsonify(result), 200) if result else (None, 404)


# TODO: remove this before delivery
@app.route('/hello')
@accept('text/html')
def hello_world():
    return send_from_directory(directory='../static', filename='example.html')


# TODO: remove this before delivery
@app.route('/users/<string:user_id>', methods=['POST'])
def create_user(user_id):
    result = None
    if find_user(user_id)[1] == 404:
        result = db.insert_user(user_id)
    return (jsonify(result), 201) if result else (None, 409)


# TODO: remove this before delivery
@app.route('/users/<string:user_id>', methods=['DELETE'])
def remove_user(user_id):
    result = None
    if find_user(user_id)[1] == 200:
        result = db.delete_user(user_id)
    return (jsonify(result), 200) if result else (None, 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
