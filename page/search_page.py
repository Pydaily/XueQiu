#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from driver.base_page import BaseView
from utils.my_appium import MyAppium
from utils.my_method import MyMethod


class Search(object):
    _search_input = (By.ID, "search_input_text")  # 搜索输入框
    _add_1st = (By.XPATH, "//*[contains(@resource-id,'follow_btn') and @instance=9]")  # 每个搜索的第一只股票
    _stock_cancel = (By.ID, "action_close")  # 搜索取消按钮
    _optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮

    def search(self, keyword):
        MyAppium().my_find(*self._search_input).send_keys(keyword)
        return self

    def search_add(self):
        stock_added = MyAppium().myelement_exist(*self._add_1st)  # 检测股票是否已添加
        if stock_added:
            MyAppium().my_find(*self._add_1st).click()
        return self

    def to_portfoli(self):
        MyAppium().my_find(*self._stock_cancel).click()
        MyAppium().my_find(*self._optional).click()
        MyMethod().loaded(False)
        return self

    def get_stocks(self):
        return BaseView.getdriver().find_element_by_id("stock").text

    def get_username(self):
        Search.search()
        return BaseView.getdriver().find_element_by_id("user_name").text
