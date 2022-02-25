# -*- coding: utf-8 -*-
import time
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from PIL import Image
import os
import example

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download_and_save(url, save_fn):

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument("--window-size=1280,1024")
    option.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(chrome_options=option)

    driver.get(url)
    print(driver.title)

    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(scroll_width, scroll_height)
    # driver.implicitly_wait(10000)

    # 显式等待
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "123"))
        )
    except TimeoutException:
        pass
    finally:
        print("退出浏览器")
        driver.save_screenshot(save_fn)
        driver.quit()
    # driver.quit()


def crop_img(img, corp_img, crop=False, x=0, y=0, w=0, h=0):
    # for img in os.listdir(img_path):
    if img.lower().endswith('.png'):
        # im = Image.open('./screen_shot/%s'% img)
        im = Image.open(img)
        print('%s裁剪中。。'% img)
        if not crop:
            x, y, w, h = 0, 0, im.width, im.height
            # x = 296
            # y = 0
            # w = 1960
            # h = 1570
        region = im.crop((x, y, x+w, y+h))
        region.save(corp_img)


if __name__ == '__main__':
    url = "file:///Users/jinxing.zhang/Documents/git/rockFireRoad/snowSpider/a.html"
    save_fn = "save.png"

    url = "http://www.beijingfangshi.com/wx_w1.html"
    save_fn = "./screenshot/%s_fangshi.png" % example.today()
    corp_save_fn = "./screenshot_final/%s_fangshi.png" % example.today()

    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/xhtml+html",
        "Host": "www.beijingfangshi.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "user-agent": "PostmanRuntime/7.29.0",
        # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    r = example.get(url, headers)
    # print r.text.encode('utf8','ignore')
    html_save_fp = "./static/%s_fangshi.html" % example.today()
    example.save_file(html_save_fp, r.text.encode('utf8','ignore'))

    local_html_url = "file:///Users/jinxing.zhang/Documents/git/rockFireRoad/snowSpider/static/%s_fangshi.html" % example.today()

    print url, local_html_url, save_fn, html_save_fp
    download_and_save(local_html_url, save_fn)
    crop_img(save_fn, corp_save_fn, True, 0, 0, 2680, 1400)