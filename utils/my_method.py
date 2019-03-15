#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By
from page.base_page import BasePage


class MyMethod(object):
    _optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮
    _stock_code = (By.ID, "portfolio_stockCode")  # 股票英文名

    # 封装页面加载检测方法
    def loaded(self, no_stock=True):
        locations = []
        while True:
            if no_stock:
                loc = BasePage().find(*self._optional)  # 检测主页是否加载完毕
            else:
                loc = BasePage().find(*self._stock_code)  # 检测自选股是否加载完毕
            locations.append(loc.location)
            if len(locations) >= 2 and locations[-1] == locations[-2]:
                break
