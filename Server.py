#!usr/bin/python
# coding=utf-8

from flask import *
import uuid
import time
import random


app = Flask(__name__)

VERSION = 'v0.01'
APIURL = '/api/' + VERSION


class CarState:

    def __init__(self, id):
        self.id = id
        self.is_return = True


carlist = []


def get_car(id):
    for car in carlist:
        if car.id == id:
            return car
        else:
            return None


def new_car(id):
    if get_car(id) is not None:
        return get_car(id)
    else:
        car = CarState(id)
        carlist.append(car)
        return car


@app.route(APIURL + '/borrow_car', methods=['POST'])
def borrow_car():
    data = request.get_data()
    body = json.loads(data)
    id = body['id']
    print id
    car = get_car(id)
    if car is None:
        car = new_car(id)
    if not car.is_return:
        result = {'result': 'failed'}
    else:
        result = {'result': 'success'}
        car.is_return = False
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