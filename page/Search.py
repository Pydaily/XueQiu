#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from driver.BasePage import BaseView
from utils.MyAppium import MyAppium
from utils.OwnMethod import MyMethod


class Search(object):
    search_input = (By.ID, "search_input_text")  # 搜索输入框
    add_1st = (By.XPATH, "//*[contains(@resource-id,'follow_btn') and @instance=9]")  # 每个搜索的第一只股票
    stock_cancal = (By.ID, "action_close")  # 搜索取消按钮
    optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮

    def search(self, keyword):
        MyAppium().my_find(*self.search_input).send_keys(keyword)
        return self

    def search_add(self):
        stock_added = MyAppium().myelement_exist(*self.add_1st)  # 检测股票是否已添加
        if stock_added:
            MyAppium().my_find(*self.add_1st).click()
        return self

    def to_optional(self):
        MyAppium().my_find(*self.stock_cancal).click()
        MyAppium().my_find(*self.optional).click()
        MyMethod().loaded(no_stock=False)
        return self

    def getstocks(self):
        return BaseView.getdriver().find_element_by_id("stock").text

    def getusername(self):
        Search.search()
        return BaseView.getdriver().find_element_by_id("user_name").text
