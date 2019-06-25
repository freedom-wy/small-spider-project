from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Float,Date
from sqlalchemy.orm import sessionmaker
import time


#创建数据库连接
engine = create_engine("mysql+pymysql://root:abcd1234@127.0.0.1:3306/lagou?charset=utf8")

#声明一个基类
Base = declarative_base()

#操作数据库需要使用session
Session = sessionmaker(bind=engine)

class Lagoutables(Base):
    __tablename__ = 'lagou_data'

    #id
    id = Column(Integer,primary_key=True,autoincrement=True)
    #岗位ID
    positionId = Column(Integer,nullable=False)
    #经度
    longitude = Column(Float,nullable=False)
    #纬度
    latitude = Column(Float,nullable=False)
    #岗位名称
    positionName = Column(String(length=50),nullable=False)
    #工作年限
    workYear = Column(String(length=20),nullable=False)
    #学历
    education = Column(String(length=20),nullable=False)
    #岗位性质
    jobNature = Column(String(length=20),nullable=True)
    #公司类型
    financeStage = Column(String(length=30),nullable=True)
    #公司规模
    companySize = Column(String(length=30),nullable=True)
    #业务方向
    industryField = Column(String(length=30),nullable=True)
    #所在城市
    city = Column(String(length=10),nullable=False)
    #岗位标签
    positionAdvantage = Column(String(length=200),nullable=True)
    #公司简称
    companyShortName = Column(String(length=50),nullable=True)
    #公司全称
    companyFullName = Column(String(length=200),nullable=True)
    #公司所在区
    district = Column(String(length=20),nullable=True)
    #公司福利标签
    companyLabelList = Column(String(length=200),nullable=True)
    #工资
    salary = Column(String(length=20),nullable=False)
    #抓取日期
    crawl_date = Column(Date,nullable=False)

#创建表
# Lagoutables.metadata.create_all(engine)

class HandleLagouData(object):
    def __init__(self):
        self.mysql_session = Session()
        self.item = Lagoutables()

    def insert_item(self,item):
        date = time.strftime("%Y-%m-%d", time.localtime())
        data = Lagoutables(
            # 岗位ID
            positionId = item['positionId'],
            # 经度
            longitude = item['longitude'],
            # 纬度
            latitude = item['latitude'],
            # 岗位名称
            positionName = item['positionName'],
            # 工作年限
            workYear = item['workYear'],
            # 学历
            education = item['education'],
            # 岗位性质
            jobNature = item['jobNature'],
            # 公司类型
            financeStage = item['financeStage'],
            # 公司规模
            companySize = item['companySize'],
            # 业务方向
            industryField = item['industryField'],
            # 所在城市
            city = item['city'],
            # 岗位标签
            positionAdvantage = item['positionAdvantage'],
            # 公司简称
            companyShortName = item['companyShortName'],
            # 公司全称
            companyFullName = item['companyFullName'],
            # 公司所在区
            district = item['district'],
            # 公司福利标签
            companyLabelList = ','.join(item['companyLabelList']),
            salary = item['salary'],
            # 抓取日期
            crawl_date = item['crawl_date']
            )
        query_result = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_date==date,Lagoutables.positionId==item['positionId']).first()
        if query_result:
            print('该岗位信息已存在%s:%s:%s'%(item['positionId'],item['city'],item['positionName']))
        else:
            self.mysql_session.add(data)
            self.mysql_session.commit()
            print('新增岗位信息%s'%item['positionId'])
            return self.item

lagou_mysql = HandleLagouData()
# item = {'positionId':6009711}
# lagou_mysql.insert_item(item)
