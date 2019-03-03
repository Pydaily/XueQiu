#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from XueQiu.driver import Appium
from XueQiu.page.Search import Search


class Xueqiu(object):
    def tosearch(self):
        Appium.getdriver().find_element_by_id("home_search").click()
        return Search()