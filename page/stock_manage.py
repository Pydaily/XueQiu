#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from page.base_page import BasePage
from page.portfolio_page import Portfolio


class StockManage(BasePage):
    _group_manage = (By.XPATH, "//*[@text='管理分组']")
    _group_add = (By.ID, "add_item")
    _group_input = (By.ID, "dialog_input_text")
    _group_submit = (By.ID, "bt_right")
    _back_portfolio = (By.ID, "action_close")
    _group_list = (By.ID, "container")
    _group_delete = (By.ID, "group_opt")

    def to_group_manage(self):
        self.my_find(*self._group_manage).click()
        return self

    def add_group(self, group_name):
        self.my_find(*self._group_add).click()
        self.my_find(*self._group_input).send_keys(group_name)
        self.my_find(*self._group_submit).click()
        return self

    def delete_group(self, group_name):
        # //*[@text='test']/preceding-sibling::*
        self.my_find(*self._group_list).my_find(By.XPATH, "//*[@text='" + group_name + "']").my_find()

    def get_group_name(self):
        pass

    def back_to_portfolio_page(self):
        self.my_find(*self._back_portfolio).click()
        return Portfolio()



