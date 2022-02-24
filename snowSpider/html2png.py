# -*- coding: utf-8 -*-
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import os


url = "file:///Users/jinxing.zhang/Documents/git/rockFireRoad/snowSpider/a.html"
print url
save_fn = "save.png"

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
driver.save_screenshot(save_fn)
driver.quit()


def crop_img(img):
    # for img in os.listdir(img_path):
    if img.lower().endswith('.png'):
        print('%s裁剪中。。'% img)
        # im = Image.open('./screen_shot/%s'% img)
        im = Image.open(img)
        x = 296
        y = 0
        w = 1960
        h = 1570
        region = im.crop((x, y, x+w, y+h))
        region.save("./screenshot_final/%s" % img)


if __name__ == '__main__':
    crop_img(save_fn)