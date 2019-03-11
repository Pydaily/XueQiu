#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import pytest
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver.base_driver import BaseView
from page.home_page import XueQiuHome
from page.base_page import BasePage
from utils.my_method import MyMethod


class TestXueQiu:
    agree = (By.XPATH, "//*[@text='允许']")  # 允许按钮
    optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮
    tv_search = (By.ID, "tv_search")  # 搜索框
    search_input = (By.ID, "search_input_text")  # 搜索输入框
    cancel = (By.ID, "image_cancel")  # 取消更新按钮
    add_1st = (By.XPATH, "//*[contains(@resource-id,'follow_btn') and @instance=9]")  # 每个搜索的第一只股票
    next_time = (By.XPATH, "//*[@text='下次再说']")  # 下次再说按钮
    stock_cancal = (By.ID, "action_close")  # 搜索取消按钮
    follow_cancel = (By.ID, "iv_close")  # 关注取消按钮
    us_stock = (By.XPATH, "//*[@text='美股']")  # 美股按钮
    stock_change = (By.ID, "btn_change")  # 涨跌幅按钮
    stock_alibaba = (By.XPATH, "//*[contains(@resource-id,'portfolio_stockName') and @text='阿里巴巴']")  # 阿里巴巴股票
    stock_del = (By.XPATH, "//*[@text='删除']")  # 删除按钮
    bmp_close = (By.ID, "closeBtn")  # BMP关闭按钮

    @pytest.fixture(scope="function", autouse=True)  # 如果scope设置为class，则需要return driver 并将base作为参数传入后续用例调用
    def base(self):
        BaseView.init_driver()
        yield
        BaseView.get_driver().quit()

    # 封装搜索添加股票方法
    def search_add_stock(self, stockname):
        home_page = XueQiuHome()
        search = home_page.to_search()
        search.search(stockname)
        search.search_add()

    @pytest.mark.parametrize("stockname", [
        "百度", "阿里巴巴", "腾讯"
    ])
    # 搜索并添加股票
    def test_add_us(self, stockname):
        home_page = XueQiuHome()
        search = home_page.to_search()
        search.search(stockname)
        search.search_add()
        search.to_portfoli()
        assert stockname in BaseView.get_driver().page_source


    # 删除添加阿里巴巴股票
    def test_delete_us(self):
        MyMethod().loaded()  # 检测首页是否加载完成
        BasePage().my_find(*self.optional).click()  # 点击自选按钮
        BasePage().my_find(*self.us_stock).click()  # 点击美股按钮
        stock_name = BasePage().myelement_exist(*self.stock_alibaba)
        if stock_name:  # 查找自选中是否有阿里巴巴股票
            sn = BasePage().my_find(*self.stock_alibaba)
            TouchAction(BaseView.get_driver()).long_press(sn).perform()
            BasePage().my_find(*self.stock_del).click()
        assert stock_name != True

    # 参数化添加三十只股票
    @pytest.mark.parametrize("stockname", [
        "百度", "阿里巴巴", "腾讯", "美团", "今日头条",
        "拼多多", "京东", "滴滴出行", "中国平安",
        "中国联通", "中国移动", "Facebook", "Google", "大疆",
        "雅虎", "微软", "高通", "小米", "格力",
        "oppo", "vivo手机", "苹果", "美的", "恒大",
        "蚂蚁金服", "网易", "陌陌", "中国人保", "京东方"
    ])
    def test_add_batch(self, stockname):
        self.search_add_stock(stockname)

    # 封装查询某项所有股票名方法
    def get_stocks(self, times):
        my_stocks = []
        for i in range(times):
            stocks = BaseView.get_driver().find_elements_by_id("portfolio_stockName")
            for x in stocks:
                my_stocks.append(x.text)
            BaseView.get_driver().swipe(550, 1540, 550, 500, duration=400)
        my_stocks = list(set(my_stocks))  # 去掉重复元素
        return my_stocks

    # 检测某个股票是否同时在全部股票以及美股中存在
    def test_exit_in_all(self):
        MyMethod().loaded()  # 检测首页是否加载完成
        BasePage().my_find(*self.optional).click()  # 点击自选按钮
        MyMethod().loaded(no_stock=False)  # 检测自选股是否加载完毕
        BasePage().my_find(*self.bmp_close).click()  # 点击BMP行情关闭按钮
        all_stocks = self.get_stocks(5)
        BasePage().my_find(*self.us_stock).click()  # 点击美股按钮
        MyMethod().loaded(no_stock=False)  # 检测美股是否加载完毕
        us_stocks = self.get_stocks(3)
        mystock= "阿里巴巴"
        assert mystock in all_stocks and mystock in us_stocks

    def test_webview(self):
        MyMethod().loaded()
        BaseView.get_driver().find_element_by_xpath("//*[@text='交易']").click()
        BaseView.get_driver().find_element_by_xpath("//*[@text='基金']").click()
        WebDriverWait(BaseView.get_driver(), 20).until(EC.presence_of_element_located(By.XPATH, "//*[@text='已有蛋卷基金账户登录']"))
        contexts = BaseView.get_driver().contexts
        print(contexts)
        BaseView.get_driver().switch_to.context(contexts[1])
        BaseView.get_driver().find_element_by_xpath("//#[@text='已有蛋卷基金账户登录']").click()
        WebDriverWait(BaseView.get_driver(), 20).until(EC.presence_of_element_located(By.XPATH, "//*[@text='使用密码登录']"))
        contexts = BaseView.get_driver().contexts
        print(contexts)
        BaseView.get_driver().switch_to.context(contexts[1])
        BaseView.get_driver().find_element_by_xpath("//*[@text='使用密码登录']").click()
        BaseView.get_driver().find_element_by_xpath("//*[@text='请输入手机号']").send_keys('13312345678')
        BaseView.get_driver().find_element_by_xpath("//*[@text='请输入密码']").send_keys('dsadsaf')
        BaseView.get_driver().find_element_by_xpath("//*[@text='安全登录']").click()


if __name__ == "__main__":
    pytest.main(["-v", "test_xueqiu.py"])
