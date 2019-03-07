#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import re

import time
from selenium.webdriver.common.by import By

from driver.BasePage import BaseView


class MyAppium(object):

    # def __init__(self):
    #     self.driver = BaseView().get_driver()
    def myelement_exist(self, *args):
        myelement = BaseView.getDriver().find_elements(*args)  # 根据查找方法和定位符获取元素信息
        if len(myelement) >= 1:  # 如果元素或列表存在则不为空
            return True
        else:
            return False

    def my_find(self, *args, timeout=30):
        end_time = time.time() + timeout
        while True:
            if self.myelement_exist(*args):
                return BaseView.getDriver().find_element(*args)
            elif time.time() > end_time:
                print("查找超时，当前页面信息如下：", BaseView.getDriver().page_source)
                break
            else:
                mypage = BaseView.getDriver().page_source
                # 建立白名单，通过XPATH将随时可能出现的按钮处理掉
                whitelist = ["//*[@text='允许']", "//*[@text='创建您的专属选股策略']",
                             "//*[@text='下次再说']", "//*[contains(@resource-id,'iv_close')]",
                             "//*[contains(@resource-id,'image_cancel')]", "//*[contains(@resource-id,'closeBtn')]"]
                rule = "['](.*?)[']"
                for key in whitelist:
                    keyword = re.search(rule, key).group(1)  # 通过正则把keyword提取出来
                    if keyword in mypage:  # 检测keyword是否在当前页面存在
                        BaseView.getDriver().find_element(By.XPATH, key).click()
                        break

    def my_swipe(self, director="up", *args, list_by, list_value):
            x = BaseView.getDriver().get_window_size()['width']  # 获取当前设备的宽度
            y = BaseView.getDriver().get_window_size()['height']  # 获取当前设备的高度
            if director == "up":  # X轴不变，Y轴从下往上
                mystart_x = x * 0.5
                mystart_y = y * 0.8
                myend_x = x * 0.5
                myend_y = y * 0.2
            elif director == "down":  # X轴不变，Y轴从上往下
                mystart_x = x * 0.5
                mystart_y = y * 0.2
                myend_x = x * 0.5
                myend_y = y * 0.8
            elif director == "left":  # Y轴不变，X轴从右往左
                mystart_x = x * 0.8
                mystart_y = y * 0.5
                myend_x = x * 0.2
                myend_y = y * 0.5
            elif director == "right":  # Y轴不变，X轴从左往右
                mystart_x = x * 0.2
                mystart_y = y * 0.5
                myend_x = x * 0.8
                myend_y = y * 0.5
            else:
                print("请输入正确的滑动方向")

            while True:
                BaseView.getDriver().swipe(mystart_x, mystart_y, myend_x, myend_y, duration=400)
                if self.myelement_exist(*args):  # 检测所找元素是否存在
                    return BaseView.getDriver().find_element(*args)
                else:
                    all_elements = []
                    new_elements = []
                    elements = BaseView.getDriver().find_elements(list_by, list_value)  # 获取当前列表信息
                    if len(all_elements) == 0 and len(elements) > 0:
                        for x in elements:
                            all_elements.append(x.text)
                    elif len(elements) > 0:  # 当前列表非空
                        for x in elements:
                            new_elements.append(x.text)
                        if new_elements[:-1] == all_elements[:-1]:  # 当前最后元素与之前最后一个元素对比
                            print("滑动已到底")
                            break
                        else:
                            all_elements += new_elements
                    else:
                        print("当前列表无元素存在")
                        break
