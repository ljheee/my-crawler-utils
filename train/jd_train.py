import os
import requests
import time
from pyquery import PyQuery as pq

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    'Host': "train.jd.com",  # required
    'Referer': "http://train.jd.com/",
}

ticket_headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    'Host': "train.jd.com",  # required
    'Referer': "http://train.jd.com/query/queryTrainStations.html",
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest'
}
url = 'http://train.jd.com/query/queryTrainStations.html'
query_tickets = 'http://train.jd.com//query/getTrainTickets.html'

datas = {
    'stationQuery.fromStation': '北京',
    'stationQuery.toStation': '广州',
    'stationQuery.date': '2019-05-20',
    'stationQuery.requestType': '0'
}
ticket_datas = {
    'stationQuery.fromStation': '北京',
    'stationQuery.toStation': '广州',
    'stationQuery.date': '2019-05-20',
    'stationQuery.requestType': '0'
}
# html = requests.post(url, data=datas) #查询主列表 main-list

tickets = requests.post(query_tickets, data=ticket_datas, headers=ticket_headers)
json = tickets.json()
success=json['success']
if(success):
    data=json['data']
    fromStations = data['fromStations']
    toStations = data['toStations']
    date = data['addition']['date']
    print(date)
    values = data['value']
    for item in values:
        print(item)


