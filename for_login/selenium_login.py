# coding:utf-8
# !/usr/local/bin python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys


def log_in(usrname, passwd):
    # 模拟登陆163邮箱
    driver = webdriver.Firefox()
    driver.get("http://1.1.1.2/ac_portal/default/pc.html?tabs=pwd")

    # 用户名 密码
    elem_user = driver.find_element_by_name("une")
    elem_user.send_keys(usrname)
    elem_pwd = driver.find_element_by_name("pass")
    elem_pwd.send_keys(passwd)
    elem_pwd.send_keys(Keys.RETURN)
    time.sleep(5)
    # assert "baidu" in driver.title
    # driver.close()
    driver.quit()


def check_time(login_time="15:49"):
    date = time.ctime()
    if login_time in date.split(" ")[3]:
        print login_time
        print date
        return True
    return False
    print date


if __name__ == '__main__':
    info = sys.argv
    print info
    if len(info) > 1:
        username = info[1]
        passwd = info[2]
    else:
        username = "maxinghua"
        passwd = "abcd1234"

    #59秒检测一次时间
    # log_in(username, passwd)
    # exit()
    while True:
        if check_time():
            log_in(username, passwd)
        time.sleep(59)

