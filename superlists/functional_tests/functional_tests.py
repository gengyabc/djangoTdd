from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.fixture()
def browser():
    # 小明想用 chrome 浏览器访问网站
    browser = webdriver.Chrome('/Users/sziit/Programming/chromedriver')
    # 不过小明在每个页面最多等 10s, 如果还是没找到想要的东西, 就不找了
    browser.implicitly_wait(10)

    yield browser

    # 很好, 现在可以睡觉了
    browser.quit()

def assert_inputbox_placeholder_is(text, browser):
    inputbox = browser.find_element_by_id('new_item')
    assert text == inputbox.get_attribute('placeholder')

def input_box_send_key(k, browser):
    inputbox = browser.find_element_by_id('new_item')
    inputbox.send_keys(k)

def assert_table_row_text_include(text, browser):
    table = browser.find_element_by_id('lists_table')
    rows = table.find_elements_by_tag_name('tr')
    assert any(text in row.text for row in rows) is True, [row.text for row in rows]

def test_homepage_add_new_item_for_one_user(browser, live_server):

    # 他打开网站的主页
    browser.get(live_server.url)

    # 他发现页面标题有 今日清单 字样
    assert '今日清单' in browser.title
    assert '今日清单' in browser.find_element_by_tag_name('h1').text

    # 他开始使用这个应用了

    # 他发现输入框显示: 想干点啥?
    assert_inputbox_placeholder_is('想干点啥呢', browser)

    # 他在文本框输入: 今天什么都不想干
    input_box_send_key('今天什么都不想干', browser)

    # 他点击 回车, 页面更新, 页面列表出现: 今天什么都不想干
    input_box_send_key(Keys.ENTER, browser)

    assert_table_row_text_include('今天什么都不想干', browser)

    assert_inputbox_placeholder_is('想干点啥呢', browser)
    input_box_send_key('今天要吃饭睡觉', browser)

    # 他点击 回车, 页面更新, 页面列表新增: 今天要吃饭睡觉
    input_box_send_key(Keys.ENTER, browser)

    assert_table_row_text_include('今天什么都不想干', browser)
    assert_table_row_text_include('今天要吃饭睡觉', browser)
 
    # 他关闭页面, 再次打开, 自己的清单项目都还在

def test_homepage_add_item_for_multi_users(browser, live_server):

    ## 第一个人登录网站
    browser.get(live_server.url)
    text = '我也不打算的公司规定'
    input_box_send_key(text, browser)
    input_box_send_key(Keys.ENTER, browser)
    assert_table_row_text_include(f'1: {text}', browser)

    url = browser.current_url
    assert 'lists' in url, 'url 里面没有 lists'

    ## 第二个用户来了
    browser.get(live_server.url)
    assert text not in browser.find_element_by_tag_name('body').text

    new_text = 'sgssdgegwweg'
    input_box_send_key(new_text, browser)
    input_box_send_key(Keys.ENTER, browser)
    assert text not in browser.find_element_by_tag_name('body').text
    assert_table_row_text_include(f'1: {new_text}', browser)

    new_url = browser.current_url
    assert 'lists' in new_url
    assert url != new_url
