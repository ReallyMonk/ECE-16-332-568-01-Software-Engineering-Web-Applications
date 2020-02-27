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
while False:
    start_t = '09:30'
    end_t = '16:00'
    c_start_t = datetime.datetime.strptime(start_t, '%H:%M')
    c_end_t = datetime.datetime.strptime(end_t, '%H:%M')
    now_t = datetime.datetime.now().strftime('%H:%M')
    c_now_t = datetime.datetime.strptime(now_t, '%H:%M')

    now_date = datetime.datetime.now().weekday()
    print(now_t)
    # is weekend
    if now_date == 5 or now_date == 6:
        last_t = datetime.datetime.strptime('23:59', '%H:%M')
        initial_t = datetime.datetime.strptime('0:0', '%H:%M')
        time.sleep((last_t-c_now_t).seconds+(c_start_t-initial_t).seconds)
    else:
        if c_now_t >= c_start_t and c_now_t <= c_end_t:
            print('start')
            get_info()
            time.sleep(61)
        elif c_now_t < c_start_t:
            print('early')
            time.sleep((c_start_t-c_now_t).seconds)
        else:
            print('late')
            last_t = datetime.datetime.strptime('23:59', '%H:%M')
            initial_t = datetime.datetime.strptime('0:0', '%H:%M')
            time.sleep((last_t-c_now_t).seconds+(c_start_t-initial_t).seconds)

