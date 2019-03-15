#!/usr/bin/env python
# -*- Coding:utf-8 -*-

import pytest
from driver.base_driver import BaseView


@pytest.fixture(scope="function", autouse=True)
def setup():
    BaseView.init_driver()
    yield
    BaseView.get_driver().quit()
