#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from appium import webdriver


class BaseView(object):
    # def __init__(self):
    #     caps = {"platformName": "android",
    #             "deviceName": "demo",
    #             "appPackage": "com.xueqiu.android",
    #             "appActivity": ".view.WelcomeActivityAlias",
    #             "unicodeKeyboard": True,
    #             "resetKeyboard": True,
    #             "autoGrantPermissions": True}
    #     self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    #
    # def get_driver(self):
    #     return self.driver
    driver = None
    """type: webdriver"""

    @classmethod
    def getDriver(cls):
        return cls.driver

    @classmethod
    def initDriver(cls):
        caps = {"platformName": "android",
                "deviceName": "demo",
                "appPackage": "com.xueqiu.android",
                "appActivity": ".view.WelcomeActivityAlias",
                "unicodeKeyboard": True,
                "resetKeyboard": True,
                "autoGrantPermissions": True}
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        cls.driver.implicitly_wait(6)
