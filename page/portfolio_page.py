#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from page.search_page import Search
from page.stock_manage import StockManage
from page.base_page import BasePage


class Portfolio(BasePage):
    _search_button = (By.ID, "action_create_cube")
    _stock_manage = (By.ID, "edit_group")
    _all_stocks_name = (By.ID, "portfolio_stockName")

    def to_search(self):
        self.find(*self._search_button).click()
        return Search()

    def to_stock_manage(self):
        self.find(*self._stock_manage).click()
        return StockManage()

    def group_select(self, group_name):
        self.find(By.XPATH, By.XPATH, "//*[@text='" + group_name + "']").click()
        return self

    def add_stock_in_group(self):
        pass

    def get_all_stocks(self):
        return self.get_elements_text("up", *self._all_stocks_name)

    def delete_stocks_from_all(self,stockname):
        pass
