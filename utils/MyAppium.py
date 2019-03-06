#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import re

import time
from selenium.webdriver.common.by import By

from driver.BasePage import BaseView


class MyAppium(object):

    # def __init__(self):
    #     self.driver = BaseView().get_driver()
    def myelement_exist(self,*args):
        myelement = BaseView.getDriver().find_elements(*args)
        if len(myelement) >= 1:
            return True
        else:
            return False

    def myfind(self, *args, timeout=30):
        end_time = time.time() + timeout
        while True:
            if self.myelement_exist(*args):
                return BaseView.getDriver().find_element(*args)
            elif time.time() > end_time:
                break
            else:
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

