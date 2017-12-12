#!usr/bin/python
# coding=utf-8

from flask import *
import uuid
import time
import random
import datetime
import urllib2
import xlrd
import xlwt
from xlutils.copy import copy


app = Flask(__name__)

VERSION = 'v0.01'
APIURL = '/api/' + VERSION


class CarState:

    def __init__(self, id, openurl, closeurl):
        self.id = id
        self.is_return = True
        self.openurl = openurl
        self.closeurl = closeurl
        self.start_time = -1

    def open(self):
        urllib2.urlopen(self.openurl).read()
        # pass

    def close(self):
        urllib2.urlopen(self.closeurl).read()
        # pass

# 填入车上的二维码的，车锁树莓派的URL
carlist = [CarState('101002', 'http://xxx.xxx.xxx.xxx:xxxx/open', 'http://xxx.xxx.xxx.xxx:xxxx/close')]

rb_data = xlrd.open_workbook('DataBase.xls')
count_data = int(rb_data.sheet_by_index(0).cell(0, 1).value)
wb_data = copy(rb_data)
ws_data = wb_data.get_sheet(0)
print '目前数据库中共有%d条数据' % count_data


def get_car(id):
    for car in carlist:
        if car.id == id:
            return car
        else:
            return None


def record(str_time, str_id, str_action, str_money, str_info):
    global count_data
    count_data += 1
    str_result = u'%s :第%s号自行车,%s，费用%s, %s' % (str_time, str_id, str_action, str_money, str_info)
    ws_data.write(0, 1, count_data)
    ws_data.write(count_data + 2, 0, str_time)
    ws_data.write(count_data + 2, 1, str_id)
    ws_data.write(count_data + 2, 2, str_action)
    ws_data.write(count_data + 2, 3, str_money)
    ws_data.write(count_data + 2, 4, str_info)
    wb_data.save('DataBase.xls')
    print str_result

@app.route(APIURL + '/borrow_car', methods=['POST'])
def borrow_car():
    data = request.get_data()
    body = json.loads(data)
    id = body['id']
    car = get_car(id)
    if car is None or not car.is_return:
        result = {'result': 'failed'}
    else:
        result = {'result': 'success'}
        car.is_return = False
        car.start_time = time.time()
        car.open()

        str_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        str_id = car.id
        str_action = u'借出'
        str_money = u'0.00元'
        str_info = u''
        record(str_time, str_id, str_action, str_money, str_info)
    return make_response(jsonify(result), 200)


@app.route(APIURL + '/return_car', methods=['POST'])
def return_car():
    data = request.get_data()
    body = json.loads(data)
    id = body['id']
    car = get_car(id)
    if car is None:
        result = {'result': 'failed'}
    else:
        result = {'result': 'success'}
        car.is_return = True
        stopTime = int(time.time() - car.start_time)
        stopMoney = ((stopTime / 60) + 1) * 0.5

        car.close()

        str_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        str_id = car.id
        str_action = u'归还'
        str_money = u'%0.2f元' % stopMoney
        str_info = u'行车时长%d秒' % stopTime
        record(str_time, str_id, str_action, str_money, str_info)
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
    import logging
    logging.basicConfig(level=logging.FATAL)
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)