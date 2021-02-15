from flask import Flask
from flask import request
from flask.helpers import send_from_directory

app = Flask(__name__)

@app.route('/users/<string:userid>', methods=['GET'])
def check_user(userid): #TODO: Check if exists in DB
    if userid == "FFFFFFFFFFFFFFFF0001020304050607":
        return userid, 200
    else:
        return userid, 403
    return userid


@app.route('/users/<string:userid>/update', methods=['PATCH'])
def update_user(userid): #TODO: Update new value in DB to track 
    data = request.json
    s =""

    for n in data :
        a = data[n]
        print(n,"è",a,sep=" ")
        s = ( "%s<br>%s  è %s " ) % (s, n, a)
    return s, 200


@app.route('/')
def hello_world():
    return send_from_directory(directory='../static', filename='example.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
