# coding = utf-8
from selenium import webdriver
from sqlstr import SQLSTR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Date,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DongFangCaiFuWebSpider():
    """
    东方财富个股资金流向爬虫
    "http://data.eastmoney.com/zjlx/detail.html"
    """
    URL = 'http://data.eastmoney.com/zjlx/detail.html'
    def __init__(self):
        self.brower = webdriver.PhantomJS()

    def scrapy_web(self):
        """
        爬取页面上个股资金流向信息
        :return:
        个股资金流向的数据结构
        """
        self.brower.get(URL)


Base = declarative_base()
class StockMoneyFlow(Base):
    __tablename__ = 'money_flow'

    date = Column(Date,primary_key=True)
    code = Column(String(6),primary_key=True)
    main_fund = Column(Float)
    main_fund_percent = Column(Float)
    super_bid = Column(Float)
    super_percent = Column(Float)
    big_bid = Column(Float)
    big_percent = Column(Float)
    medium_bid = Column(Float)
    medium_percent = Column(Float)
    small_bid = Column(Float)
    small_percent = Column(Float)


class SqlManager():
    """
    数据库结构，将抓取的内容导入数据库
    """
    def __init__(self):
        self.sql = create_engine(SQLSTR)
        # run only on the first time
        Base.metadata.create_all(self.sql)


    def to_sql(self):
        """
        将内容插入到数据库
        :return:
        """
        pass


if __name__ == '__main__':
    dfcf = DongFangCaiFuWebSpider()
    sql = SqlManager()
