#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from XueQiu.page.Search import Search

from driver.BasePage import BaseView


class Xueqiu(object):
    def tosearch(self):
        BaseView.getdriver().find_element_by_id("home_search").click()
        return Search()