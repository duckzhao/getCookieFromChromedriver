import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import time

def open_chrome():
    with open('./config.txt', mode='r', encoding='utf-8')as f:
        path = f.read() + '\chrome.exe'
    # print(path)
    os.system('"{}" --remote-debugging-port=9222'.format(path))

t = threading.Thread(target=open_chrome, name='t')


def process_cookie(driver):
    print('正在提取', driver.title, '页面的cookie')
    c = driver.get_cookies()
    # print(c)
    cookies = {}
    # 获取cookie中的name和value,转化成requests可以使用的形式
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    # driver.close()
    return cookies, driver.title


def write_cookie(cookie_dict, index):
    cookie_str = ''
    for key in cookie_dict.keys():
        value = cookie_dict[key]
        cookie_str += key + '=' + value + '; '
    cookie_str = cookie_str[:-2]
    with open('./{}-cookie.txt'.format(index), mode='w', encoding='utf-8')as f:
        f.write(cookie_str)

# 开启一个死循环，一直读取浏览器中的cookie
def run(driver):
    input('请跳转至需要获取cookie的页面进行登录等预操作，操作好后输入任意字符开始提取cookie：')
    for i in range(1, 100):
        cookie_dict, name = process_cookie(driver)
        # stop_thread(t)
        write_cookie(cookie_dict, i)
        k = input('如要继续提取其他网页cookie，请在浏览器中完成操作后输入任意字符提取；如要退出程序，请输入2：')
        if k == '2':
            print('程序即将退出！')
            time.sleep(2)
            driver.close()
            break

if __name__ == '__main__':
    t.start()
    time.sleep(2)
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    run(driver)