#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-09 16:25:57
# Project: xianyu_list
from pyspider.libs.base_handler import *
from fake_useragent import UserAgent
import json
from urllib import parse
import datetime
import time
import pymongo
import random


class Handler(BaseHandler):
    # fakeUA
    ua = UserAgent()
    ua.update()
    crawl_config = {
        'headers': {
            'User-Agent': ua.random}
    }
    # 搜索关键词
    name = ['女仆装']
    # 将mongodb中的status字段置为0（默认resultDB不需要）
    # def set_mongo_status(self,keyword):
    #     client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    #     db = client['pyspider_resultdb']
    #     coll = db['xianyu_list']
    #     # 将所有已存在的历史记录状态刷新为0
    #     data_id = coll.update_many({'keyword':keyword}, {'$set': {'status': '0'}})
    #     print('update history status: ' + str(data_id))

    @every(minutes=15)
    def on_start(self):
        for name in self.name:
            self.crawl('https://2.taobao.com/list/list.htm?st_edtime=1&_input_charset=utf8&q={}&ist=0'.format(name), save=name, callback=self.get_itag)
            time.sleep(random.uniform(0, 2.5))

    @config(age=15 * 60)
    def get_itag(self, response):
        # 获取首个链接为itag
        pageNum = int(response.etree.xpath('//span[@class="paginator-count"]/text()')[0].lstrip('共').rstrip('页'))
        itag_flag = response.etree.xpath('//ul[@class="item-lists"]/li[1]//h4/a/@href')[0]
        # 用于传参pageNum和itag，爬取链接可以为任意
        self.crawl('https://www.baidu.com', itag=itag_flag, save={'name': response.save, 'pageNum': pageNum, 'itag_flag': itag_flag}, callback=self.listPage)
    # 爬取新列表信息前将mongoDB中的历史数据状态置为0（默认resultDB不需要）
    # @config(age=15*60)
    # def reset_db_status(self,response):
    #     self.set_mongo_status(response.save['name'])
    #     self.crawl('https://google.com',save ={'name': response.save['name'],'pageNum':response.save['pageNum'],'itag_flag':response.save['itag_flag']},callback=self.listPage,itag=response.save['itag_flag'])

    @config(age=15 * 60)
    def listPage(self, response):
        # 关键字
        keyword = response.save['name']
        # 结果最大页数
        pageNum = response.save['pageNum']
        # itag
        itag_flag = response.save['itag_flag']
        # print('listpage_itag_flag:'+itag_flag)
        for i in range(1, pageNum + 1):
            #            time.sleep(random.uniform(0, 2))
            self.crawl('https://2.taobao.com/list/list.htm?st_edtime=1&page={}&_input_charset=utf8&q={}&ist=0'.format(i, keyword), itag=itag_flag, auto_recrawl=True, save={'name': keyword, 'pageNum': pageNum, 'itag_flag': itag_flag}, callback=self.listPage)

        for i in range(1, len(response.etree.xpath('//ul[@class="item-lists"]/li')) + 1):
            # 淘宝bug,列表物品简介无法正确获取时返回空
            try:
                desc = response.etree.xpath('//ul[@class="item-lists"]/li[{}]//div[@class="item-description"]/text()'.format(i))[0]
            except BaseException:
                desc = ''
            # 单独从个人URL中提取名字
            try:
                user_name = parse.unquote(response.etree.xpath('//ul[@class="item-lists"]/li[{}]//div[@class="seller-nick"]/a/@href'.format(i))[0], encoding="gbk").split('=')[1]
            except BaseException:
                user_name = ''

            self.send_message(self.project_name, {'keyword': keyword,
                                                  'title': response.etree.xpath('//ul[@class="item-lists"]/li[{}]//h4/a/text()'.format(i))[0],
                                                  'price': response.etree.xpath('//ul[@class="item-lists"]/li[{}]//span[@class="price"]/em/text()'.format(i))[0],
                                                  'desc': desc,
                                                  'pub_time': response.etree.xpath('//ul[@class="item-lists"]/li[{}]//span[@class="item-pub-time"]/text()'.format(i))[0],
                                                  'user_name': user_name,
                                                  'location': response.etree.xpath('//ul[@class="item-lists"]/li[{}]//div[@class="seller-location"]/text()'.format(i))[0],
                                                  'user_infoURL':
                                                  'https:' + response.etree.xpath('//ul[@class="item-lists"]/li[{}]//div[@class="seller-nick"]/a/@href'.format(i))[0],
                                                  'url': 'https:' + response.etree.xpath('//ul[@class="item-lists"]/li[{}]//h4/a/@href'.format(i))[0],
                                                  'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                              url='https:' + response.etree.xpath('//ul[@class="item-lists"]/li[{}]//h4/a/@href'.format(i))[0])

    def on_message(self, project, msg):
        return msg
