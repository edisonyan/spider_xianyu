from pyspider.result import ResultWorker
import pymongo



class MyResultWorker(ResultWorker):
    def on_result(self, task, result):
        assert task['taskid']
        assert task['project']
        assert task['url']
        assert result
        if not result:
            return

        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['pyspider_resultdb']
        coll = db['xianyu_list']

        #判断为收购类型
        item_type = 'sell'
        sell_keyword = ['收','求购']
        for k in sell_keyword:
            if k in result['title'] or k in result['desc']:
                item_type = 'buy'
                
        #定义数据库
        data = {
            'taskid': task['taskid'],
            'url': result['url'],
            'title': result['title'],
            'keyword': result['keyword'],
            'price': result['price'],
            'description': result['desc'],
            'user_name': result['user_name'],
            'location': result['location'],
            'user_infoURL': result['user_infoURL'],
            'pub_time': result['pub_time'],
            'status': '1',  # 取得的数据默认为1
            'type': item_type,#买卖类型
            'crawl_time': result['crawl_time']
        }

        # 判断如果存在记录则更新,否则插入
        if coll.find_one({'url': result['url']}):
            data_id = coll.update({'url': result['url']}, {'$set': data})
            print('update:' + str(data_id))
        else:
            data_id = coll.insert(data)
            print('insert:' + str(data_id))
