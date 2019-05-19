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


skus = []

paoxie_url = 'https://www.smzdm.com/fenlei/paobuxie/p1'

html = requests.get(paoxie_url, headers=headers).content.decode('utf-8')
# print(html)
doc = pq(html);
# feed-main-list
p = doc('#feed-main-list li')
items = p.items()

for item in items:
    sub = pq(item)
    title = sub('.feed-block-title a').text();  # 好价 ASICS 亚瑟士 Nitrofuze 2 T7E3N 男式入门缓冲跑步鞋 245元
    strs = title.split(' ');
    priceStr = strs[-1]  # 245元
    index = priceStr.find('元')

    price = 1000
    if index == -1:  #个别商品没有优惠价
        price = 1000
    else:
        price = int(priceStr[0: index])

    descripe = sub('.feed-block-descripe').text()
    url = sub('.feed-link-btn-inner a').attr('href')
    time = sub('.feed-block-extras').text()

    sku = SkuItem(title, price, descripe, url, time)
    skus.append(sku)

brand = 'ASICS'  # 筛选品牌
filterPrice = 600  # 筛选价格
newList = filter(lambda item: (brand in item.skuName) and (int(item.price) <= filterPrice), skus)
newList = sorted(newList, key=lambda item: item.price)  # 刷选后价格递增排序

for youWant in newList:
    print(youWant)
print(skus.__len__())  # 源列表不变

# for i in skus:
#     if brand in i.skuName:
#         print(i)
