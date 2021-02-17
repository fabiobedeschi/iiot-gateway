from flask import Flask
from flask import request
from flask.helpers import send_from_directory

app = Flask(__name__)


@app.route('/users/<string:user_id>', methods=['GET'])
def check_user(user_id):  # TODO: Check if exists in DB
    if user_id == "FFFFFFFFFFFFFFFF0001020304050607":
        return user_id, 200
    else:
        return user_id, 403


@app.route('/users/<string:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):  # TODO: Update new value in DB to track
    data = request.json
    s = ""

    for n in data:
        a = data[n]
        print(n, "è", a, sep=" ")
        s = ("%s<br>%s  è %s ") % (s, n, a)
    return s, 200


@app.route('/waste_bins/<string:waste_bin_id>', methods=['PUT', 'PATCH'])
def update_waste_bin(waste_bin_id):  # TODO: Update new value in DB to track
    data = request.json
    s = ""

    for n in data:
        a = data[n]
        print(n, "è", a, sep=" ")
        s = ("%s<br>%s  è %s ") % (s, n, a)
    return s, 200


@app.route('/hello')
def hello_world():
    return send_from_directory(directory='../static', filename='example.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
