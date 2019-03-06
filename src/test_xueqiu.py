#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import time
from appium import webdriver
import pytest
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver.BasePage import BaseView
from utils.MyAppium import MyAppium


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
        BaseView.initDriver()
        print(BaseView.driver)
        yield
        BaseView.getDriver().quit()

    #封装滑动方法
    def swipe(self, by, director="up"):
        x = BaseView.getDriver().get_window_size()['width']
        y = BaseView.getDriver().get_window_size()['height']
        if director == "up":
            pass
        elif director == "down":
            pass
        elif director == "left":
            pass

    # # 封装控件查找方法，默认选择click方法，以便处理弹窗问题
    # def find(self, *args, timeout=30):
    #     end_time = time.time() + timeout
    #     while True:
    #         try:
    #             return BaseView.getDriver().find_element(*args)
    #             break
    #         except Exception as e:
    #             print(e)
    #             # 建立白名单，通过XPATH将随时可能出现的按钮处理掉
    #             whitelist = ["//*[@text='允许']", "//*[@text='创建您的专属选股策略']",
    #                          "//*[@text='下次再说']", "//*[contains(@resource-id,'iv_close')]",
    #                          "//*[contains(@resource-id,'image_cancel')]"]
    #             for key in whitelist:
    #                 if BaseView.getDriver().find_element(By.XPATH, key):
    #                     BaseView.getDriver().find_element(By.XPATH, key).click()
    #         if time.time() > end_time:
    #             break

    # 封装页面加载检测方法
    def loaded(self, no_stock=True):
        locations = []
        while True:
            if no_stock:
                loc = MyAppium().myfind(*self.optional)  # 检测主页是否加载完毕
            else:
                loc = MyAppium().myfind(*self.stock_change)  # 检测自选股是否加载完毕
            locations.append(loc.location)
            if len(locations) >= 2:
                if locations[-1] == locations[-2]:
                    break

    # 封装搜索添加股票方法
    def search_add_stock(self, stockname):
        self.loaded()  # 检测首页是否加载完成
        MyAppium().myfind(*self.tv_search).click()   # 点击搜索框
        MyAppium().myfind(*self.search_input).send_keys(stockname)
        if MyAppium().myfind(*self.add_1st).is_displayed():
            MyAppium().myfind(*self.add_1st).click()   # 点击第一只股票的添加按钮

    # 搜索并添加阿里巴巴股票
    def test_add_us(self):
        self.search_add_stock("阿里巴巴")  # 搜索阿里巴巴
        MyAppium().myfind(*self.stock_cancal).click()   # 点击搜索取消按钮
        MyAppium().myfind(*self.optional).click()   # 点击自选按钮
        MyAppium().myfind(*self.us_stock).click()   # 点击美股按钮
        assert MyAppium().myfind(*self.stock_alibaba).text == "阿里巴巴"

    # 删除添加阿里巴巴股票
    def test_delete_us(self):
        self.loaded()  # 检测首页是否加载完成
        MyAppium().myfind(*self.optional).click()  # 点击自选按钮
        self.loaded(no_stock=False)  # 检测自选股是否加载完毕
        MyAppium().myfind(*self.us_stock).click()  # 点击美股按钮
        stock_name = MyAppium().myfind(*self.stock_alibaba)
        if stock_name.is_displayed():  # 查找自选中是否有阿里巴巴股票
            TouchAction(BaseView.getDriver()).long_press(stock_name).perform()
            MyAppium().myfind(*self.stock_del)
        assert not stock_name.is_displayed()

    # 参数化添加三十只股票
    @pytest.mark.parametrize("stockname", [
        "百度", "阿里巴巴", "腾讯", "美团", "今日头条",
        "拼多多", "饿了么", "京东", "滴滴出行", "中国平安",
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
            stocks = BaseView.getDriver().find_elements_by_id("portfolio_stockName")
            for x in stocks:
                my_stocks.append(x.text)
            BaseView.getDriver().swipe(550, 1540, 550, 500, duration=400)
        my_stocks = list(set(my_stocks))  # 去掉重复元素
        return my_stocks

    # 检测某个股票是否同时在全部股票以及美股中存在
    def test_exit_in_all(self):
        self.loaded()  # 检测首页是否加载完成
        MyAppium().myfind(*self.optional).click()  # 点击自选按钮
        self.loaded(no_stock=False)  # 检测自选股是否加载完毕
        MyAppium().myfind(*self.bmp_close).click()  # 点击BMP行情关闭按钮
        all_stocks = self.get_stocks(5)
        MyAppium().myfind(*self.us_stock).click()  # 点击美股按钮
        self.loaded(no_stock=False)  # 检测美股是否加载完毕
        us_stocks = self.get_stocks(3)
        mystock= "阿里巴巴"
        assert mystock in all_stocks and mystock in us_stocks

    # def test_webview(self):
    #     self.loaded()
    #     BaseView.getDriver().find_element_by_xpath("//*[@text='交易']").click()
    #     BaseView.getDriver().find_element_by_xpath("//*[@text='基金']").click()
    #     WebDriverWait(BaseView.getDriver(), 20).until(EC.presence_of_element_located(By.XPATH, "//*[@text='已有蛋卷基金账户登录']"))
    #     contexts = BaseView.getDriver().contexts
    #     print(contexts)
    #     BaseView.getDriver().switch_to.context(contexts[1])
    #     BaseView.getDriver().find_element_by_xpath("//#[@text='已有蛋卷基金账户登录']").click()
    #     WebDriverWait(BaseView.getDriver(), 20).until(EC.presence_of_element_located(By.XPATH, "//*[@text='使用密码登录']"))
    #     contexts = BaseView.getDriver().contexts
    #     print(contexts)
    #     BaseView.getDriver().switch_to.context(contexts[1])
    #     BaseView.getDriver().find_element_by_xpath("//#[@text='使用密码登录']").click()
    #     BaseView.getDriver().find_element_by_xpath("//#[@text='请输入手机号']").send_keys('13312345678')
    #     BaseView.getDriver().find_element_by_xpath("//#[@text='请输入密码']").send_keys('dsadsaf')
    #     BaseView.getDriver().find_element_by_xpath("//#[@text='安全登录']").click()

    # def test_page_source(self):
    #     self.loaded()
    #     print(BaseView.getDriver().page_source)
    #     test = ["//*[contains(@resource-id,'image_cancel')]",
    #             "//*[@text='自选' and contains(@resource-id,'tab_name')]",
    #             "tv_search","tab_name","//*[@text='美股']"]
    #     for i in test:
    #         print(i)
    #         print(i in BaseView.getDriver().page_source)


if __name__ == "__main__":
    pytest.main(["-v", "test_xueqiu.py"])
