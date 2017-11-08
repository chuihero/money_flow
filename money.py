# coding = utf-8
import time
import datetime
import re

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
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
        self.brower.get(self.URL)
        money_flows = []

        # 获取当前页面流量数据
        def get_flow():
            _flows = self.brower.find_element_by_xpath("//div[@class='main']//div[@class='content']/table/tbody")
            flows = _flows.text.split('\n')
            return flows

        # next page
        # next_page = self.brower.find_element_by_xpath("//div[@class='PageNav']/div").find_element_by_link_text('下一页')
        while True:
            # 不到最后一页
            money_flows.extend(get_flow())

            next_page = self.brower.find_element_by_xpath("//div[@class='PageNav']/div").find_element_by_link_text('下一页')
            if next_page.get_attribute('class') == 'nolink':
                break

            current_page = self.brower.find_element_by_xpath("//div[@class='PageNav']/div/span[@class='at']").text
            next_page.click()
            # time.sleep(3)

            while True:
                try:
                    now_page = self.brower.find_element_by_xpath("//div[@class='PageNav']/div/span[@class='at']").text
                except StaleElementReferenceException:
                    print('too fast')
                    time.sleep(3)
                    continue
                if current_page != now_page:
                    break
                time.sleep(3)

            while current_page == self.brower.find_element_by_xpath("//div[@class='PageNav']/div/span[@class='at']").text:
                time.sleep(3)
            print('next page!')

        return money_flows








Base = declarative_base()
class StockMoneyFlow(Base):
    __tablename__ = 'money_flow'

    date = Column(Date,primary_key=True)
    code = Column(String(6),primary_key=True)
    price = Column(Float)
    net_change = Column(Float)
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

    def seq_items(self,money_flows):
        """

        :param money_flows:list，从爬虫到处的list。
        ['1 002156 通富微电 详情 数据 股吧 12.09 10.01% 2.06亿 33.94% 1.89亿 31.18% 1669万 2.75% -8679万 -14.32% -1.19亿 -19.62%',]

        :return:  list,其中元素为StockMoneyFlow
        """
        self.items = []
        date = str(datetime.date.today())

        for line in money_flows:
            i = line.split()
            flow = StockMoneyFlow()
            flow.date = date
            flow.code = i[1]

            # 判断是否停牌
            if '-' == i[6]\
                or '-' == i[7]:
                flow.price = None
                flow.net_change = None
                flow.main_fund = None
                flow.main_fund_percent = None
                flow.super_bid = None
                flow.super_percent = None
                flow.big_bid = None
                flow.big_percent = None
                flow.medium_bid = None
                flow.medium_percent = None
                flow.small_bid = None
                flow.small_percent = None
            else:
                flow.price = float(re.findall(r'(\d*.?\d+)',i[6])[0])
                flow.net_change = float(re.findall(r'(\d*.?\d+)',i[7])[0])
                if '-'==i[8] or '-'==i[9]:
                    flow.main_fund = None
                    flow.main_fund_percent = None
                else:
                    # 需要区别单位是亿还是万。这里归一化为万
                    flow.main_fund = float(re.findall(r'(\d*.?\d+)',i[8])[0]) * (10000.0 if i[8][-1]=='亿' else 1.0)
                    flow.main_fund_percent = float(re.findall(r'(\d*.?\d+)',i[9])[0])/100.0

                if '-'==i[10] or '-'==i[11]:
                    flow.big_bid = None
                    flow.big_percent = None
                else:
                    # 需要区别单位是亿还是万。这里归一化为万
                    flow.big_bid = float(re.findall(r'(\d*.?\d+)',i[10])[0]) * (10000.0 if i[10][-1]=='亿' else 1.0)
                    flow.big_percent = float(re.findall(r'(\d*.?\d+)',i[11])[0])/100.0

                if '-'==i[12] or '-'==i[13]:
                    flow.super_bid = None
                    flow.super_percent = None
                else:
                    # 需要区别单位是亿还是万。这里归一化为万
                    flow.super_bid = float(re.findall(r'(\d*.?\d+)',i[12])[0]) * (10000.0 if i[12][-1]=='亿' else 1.0)
                    flow.super_percent = float(re.findall(r'(\d*.?\d+)',i[13])[0])/100.0

                if '-'==i[14] or '-'==i[15]:
                    flow.medium_bid = None
                    flow.medium_percent = None
                else:
                    # 需要区别单位是亿还是万。这里归一化为万
                    flow.medium_bid = float(re.findall(r'(\d*.?\d+)',i[14])[0]) * (10000.0 if i[14][-1]=='亿' else 1.0)
                    flow.medium_percent = float(re.findall(r'(\d*.?\d+)',i[15])[0])/100.0

                if '-'==i[16] or '-'==i[17]:
                    flow.small_bid = None
                    flow.small_percent = None
                else:
                    # 需要区别单位是亿还是万。这里归一化为万
                    flow.small_bid = float(re.findall(r'(\d*.?\d+)',i[16])[0]) * (10000.0 if i[16][-1]=='亿' else 1.0)
                    flow.small_percent = float(re.findall(r'(\d*.?\d+)',i[17])[0])/100.0
            self.items.append(flow)



    def to_sql(self):
        """
        将内容插入到数据库
        :return:
        """
        Session = sessionmaker(bind=self.sql)
        session = Session()
        primary_code = [] # 防止出现duplicate key的情况
        for i in self.items:
            # 重复数据
            if i.code in primary_code:
                continue
            session.add(i)
            primary_code.append(i.code)

        session.commit()



if __name__ == '__main__':
    dfcf = DongFangCaiFuWebSpider()
    flows = dfcf.scrapy_web()

    sql = SqlManager()

    sql.seq_items(flows)
    sql.to_sql()
