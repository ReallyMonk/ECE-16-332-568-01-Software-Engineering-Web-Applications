import pymongo
import time
import json
import requests
import datetime


def get_info():
    companies = [
        'GOOG', 'YOJ.SG', 'NVDA', 'AMZN', 'TSLA', 'AAPL', 'COKE', 'MCD',
        'MSFT', 'SNE'
    ]

    for name in companies:
        # download data
        # url = "https://query1.finance.yahoo.com/v8/finance/chart/" + name + "?symbol=" + name + "&period1=" + str(timestamp-80000) + "&period2=" + str(timestamp+1000) + "&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=RGKkY5jfStA&corsDomain=finance.yahoo.com"
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/'+name+'?region=US&lang=en-US&includePrePost=false&interval=1m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'

        request = requests.get(url)

        res = request.content
        #print(res)

        # write to MongoDB
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.realtime_info

        collection = db[name]
        data = json.loads(request.content)
        time = {'time': data['chart']['result'][0]['timestamp'][-1]}
        print(time)
        _high = {'high': data['chart']['result'][0]['indicators']['quote'][0]['high'][-1]}
        _low = {'low': data['chart']['result'][0]['indicators']['quote'][0]['low'][-1]}
        _open = {'open': data['chart']['result'][0]['indicators']['quote'][0]['open'][-1]}
        _close = {'close': data['chart']['result'][0]['indicators']['quote'][0]['close'][-1]}
        _volume = {'volum': data['chart']['result'][0]['indicators']['quote'][0]['volume'][-1]}

        # collection.insert_many(rest_info)
        #print(type(time))
        all_info = {}
        all_info.update(time)
        all_info.update(_high)
        all_info.update(_low)
        all_info.update(_open)
        all_info.update(_close)
        all_info.update(_volume)
        print(all_info)

        # write into json file
        path = 'D:\Rutgers\\2nd Semester\SOFTWR ENGG WEB APPL\Homework\Project\data\\realtime_data\\'
        with open(path + name + '.json', 'a') as f:
            f.write(json.dumps(all_info) + '\n')
            f.close()

        collection.insert_one(all_info)


#get_info(1582757640)

    # analysis the time

d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 17:40:10', '%Y-%m-%d %H:%M:%S')

delta = d2 - d1
print(delta.seconds)



while True:
    if 