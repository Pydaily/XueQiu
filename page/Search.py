#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from XueQiu.driver import Appium


class Search(object):
    def search(self, keyword):
        Appium.getdriver().find_element_by_id("search_input_text").send_keys(keyword)
        return self

    def getstocks(self):
        return Appium.getdriver().find_element_by_id("stock").text

    def getusername(self):
        Search.search()
        return Appium.getdriver().find_element_by_id("user_name").text
