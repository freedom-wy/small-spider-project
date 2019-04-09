import pymysql
import time
import setting
import csv



class Handle_mysql(object):
    def __init__(self):
        self.db = pymysql.connect(host=setting.mysql_ip,port=setting.mysql_port,database=setting.mysql_database,user=setting.mysql_username,password=setting.mysql_password)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def handle_task(self):
        #获取任务关键字
        sql = "SELECT search_word FROM seo_fast_rankings WHERE state=1;"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    #插入和更新数据
    def handle_insert_db(self,item=None):
        sql_insert = """ INSERT INTO seo_baidu_m_keyword_ziran (keyword,rank,crawl_date) VALUES ("%s",'%s',"%s");""" % (item['keyword'],item['rank'],item['crawl_date'])
        try:
            self.cursor.execute(sql_insert)
            self.db.commit()
        except:
            pass
            # print(sql_insert)

mysql = Handle_mysql()
if __name__ == '__main__':
    #插入数据前先删除当日数据
    date = time.strftime("%Y-%m-%d", time.localtime())
    sql_delete = """ DELETE FROM seo_baidu_m_keyword_ziran where crawl_date='%s'"""%date
    mysql.cursor.execute(sql_delete)
    mysql.db.commit()
    #导入当日数据
    with open('baidu_m_keyword_ziran.csv','r',encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        data = next(csv_reader)
        for i in csv_reader:
            info = {}
            info['keyword'] = i[0]
            info['rank'] = i[1]
            info['crawl_date'] = i[2]
            mysql.handle_insert_db(info)
