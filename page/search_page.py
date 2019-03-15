#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from driver.base_driver import BaseView
from page.base_page import BasePage
from page.home_page import XueQiuHome


class Search(BasePage):
    _search_input = (By.ID, "search_input_text")  # 搜索输入框
    _add_1st = (By.XPATH, "//*[contains(@resource-id,'follow_btn') and @instance=9]")  # 每个搜索的第一只股票
    _stock_cancel = (By.ID, "action_close")  # 搜索取消按钮
    _optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮
    _stocks_name = (By.ID, "portfolio_stockName")

    def search(self, keyword):
        BasePage().find(*self._search_input).send_keys(keyword)
        return self

    def search_add(self):
        stock_added = BasePage().element_exist(*self._add_1st)  # 检测股票是否已添加
        if stock_added:
            BasePage().find(*self._add_1st).click()
        return self

    def back_home(self):
        BasePage().find(*self._stock_cancel).click()
        return XueQiuHome()

    def get_stocks(self):
        return self.get_elements_text("up", *self._stocks_name)

    def get_username(self):
        Search.search()
        return BaseView.getdriver().find_element_by_id("user_name").text
