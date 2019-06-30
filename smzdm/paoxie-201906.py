import os
import requests
import time
from pyquery import PyQuery as pq

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    'Host': "www.smzdm.com",  # required
    'Referer': "https://www.smzdm.com/"
}

class SkuItem:
    def __init__(self, skuName, price, descripe, url, time):
        self.skuName = skuName;
        self.price = price;
        self.descripe = descripe;
        self.url = url;
        self.time = time;

    def __str__(self):
        return "skuName:" + self.skuName + ",price:" + str(
            self.price) + ",descripe:" + self.descripe + ",url:" + self.url + " ,time:" + self.time + " (__str__)"

    def toString(self):
        return "price:" + str(
            self.price) + ",skuName:" + self.skuName + ",descripe:" + self.descripe + ",url:" + self.url + " ,time:" + self.time + " (__str__)"


def parsePrice(priceStr):
    if priceStr.__contains__('过期') \
            or priceStr.__contains__('$') \
            or priceStr.__contains__('售罄') \
            or priceStr.__contains__('折起'):
        return -2

    priceStr = priceStr.replace('低至', '')
    priceStr = priceStr.replace('（需用券）', '')
    priceStr = priceStr.replace('（前2小时）', '')

    price = 1000
    index = priceStr.find('元')
    if index == -1:  # 个别商品没有优惠价
        price = 1000
    else:
        try:
            price = float(priceStr[0: index])
        except ValueError as e:     #python3.7 的异常处理
            print(e)
            price = -2
    return price;


skus = []


def get_url(page):
    paoxie_url = 'https://www.smzdm.com/fenlei/paobuxie/p' + str(page)
    html = requests.get(paoxie_url, headers=headers).content.decode('utf-8')

    doc = pq(html);
    # feed-main-list
    p = doc('#feed-main-list li')
    items = p.items()

    for item in items:
        sub = pq(item)
        title = sub('.feed-block-title a').text();  # 好价 ASICS 亚瑟士 Nitrofuze 2 T7E3N 男式入门缓冲跑步鞋
        priceStr = sub('.z-highlight a').text();

        price = parsePrice(priceStr)
        if price == -2:
            continue;  # 过期

        descripe = sub('.feed-block-descripe').text()
        url = sub('.feed-link-btn-inner a').attr('href')
        time = sub('.feed-block-extras').text()

        sku = SkuItem(title, price, descripe, url, time)
        skus.append(sku)


if __name__ == '__main__':
    for i in range(8):
        get_url(i + 1)

    skus.sort(key=lambda item: item.price)
    for sku in skus:
        print(sku.toString())
