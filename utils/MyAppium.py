#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import re

from driver.BasePage import BaseView
import time
from selenium.webdriver.common.by import By


class MyAppium(object):

    # def __init__(self):
    #     self.driver = BaseView().get_driver()

    def myfind(self, *args, timeout=60):
        end_time = time.time() + timeout
        while True:
            try:
                return BaseView.getDriver().find_element(*args)
            except Exception as e:
                print(e)
                mypage = BaseView.getDriver().page_source
                # 建立白名单，通过XPATH将随时可能出现的按钮处理掉
                whitelist = ["//*[@text='允许']", "//*[@text='创建您的专属选股策略']",
                             "//*[@text='下次再说']", "//*[contains(@resource-id,'iv_close')]",
                             "//*[contains(@resource-id,'image_cancel')]"]
                rule = "['](.*?)[']"
                for key in whitelist:
                    keyword = re.search(rule, key).group(1)
                    if keyword in mypage:
                        BaseView.getDriver().find_element(By.XPATH, key).click()
                        break
            if time.time() > end_time:
                print("超时")
                break
