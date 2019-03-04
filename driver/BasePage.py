#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import time

from appium import webdriver
from appium.webdriver.webdriver import WebDriver


class BaseView(object):
    driver = None
    ''':type driver: WebDriver'''

    def initdriver(cls):
        caps = {"platformName": "android",
                "deviceName": "demo",
                "appPackage": "com.xueqiu.android",
                "appActivity": ".view.WelcomeActivityAlias",
                "unicodeKeyboard": True,
                "resetKeyboard": True,
                "autoGrantPermissions": True}
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    def getdriver(cls):
        return cls.driver

