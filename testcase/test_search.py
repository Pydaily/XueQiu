#!/usr/bin/env python
# -*- Coding:utf-8 -*-
import pytest

from page.home_page import XueQiuHome


class TestSearch:

    @pytest.mark.parametrize("stockname", [
        "百度", "阿里巴巴", "腾讯"
    ])
    # 搜索并添加股票
    def test_add_us(self, stockname):
        assert stockname in \
               XueQiuHome().to_search().search(stockname).search_add().\
                   back_home().to_portfolio().get_all_stocks()
