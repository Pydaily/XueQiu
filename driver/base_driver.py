#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from appium import webdriver
from appium.webdriver import WebElement


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
    driver = None  # type: webdriver

    @classmethod
    def get_driver(cls) -> WebElement:
        return cls.driver

    @classmethod
    def init_driver(cls):
        caps = {"platformName": "android",
                "deviceName": "demo",
                "appPackage": "com.xueqiu.android",
                "appActivity": ".view.WelcomeActivityAlias",
                "unicodeKeyboard": True,
                "resetKeyboard": True,
                "autoGrantPermissions": True}
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        cls.driver.implicitly_wait(6)
