#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from appium import webdriver
from appium.webdriver.webdriver import WebDriver


class Appium(object):
    driver = None
    ''':type driver: WebDriver'''

    def initdriver(cls):
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                       {"platformName": "android",
                                        "deviceName": "demo",
                                        "appPackage": "com.xueqiu.android",
                                        "appActivity": ".view.WelcomeActivityAlias",
                                        "unicodeKeyboard": True,
                                        "resetKeyboard": True,
                                        "autoGrantPermissions": True,
                                        "noReset":True
                                        })
    def getdriver(cls):
        return cls.driver