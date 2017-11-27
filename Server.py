#!usr/bin/python
# coding=utf-8

from flask import *
import uuid
import time
import random
import urllib2



app = Flask(__name__)

VERSION = 'v0.01'
APIURL = '/api/' + VERSION


class CarState:

    def __init__(self, id, openurl, closeurl):
        self.id = id
        self.is_return = True
        self.openurl = openurl
        self.closeurl = closeurl

    def open(self):
        urllib2.urlopen(self.openurl).read()

    def close(self):
        urllib2.urlopen(self.closeurl).read()

# 填入车上的二维码的，车锁树莓派的URL
carlist = [CarState('111', 'http://192.168.1.1/open', 'http://192.168.1.1/open')]


def get_car(id):
    for car in carlist:
        if car.id == id:
            return car
        else:
            return None


@app.route(APIURL + '/borrow_car', methods=['POST'])
def borrow_car():
    data = request.get_data()
    body = json.loads(data)
    id = body['id']
    print id
    car = get_car(id)
    if car is None or not car.is_return:
        result = {'result': 'failed'}
    else:
        result = {'result': 'success'}
        car.is_return = False
        car.open()
        print 'car has been rented ,id=%s' % id
    return make_response(jsonify(result), 200)


@app.route(APIURL + '/return_car', methods=['POST'])
def return_car():
    data = request.get_data()
    body = json.loads(data)
    id = body['id']
    print id
    car = get_car(id)
    if car is None:
        result = {'result': 'failed'}
    else:
        result = {'result': 'success'}
        car.is_return = True
        car.close()
        print 'car has been returned ,id=%s' % id
    return make_response(jsonify(result), 200)


@app.route(APIURL + '/is_return', methods=['POST'])
def is_return():
    data = request.get_data()
    body = json.loads(data)
    id = body['id']
    car = get_car(id)
    if car is None or not car.is_return:
        result = {'result': 'not return'}
    else:
        result = {'result': 'return'}
    return make_response(jsonify(result), 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)