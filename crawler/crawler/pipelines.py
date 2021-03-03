# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from model.db_loader import MySQL
import json
import datetime
from crawler.data_controller import arr2str

sql_db = MySQL(key_file='../keys/aws_sql_key.json',
               database='crawl_job')
with open('model/dtype_map.json') as file :
    dtype_map = json.load(file)

class CrawlerPipeline:
    def create_sql_item(self,item,dtype) :
        if dtype == 'string' or 'datetime':
            return "'{}'".format(item)
        elif dtype == 'bool' or 'int':
            return "{}".format(item)
            
    def process_item(self, items, spider):
        print('@'*10,'pipeline','@'*10)
        key_arr = []
        item_arr = []
        # print(items)
        for key, item in items.items() :
            if item != None :
                key_arr.append(key)
                item_arr.append(self.create_sql_item(item,dtype=dtype_map[key]))
        
        sql_db.insert_data('job_detail',arr2str(key_arr),arr2str(item_arr))
        print('[Success]insert data for mysql')
        return items

    def open_spider(self,spider) :
        sql_db.MYSQL_CONN = sql_db.conn_mysqldb()

