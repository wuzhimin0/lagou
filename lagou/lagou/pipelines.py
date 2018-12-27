# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,json
class LagouPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host="localhost",user="root",password="123456",db="lagou",port=63295,charset="utf8")
        # 创建数据库对象，执行sql语句
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        with open(r"D:\desktop\python actual\python spider\lagou\lagou.json","a+",encoding="utf-8") as f:
            f.write(json.dumps(dict(item),ensure_ascii=False) + "\n")
        try:
            # 插入数据
            self.cursor.execute('insert into lagou(positions,salary,company_name,city,district,workYear,education,industryLables,job_detail,company_url) value("%s", "%s", "%s", "%s", "%s", "%s","%s","%s","%s","%s")'%(item["positions"], item["salary"], item["company_name"], item["city"], item["district"], item["workYear"],item["education"], item["industryLables"], item["job_detail"], item["company_url"]))
            # 提交sql语句
            self.db.commit()
        except Exception as error:
            # 打印错误
            self.db.rollback()
            print(error)
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()

