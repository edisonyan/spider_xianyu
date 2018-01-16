# spider_xianyu
a crawler case for xianyu base on pyspider

# Features
* crawl xianyu list page data(title,desc,userinfo,location,price...) 

# Dependencies
Use Python 3 and 
* [pyspider](https://github.com/binux/pyspider)
* [mongoDB(optional)](https://www.mongodb.com/)
* [fake-useragent(optional)](https://github.com/hellysmile/fake-useragent)


# Install and Configuration
* pip install pyspider
* run command pyspider, visit http://localhost:5000/
* create project
* Copy the script code in my_result_worker.py file to pyspider webdav mode
* Only tested on Mac OS X 10.13 and Debian 9

# Running
Downloading and viewing your data from WebUI is convenient, but may not suitable for computer.
If want to store the cralwed date to local database, It's highly recommended to override [ResultWorker](https://github.com/edisonyan/spider_xianyu/blob/master/my_result_worker.py). 
and you can use command-line to specify the parameters. A [config file](https://github.com/edisonyan/spider_xianyu/blob/master/config.json) is a better choice.

For example command-line in my machine:
```python

        pyspider -c config.json --logging-config logging.conf
```
## Documentation
* [Pyspider](http://docs.pyspider.org/en/latest/)
