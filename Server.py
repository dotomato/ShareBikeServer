#!usr/bin/python
# coding=utf-8

from flask import *
import uuid
import time
import random


app = Flask(__name__)

VERSION = 'v0.01'
APIURL = '/api/' + VERSION


@app.route(APIURL + '/borrow_car', methods=['POST'])
def borrow_car():
    data = request.get_data()
    body = json.loads(data)
    result = {'result': 'success'}
    return make_response(jsonify(result), 200)


@app.route(APIURL + '/return_car', methods=['POST'])
def return_car():
    data = request.get_data()
    body = json.loads(data)
    result = {'result': 'success'}
    return make_response(jsonify(result), 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)