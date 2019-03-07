#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from selenium.webdriver.common.by import By
from utils.MyAppium import MyAppium


class MyMethod:
    optional = (By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]")  # 自选按钮
    stock_change = (By.ID, "btn_change")  # 涨跌幅按钮

    # 封装页面加载检测方法
    def loaded(self, no_stock=True):
        locations = []
        while True:
            if no_stock:
                loc = MyAppium().my_find(*self.optional)  # 检测主页是否加载完毕
            else:
                loc = MyAppium().my_find(*self.stock_change)  # 检测自选股是否加载完毕
            locations.append(loc.location)
            if len(locations) >= 2 and locations[-1] == locations[-2]:
                print("页面加载完成")
                break
