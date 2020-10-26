from selenium import webdriver
from selenium.webdriver import ActionChains
import time


def login(id, password):
    url = 'https://music.163.com/'
    browser = webdriver.Chrome("chromedriver.exe")
    browser.maximize_window()
    browser.get(url)

    element = browser.find_element_by_xpath('//div[@class="m-tophead f-pr j-tflag"]')
    ActionChains(browser).move_to_element(element).perform()
    # 点击登录
    s1 = '//div[@class="m-tophead f-pr j-tflag"]/a'
    browser.find_element_by_xpath(s1).click()
    # 切换登录
    element = browser.find_element_by_id("otherbtn")
    ActionChains(browser).move_to_element(element).perform()
    browser.find_element_by_xpath("//div[@id='otherbtn']/a").click()
    # 勾选条款
    element = browser.find_element_by_css_selector(".u-official-terms")
    ActionChains(browser).move_to_element(element).perform()
    browser.find_element_by_id("j-official-terms").click()
    # 点击手机号登录
    element = browser.find_element_by_css_selector(".f-mgt10")
    ActionChains(browser).move_to_element(element).perform()
    browser.find_element_by_css_selector(".u-btn2.u-btn2-2").click()
    # 输入账密
    browser.find_element_by_css_selector(".j-phone.txt.u-txt").clear()
    browser.find_element_by_css_selector(".j-phone.txt.u-txt").send_keys(id)
    browser.find_element_by_css_selector(".j-pwd.u-txt").clear()
    browser.find_element_by_css_selector(".j-pwd.u-txt").send_keys(password)
    # 点击登录
    element = browser.find_element_by_css_selector(".f-mgt20")
    ActionChains(browser).move_to_element(element).perform()
    browser.find_element_by_css_selector(".j-primary.u-btn2.u-btn2-2").click()

    time.sleep(10)

    # browser.find_element_by_name('p').clear()
    # browser.find_element_by_name('p').send_keys(id)  # 输入用户账户
    # browser.find_element_by_name('pw').clear()
    # browser.find_element_by_name('pw').send_keys(passwd)  # 输入用户密码
    # browser.find_element_by_xpath('//div/a[@class="j-primary u-btn2 u-btn2-2"]').click()  # 点击登录
    # time.sleep(5)
    # print(browser.find_element_by_class_name('head f-fl f-pr').text)


if __name__ == '__main__':
    login(13437104137, "Cjt4713!")
