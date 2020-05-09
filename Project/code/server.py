from flask import Flask
import pymongo
from getyeardata import get_year_data
from newbcf import predict as predict_nextday
# from backgroud import get_info
import pymongo
import time
import json
import requests
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # background()
    return 'hello world'


@app.route('/update_year_data')
def update_year_data():
    get_year_data()
    return 'done'


@app.route('/y_search')
def year_search(comp='AAPL'):
    # connect to the database
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.year_info

    doc = db[comp]

    res = list(doc.find())

    print(list(res[0].keys()))

    _time = res[0]['time']
    _high = res[0]['high']
    _low = res[0]['low']
    # _open = res[0]['open']
    # _close = res[0]['close']
    # _volume = res[0]['volume']

    avg = []
    for a, b in zip(_high, _low):
        avg.append((a + b) / 2)

    return _time, avg


@app.route('/predict')
def predict():
    no, trainY = year_search()
    trainX = range(1, len(trainY) + 1)
    value, trend = predict_nextday(trainX, trainY)
    print(value[0], trend[0])

    return str(value[0])


app.run(port=5005)
