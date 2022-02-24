from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
    driver.get(url)
    print(driver.current_url)
    driver.close()


if __name__ == '__main__':
    url ="file:///Users/jinxing.zhang/Documents/git/rockFireRoad/snowSpider/templates/zhujianwei.html"
    main(url)



#  brew install chromedriver