from flask import Flask
from flask.helpers import send_from_directory

app = Flask(__name__)


@app.route('/')
def hello_world():
    return send_from_directory(directory='../static', filename='example.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
