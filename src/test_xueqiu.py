#!/usr/bin/env python
# -*- Coding:utf-8 -*-

from appium import webdriver
import pytest
import allure

class TestXueQiu:

    @allure.feature("启动设置")
    @allure.story("configbase")
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


    @allure.feature("搜索功能测试")
    @allure.story("搜索拼多多并查看股票")
    def test_search_pdd(self):
        with allure.step("点击搜索框，进入查询界面"):
            self.driver.find_element_by_id("tv_search").click()
        with allure.step("输入pdd进行搜索"):
            self.driver.find_element_by_id("search_input_text").send_keys("pdd")
        with allure.step("点击拼多多股票"):
            self.driver.find_element_by_xpath("//*[@text='拼多多']").click()
        with allure.step("检验是否正确打开拼多多股票"):
            allure.attach("预期结果", "测试通过")
            assert self.driver.find_element_by_xpath("//*[@text='拼多多']") \
                   and self.driver.find_element_by_xpath("//*[@text='美股开户']")

    @allure.feature("添加自选股功能测试")
    @allure.story("把阿里巴巴股票添加到自选股")
    def test_add_alibaba(self):
        with allure.step("点击搜索框，进入查询界面"):
            self.driver.find_element_by_id("tv_search").click()
        with allure.step("输入阿里巴巴进行搜索"):
            self.driver.find_element_by_id("search_input_text").send_keys("阿里巴巴")
        with allure.step("将搜索到的第一个股票添加到自选，检测是否已添加，已添加则跳过此步"):
            try:
                self.driver.find_element_by_xpath\
                    ("//*[contains(@resource-id,'follow_btn') and @instance=9]").click()
            except:
                print("搜索的股票已经在自选股之中")
                pass
        with allure.step("检测是否有评价界面，有则点击，然后返回上层界面"):
            try:
                self.driver.find_element_by_xpath("//*[@text='下次再说']").click()
            except:
                pass
            self.driver.back()
        with allure.step("检测是否有关注股票的tips"):
            try:
                self.driver.find_element_by_id("iv_close").click()
            except:
                pass
        with allure.step("进行自选股界面，并检测搜索的股票是否已添加在自选股当中"):
            allure.attach("预期结果", "测试通过")
            self.driver.find_element_by_xpath\
                ("//*[@text='自选' and contains(@resource-id,'tab_name')]").click()
            assert self.driver.find_element_by_xpath \
                ("//*[contains(@resource-id,'portfolio_stockName') and @text='阿里巴巴']")


if __name__ == "__main__":
    pytest.main(["-v","-p","no:warnings","--alluredir","../log/","test_xueqiu_demo.py"])