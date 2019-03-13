import json

import requests
from lxml import etree
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["dawn"]
for i in range(1, 88):
    url = "http://www.xiaoshuo520.com/vip_{}.html".format(i)
    response = requests.get(url)
    ret = response.content.decode()
    html = etree.HTML(ret)
    xs_url_list = html.xpath('//*[@id="container"]/div/a/@href')
    for url in xs_url_list:
        xs_url = "http://www.xiaoshuo520.com" + url
        response = requests.get(xs_url)
        ret = response.content.decode()
        html = etree.HTML(ret)
        detail_url = html.xpath('//div[@class="bookbtn-bd"]/a[3]/@href')[0]
        start_read_url = "http://www.xiaoshuo520.com" + detail_url
        item = {}
        item["url"] = start_read_url

        list = []
        while True:
            response = requests.get(start_read_url)
            ret = response.content.decode()
            html = etree.HTML(ret)
            try:
                item["caption_header"] = html.xpath('//div[@class="readbg"]/h1/text()')[0]  # 判断是否有title并把最后一张免费阅读放入字典
            except IndexError:
                print("下载完一本书")
                # list.append(dic_n)
                item["article"] = list
                mycol.insert_one(item)
                # with open("xs_2_520.txt", "a+", encoding="utf-8")as f:
                #     json.dump(item, f, ensure_ascii=False, indent=4)
                #     f.write("\n")
                break
            item["classify"] = html.xpath('//div[@class="readbg"]/div[@class="readlocation"]/div/a[2]/text()')[0]
            item["name"] = html.xpath('//div[@class="readbg"]/div[@class="readlocation"]/div/a[3]/text()')[0]
            item["a_t_word"] = html.xpath('//div[@class="readbg"]/div[@class="article-infos"]/text()')

            article_list = html.xpath('//div[@class="readbg"]/div[@class="article-con"]//text()') #文章内容列表
            all_word = ""
            for p in article_list:
                last=article_list.index(p)
                p = p.replace("\r\n", "").replace(" ", "")
                all_word += p
                if len(article_list) -1 == last:
                    dic_n = {}
                    dic_n[item["caption_header"]] = all_word
                    list.append(dic_n)
            # dic[item["caption_header"]]=all_word
            next1 = html.xpath('//div[@class="readbg"]/div[@class="articlebtn"]/a[3]/@href')[0]
            last1 = start_read_url.split("/")[-1]
            start_read_url = start_read_url.replace(last1, next1)
            print(start_read_url)
