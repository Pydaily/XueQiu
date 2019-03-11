#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By

from page.portfolio_page import Portfolio
from page.search_page import Search
from page.base_page import BasePage
from utils.my_method import MyMethod


class XueQiuHome(BasePage):
    tv_search = (By.ID, "tv_search")  # 搜索框
    portfolio = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮

    def to_search(self):
        MyMethod().loaded()  # 检测首页是否加载完成
        self.my_find(*self.tv_search).click()
        return Search()

    def to_portfolio(self):
        MyMethod().loaded()
        self.my_find(*self.portfolio).click()
        return Portfolio()
