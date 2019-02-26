#!/usr/bin/env python
# -*- Coding:utf-8 -*-

from appium import webdriver
import pytest
from selenium.webdriver.common.by import By


class TestXueQiu:
    @pytest.fixture(scope="function", autouse=True)  # 如果scope设置为class，则需要return driver 并将base作为参数传入后续用例调用
    def base(self):
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                       {"platformName": "android",
                                        "deviceName": "demo",
                                        "appPackage": "com.xueqiu.android",
                                        "appActivity": ".view.WelcomeActivityAlias",
                                        "unicodeKeyboard": True,
                                        "resetKeyboard": True,
                                        "autoGrantPermissions": True
                                        })
        self.driver.implicitly_wait(6)
        # 权限弹窗允许检测
        self.find(By.XPATH, "//*[@text='允许']")
        self.find(By.XPATH, "//*[@text='允许']")
        yield
        self.driver.quit()

    # 封装click方法,如果将其改成通用有以下问题:当控件未找到时.click()或者其他操作会报错
    # 那样会需要每次增加相应的If判断，后续考虑如何解决
    def find(self, id, value):
        try:
            if self.driver.find_element(id, value):
                return self.driver.find_element(id, value).click()
            else:
                # 建立白名单，通过XPATH将随时可能出现的按钮处理掉
                # 把else的代码放到except中处理会报错，后续需理清
                whitelist = ["//*[@text='允许']", "//*[@text='创建您的专属选股策略']",
                             "//*[@text='下次再说']", "//*[contains(@resource-id,'iv_close')]"]
                for key in whitelist:
                    if self.driver.find_element(By.XPATH, key):
                        self.driver.find_element(By.XPATH, key).click()
        except:
            pass

    def loaded(self):
        locations = []
        while True:
            loc = self.driver.find_element_by_xpath("//*[@text='自选' and contains(@resource-id,'tab_name')]")
            print(loc)
            locations.append(loc.location)
            if len(locations) >= 2:
                if locations[-1] == locations[-2]:
                    break

    def test_search_pdd(self):
        self.loaded()
        print("加载完成")
#        self.driver.find_element(By.XPATH, "//*[@text='自选' and contains(@resource-id,'tab_name')]").click()
        self.find(By.ID, "tv_search")
        self.driver.find_element_by_id("search_input_text").send_keys("pdd")
        self.find(By.XPATH, "//*[@text='拼多多']")
        assert self.driver.find_element_by_xpath("//*[@text='拼多多']") \
               and self.driver.find_element_by_xpath("//*[@text='美股开户']")


if __name__ == "__main__":
    pytest.main(["-v", "test_xueqiu.py"])
