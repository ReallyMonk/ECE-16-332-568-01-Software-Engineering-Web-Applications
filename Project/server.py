from flask import Flask
from flask import render_template
import pymongo
from getyeardata import get_year_data
from newbcf import predict as predict_nextday
# from backgroud import get_info
import pymongo
import time
import json
import requests
import datetime
import json

app = Flask(__name__)


@app.route('/index', methods=['GET'])
def index():
    # background()
    name = 1
    return render_template('stockprediction.html', data=name)


@app.route('/update_year_data')
def update_year_data():
    get_year_data()
    return 'done'


@app.route('/yeardata_search/<comp>', methods=['GET'])
def year_search(comp):
    # connect to the database
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.year_info

    doc = db[comp]

    res = list(doc.find())

    print(list(res[0].keys()))

    _time = res[0]['time']
    _high = res[0]['high']
    _low = res[0]['low']
    _open = res[0]['open']
    _close = res[0]['close']
    _volume = res[0]['volume']

    # package into json
    all_info = {
        'time': _time,
        'high': _high,
        'low': _low,
        'open': _open,
        'close': _close,
        'volume': _volume
    }
    stock_info = json.dumps(all_info)

    return stock_info


@app.route('/predict/<comp>')
def predict(comp):
    # take average of low and high
    all_data = json.loads(year_search(comp))

    trainY = all_data['high']

    trainX = range(1, len(trainY) + 1)
    value, trend = predict_nextday(trainX, trainY)
    print(value[0], trend[0])

    return str(value[0])


app.run(port=5005)
