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

def test_homepage_title_should_have_今日清单(browser):
    def assert_inputbox_placeholder_is(text):
        inputbox = browser.find_element_by_id('new_item')
        assert text == inputbox.get_attribute('placeholder')

    def input_box_send_key(k):
        inputbox = browser.find_element_by_id('new_item')
        inputbox.send_keys(k)

    def assert_table_row_text_include(text):
        table = browser.find_element_by_id('lists_table')
        rows = table.find_elements_by_tag_name('tr')
        assert any(text in row.text for row in rows) is True

    # 他打开网站的主页
    browser.get('http://localhost:8000')

    # 他发现页面标题有 今日清单 字样
    assert '今日清单' in browser.title
    assert '今日清单' in browser.find_element_by_tag_name('h1').text

    # 他开始使用这个应用了

    # 他发现输入框显示: 想干点啥?
    assert_inputbox_placeholder_is('想干点啥呢')

    # 他在文本框输入: 今天什么都不想干
    input_box_send_key('今天什么都不想干')

    # 他点击 回车, 页面更新, 页面列表出现: 今天什么都不想干
    input_box_send_key(Keys.ENTER)

    assert_table_row_text_include('今天什么都不想干')

    assert_inputbox_placeholder_is('想干点啥呢')
    input_box_send_key('今天要吃饭睡觉')

    # 他点击 回车, 页面更新, 页面列表新增: 今天要吃饭睡觉
    input_box_send_key(Keys.ENTER)

    assert_table_row_text_include('今天什么都不想干')
    assert_table_row_text_include('今天要吃饭睡觉')
 
    # 他关闭页面, 再次打开, 自己的清单项目都还在