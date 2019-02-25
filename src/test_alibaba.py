#!/usr/bin/env python
# -*- Coding:utf-8 -*-
from appium import webdriver
import pytest
from appium.webdriver.common.touch_action import TouchAction


class TestXueQiu:

    @pytest.fixture(scope="function", autouse=True)  # 如果scope设置为class，则需要return driver 并将base作为参数传入后续用例调用
    def base(self):
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                       {"platformName":"android",
                                        "deviceName":"demo",
                                        "appPackage":"com.xueqiu.android",
                                        "appActivity":".view.WelcomeActivityAlias",
                                        "unicodeKeyboard":True,
                                        "resetKeyboard":True,
                                        "autoGrantPermissions":True
                                        })
        self.driver.implicitly_wait(6)
        try:
            self.driver.find_element_by_id("btn_allow").click()
        except:
            pass

        try:
            self.driver.find_element_by_id("btn_allow").click()
        except:
            pass


        yield
        self.driver.quit()


    def test_alibaba_search(self):
        self.driver.find_element_by_xpath \
            ("//*[@text='自选' and contains(@resource-id,'tab_name')]").click()  # 点击自选按钮
        self.driver.find_element_by_id("action_create_cube").click()  # 点击搜索按钮
        self.driver.find_element_by_id("search_input_text").send_keys("阿里巴巴")  # 输入阿里巴巴进行搜索
        before = self.driver.find_element_by_id("add_attention").\
            find_element_by_class_name("android.widget.TextView").get_attribute("resourceId")
        if before == "com.xueqiu.android:id/follow_btn":
            self.driver.find_element_by_id("follow_btn").click()
            after = self.driver.find_element_by_id("add_attention").\
                find_element_by_class_name("android.widget.TextView").get_attribute("resourceId")
            assert before != after # 通过按钮的ID判断状态是否变化

        try:
            self.driver.find_element_by_xpath("//*[@text='下次再说']").click()  # 检测是否有评价弹窗，有则点击下次再说
        except:
            pass
        self.driver.find_element_by_id("action_close").click()  # 点击取消按钮，返回自选界面
        assert self.driver.find_element_by_id("portfolio_whole_item"). \
              find_element_by_id("portfolio_stockName"). \
              get_attribute("text") == "阿里巴巴"

    def test_touch(self):
        locations = []
        while True:
            location = self.driver.find_element_by_xpath \
                ("//*[@text='自选' and contains(@resource-id,'tab_name')]")
            locations.append(location.location)
            if len(locations) >= 2:
                if locations[-1] == locations[-2]:
                    break
        self.driver.find_element_by_xpath \
            ("//*[@text='自选' and contains(@resource-id,'tab_name')]").click()

        element = self.driver.find_element_by_xpath("//*[@text='阿里巴巴']")
        TouchAction(self.driver).long_press(element).perform()
        self.driver.find_element_by_xpath("//*[@text='删除']").click()
        assert self.driver.find_element_by_id("portfolio_whole_item"). \
              find_element_by_id("portfolio_stockName"). \
              get_attribute("text") != "阿里巴巴"


        self.driver.find_element(b)