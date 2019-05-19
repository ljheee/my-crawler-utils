import asyncio
import requests
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


skus = []  #


async def get_url(page):
    print(page)
    paoxie_url = 'https://www.smzdm.com/fenlei/paobuxie/p' + str(page)
    html = requests.get(paoxie_url, headers=headers).content.decode('utf-8')
    doc = pq(html);
    p = doc('#feed-main-list li')
    items = p.items()

    for item in items:
        sub = pq(item)
        title = sub('.feed-block-title a').text();  # 好价 ASICS 亚瑟士 Nitrofuze 2 T7E3N 男式入门缓冲跑步鞋 245元
        strs = title.split(' ');
        priceStr = strs[-1]  # 245元   低至98.9    $32.9
        index = priceStr.find('元')
        dzIndex = priceStr.find('低至')

        price = 1000
        if index == -1:  # 个别商品没有优惠价
            price = 1000
        else:
            if dzIndex !=-1:
                price = float(priceStr[2: index])
            else:
                if priceStr[0: index].isnumeric():
                    price = float(priceStr[0: index])
        descripe = sub('.feed-block-descripe').text()
        url = sub('.feed-link-btn-inner a').attr('href')
        time = sub('.feed-block-extras').text()
        sku = SkuItem(title, price, descripe, url, time)
        skus.append(sku)


def filter_list(brand, filterPrice):
    newList = filter(lambda item: (brand in item.skuName) and (float(item.price) <= filterPrice), skus)
    newList = sorted(newList, key=lambda item: item.price)  # 刷选后价格递增排序
    return newList


if __name__ == '__main__':
    for i in range(8):
        asyncio.run(get_url(i + 1))

    newList = filter_list('ASICS', 350);
    for youWant in newList:
        print(youWant)
