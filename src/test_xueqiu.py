#!/usr/bin/env python
# -*- Coding:utf-8 -*-

from appium import webdriver
import pytest
from selenium.webdriver.common.by import By


class TestXueQiu:
    agree = (By.XPATH, "//*[@text='允许']")  # 允许按钮
    optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮
    tv_search = (By.ID, "tv_search")  # 搜索框
    search_input = (By.ID, "search_input_text")  # 搜索输入框
    stock_name = (By.XPATH, "//*[@text='拼多多']")
    cancel = (By.ID, "image_cancel")  # 取消更新按钮
    add_1st = (By.XPATH, "//*[contains(@resource-id,'follow_btn') and @instance=9]")  # 每个搜索的第一只股票
    next_time = (By.XPATH, "//*[@text='下次再说']")  # 下次再说按钮
    stock_cancal = (By.ID, "action_close")  # 搜索取消按钮
    follow_cancel =(By.ID, "iv_close")  # 关注取消按钮
    us_stock = (By.XPATH, "//*[@text='美股']")  # 美股按钮
    @pytest.fixture(scope="function", autouse=True)  # 如果scope设置为class，则需要return driver 并将base作为参数传入后续用例调用
    def base(self):
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                       {"platformName": "android",
                                        "deviceName": "demo",
                                        "appPackage": "com.xueqiu.android",
                                        "appActivity": ".view.WelcomeActivityAlias",
                                        "unicodeKeyboard": True,
                                        "resetKeyboard": True,
                                        "autoGrantPermissions": True
                                        })
        self.driver.implicitly_wait(6)
        # 权限弹窗允许检测
        self.find(*self.agree)
        self.find(*self.agree)
        yield
        self.driver.quit()

    # 默认选择click方法，以便处理弹窗问题
    def find(self, *args,clickcheck=True):
        try:
            if self.driver.find_element(*args):
                if clickcheck is True:
                    return self.driver.find_element(*args).click()
                else:
                    return self.driver.find_element(*args)
            else:
                # 建立白名单，通过XPATH将随时可能出现的按钮处理掉
                # 把else的代码放到except中处理会报错，后续需理清
                whitelist = ["//*[@text='允许']", "//*[@text='创建您的专属选股策略']",
                             "//*[@text='下次再说']", "//*[contains(@resource-id,'iv_close')]"]
                for key in whitelist:
                    if self.driver.find_element("By.XPATH", key):
                        self.driver.find_element("By.XPATH", key).click()
        except:
            pass

    def loaded(self):
        locations = []
        while True:
            loc = self.find(*self.optional,clickcheck=False)
            locations.append(loc.location)
            if len(locations) >= 2:
                if locations[-1] == locations[-2]:
                    break

    def test_add_us(self):
        self.find(*self.cancel)  # 点击关闭更新按钮
        self.loaded()  # 检测是否加载完成
        self.find(*self.tv_search)  #  点击搜索框
        self.find(*self.search_input,clickcheck=False).send_keys("阿里巴巴")  # 搜索阿里巴巴
        self.find(*self.add_1st)  # 点击第一只股票的添加按钮
        self.find(*self.next_time)  # 处理可能出现的评价按钮
        self.find(*self.stock_cancal) # 点击搜索取消按钮
        self.find(*self.follow_cancel)  # 处理可能弹出的关注tips
        self.find(*self.optional)  # 点击自选按钮
        self.find(*self.us_stock)  # 点击美股按钮
        assert self.driver.find_element_by_xpath \
            ("//*[contains(@resource-id,'portfolio_stockName') and @text='阿里巴巴']")


if __name__ == "__main__":
    pytest.main(["-v", "test_xueqiu.py"])
