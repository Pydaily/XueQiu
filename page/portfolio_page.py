#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from page.search_page import Search
from page.stock_manage import StockManage
from utils.my_appium import MyAppium


class Portfolio(MyAppium):
    _search_button = (By.ID, "action_create_cube")
    _stock_manage = (By.ID, "edit_group")
    def to_search(self):
        self.my_find(*self._search_button).click()
        return Search()

    def to_stock_manage(self):
        self.my_find(*self._stock_manage).click()
        return StockManage()

    def group_select(self,group_name):
        self.my_find(By.XPATH, By.XPATH, "//*[@text='" + group_name + "']").click()
        return self

    def add_stock_in_group(self):
        self.my
