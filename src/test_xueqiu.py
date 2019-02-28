#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from time import sleep
from appium import webdriver
import pytest
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By


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
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                       {"platformName": "android",
                                        "deviceName": "demo",
                                        "appPackage": "com.xueqiu.android",
                                        "appActivity": ".view.WelcomeActivityAlias",
                                        "unicodeKeyboard": True,
                                        "resetKeyboard": True,
                                        "autoGrantPermissions": True,
                                        'noReset': True
                                        })
        self.driver.implicitly_wait(6)
        self.find(*self.agree)  # 权限提示检测
        self.find(*self.agree)
        yield
        self.driver.quit()

    # 封装控件查找方法，默认选择click方法，以便处理弹窗问题
    def find(self, *args, autoclick=True):
        try:
            if self.driver.find_element(*args):
                if autoclick:
                    return self.driver.find_element(*args).click()
                else:
                    return self.driver.find_element(*args)
            else:
                # 建立白名单，通过XPATH将随时可能出现的按钮处理掉
                # 把else的代码放到except中处理会报错，后续需理清
                whitelist = ["//*[@text='允许']", "//*[@text='创建您的专属选股策略']",
                             "//*[@text='下次再说']", "//*[contains(@resource-id,'iv_close')]"]
                for key in whitelist:
                    if self.driver.find_element(By.XPATH, key):
                        self.driver.find_element(By.XPATH, key).click()
        except:
            pass

    # 封装页面加载检测方法
    def loaded(self, no_stock=True):
        locations = []
        while True:
            if no_stock:
                loc = self.find(*self.optional, autoclick=False)  # 检测主页是否加载完毕
            else:
                loc = self.find(*self.stock_change, autoclick=False)  # 检测自选股是否加载完毕
            locations.append(loc.location)
            if len(locations) >= 2:
                if locations[-1] == locations[-2]:
                    break

    # 封装搜索添加股票方法
    def search_add_stock(self, stockname):
        self.find(*self.cancel)  # 点击关闭更新按钮
        self.loaded()  # 检测首页是否加载完成
        self.find(*self.tv_search)  # 点击搜索框
        self.find(*self.search_input, autoclick=False).send_keys(stockname)
        self.find(*self.add_1st)  # 点击第一只股票的添加按钮
        self.find(*self.next_time)  # 处理可能出现的评价按钮

    # 搜索并添加阿里巴巴股票
    def test_add_us(self):
        self.search_add_stock("阿里巴巴")  # 搜索阿里巴巴
        self.find(*self.stock_cancal)  # 点击搜索取消按钮
        self.find(*self.follow_cancel)  # 处理可能弹出的关注tips
        self.find(*self.optional)  # 点击自选按钮
        self.find(*self.us_stock)  # 点击美股按钮
        assert self.find(*self.stock_alibaba, autoclick=False)

    # 删除添加阿里巴巴股票
    def test_delete_us(self):
        self.find(*self.cancel)  # 点击关闭更新按钮
        self.loaded()  # 检测首页是否加载完成
        self.find(*self.optional)  # 点击自选按钮
        self.loaded(no_stock=False)  # 检测自选股是否加载完毕
        self.find(*self.us_stock)  # 点击美股按钮
        el = self.find(*self.stock_alibaba, autoclick=False)  # 查找自选中是否有阿里巴巴股票
        if el:
            TouchAction(self.driver).long_press(el).perform()
            self.find(*self.stock_del)
        assert not self.find(*self.stock_alibaba, autoclick=False)

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

    # 检测美股中的股票是否在全部股票当中
    def test_exit_in_all(self):
        self.find(*self.cancel)  # 点击关闭更新按钮
        self.loaded()  # 检测首页是否加载完成
        self.find(*self.optional)  # 点击自选按钮
        self.loaded(no_stock=False)  # 检测自选股是否加载完毕
        self.find(*self.bmp_close)  # 点击BMP行情关闭按钮
        all_stocks = []
        for i in range(5):
            stocks = self.driver.find_elements_by_id("portfolio_stockName")
            for x in stocks:
                all_stocks.append(x.text)
            self.driver.swipe(550, 1540, 550, 500, duration=400)
        all_stocks = list(set(all_stocks))  # 去掉重复元素

        self.find(*self.us_stock)  # 点击美股按钮
        self.loaded(no_stock=False)  # 检测自选股是否加载完毕
        for j in range(3):
            us_stocks = self.driver.find_elements_by_id("portfolio_stockName")
            for y in us_stocks:
                assert y.text in all_stocks
            sleep(2)
            self.driver.swipe(550, 1540, 550, 500, duration=400)


if __name__ == "__main__":
    pytest.main(["-v", "test_xueqiu.py"])
