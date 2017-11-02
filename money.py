# coding = utf-8
from selenium import webdriver
from sqlstr import SQLSTR

class DongFangCaiFuWebSpider():
    """
    东方财富个股资金流向爬虫
    "http://data.eastmoney.com/zjlx/detail.html"
    """
    def __init__(self):
        pass

    def scrapy_web(self):
        """
        爬取页面上个股资金流向信息
        :return:
        个股资金流向的数据结构
        """
        pass


class SqlManager():
    """
    数据库结构，将抓取的内容导入数据库
    """
    def __init__(self):
        pass

    def to_sql(self):
        """
        将内容插入到数据库
        :return:
        """
        pass
