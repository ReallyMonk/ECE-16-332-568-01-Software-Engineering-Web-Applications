import requests
import json
from datetime import datetime
import pymongo
import time

'''
url = "https://query1.finance.yahoo.com/v8/finance/chart/GOOG?symbol=GOOG&period1=1441166400&period2=1519621200&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=RGKkY5jfStA&corsDomain=finance.yahoo.com"
url = "https://query1.finance.yahoo.com/v8/finance/chart/SNE?symbol=SNE&period1=1582587792&period2=1582760592&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=RGKkY5jfStA&corsDomain=finance.yahoo.com"

request = requests.get(url)

path = 'D:\Rutgers\\2nd Semester\SOFTWR ENGG WEB APPL\Homework\Project\data\\'
'''


def get_year_data(t_start, t_end):
    print('connect to MongoDB')
    # connect to MongoDB
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.year_info

    # get the stock info from yahoo financial
    companies = [
        'GOOG', 'YOJ.SG', 'NVDA', 'AMZN', 'TSLA', 'AAPL', 'COKE', 'MCD',
        'MSFT', 'SNE'
    ]
    for name in companies:
        print('Download ', name)
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + name + '?symbol=' + name + '&period1=' + t_start + '&period2=' + t_end + '&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=RGKkY5jfStA&corsDomain=finance.yahoo.com'

        request = requests.get(url)
        print('Write ', name)
        # write info to mongoDB
        collection = db[name]
        data = json.loads(request.content)
        time = {'time': data['chart']['result'][0]['timestamp']}
        rest_info = data['chart']['result'][0]['indicators']['quote'][0]
        # collection.insert_many(rest_info)
        print(type(time))
        all_info = dict(time, **rest_info)

        # write into json file
        path = 'F:\Rutgers\\2ndSemester\SOFTWR ENGG WEB APPL\Homework\Project\data\year_data\\'
        with open(path + name + '.json', 'w') as f:
            f.write(json.dumps(all_info))
            f.close()

        collection.insert_one(all_info)


# please set the date you want here as the format yy-mm-dd
start_t = '2015-04-05'
end_t = '2016-04-08'

strt_stp = str(int(time.mktime(time.strptime(start_t+' 09:30:00', '%Y-%m-%d %H:%M:%S'))))
endt_stp = str(int(time.mktime(time.strptime(end_t+' 16:00:00', '%Y-%m-%d %H:%M:%S'))))

get_year_data(strt_stp, endt_stp)
