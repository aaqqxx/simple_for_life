# encoding:utf8
import sys

reload(sys)
sys.setdefaultencoding("utf8")
from selenium import webdriver
import time

if __name__ == "__main__":
    browser = webdriver.Firefox()
    # 打开百度文库的首界面
    browser.get("https://wenku.baidu.com/")
    # 通过ID找网页的标签，找到搜索框的标签
    seek_input = browser.find_element_by_id("kw")
    # 设置搜索的内容
    contents = "饮料"
    contents = str(contents).decode("utf8")
    seek_input.send_keys(contents)
    # 找到搜索文档按钮
    seek_but = browser.find_element_by_id("sb")
    # 并点击搜索文档按钮
    seek_but.click()
    while True:
        # 获取所有的文档a标签，这里的elements指的是有多个元素,*表示的是任意的（在xpath中可以用）
        all_a = browser.find_elements_by_xpath("//*[@id=\"bd\"]/div/div/div[4]/div/dl[*]/dt/p[1]/a")
        for a in all_a:
            print a.get_attribute("href")
            print a.get_attribute("title")
            # 获取body标签，的html
        body = browser.find_element_by_tag_name("body")
        body_html = body.get_attribute("innerHTML")
        # 判断下一页按钮是否存在
        flag = str(body_html).find("class=\"next\"")
        if flag != -1:
            # 获取下一页按钮的标签，这里用的是class标签，因为它只有一个
            next_page = browser.find_element_by_class_name("next")
            # 点击下一页
            next_page.click()
            # 点击之后，睡眠5s，防止页面没有加载完全，报no such element的错误
            time.sleep(5)
        else:
            break