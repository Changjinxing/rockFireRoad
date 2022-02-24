
#coding=utf-8
import datetime
import json
import sys
import urllib2

import lxml
import requests

from bs4 import BeautifulSoup
from lxml import etree
from lxml import html


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(num)
        return True
    except (TypeError, ValueError):
        pass

    return False


def translate_num(num):
    if num.isdigit():
        return int(num)
    else:
        return float(num)


def get(url, h):
    r = requests.get(url, headers=h)
    if r.status_code == 200:
        return r


def parse_num(r, xpath):
    # print r.content
    root = lxml.html.fromstring(r.content)
    nums = root.xpath(xpath)
    # print type(nums), len(nums)
    real_nums = []
    for num in nums:
        # if num.isdigit():
        if is_number(num):
            real_nums.append(translate_num(num))
    # print len(real_nums), json.dumps(real_nums)
    # exit()
    return real_nums


def get_all_url(url):
    html = urllib2.urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html, features="html.parser")
    # print soup.text
    print soup.find("/html/body/div[4]/h3")
    # tags = soup.find_all("a")
    # for tag in tags:
    #     print tag.get("href")


def download(url):
    html = urllib2.urlopen(url).read().decode("utf-8")
    # html_str = ElementTree.tostring(html).decode()
    # print type(html_str)
    # exit()
    dom = etree.HTML(html)
    print type(etree.tostring(dom))
    print etree.tostring(dom)
    exit()
    return dom


def xpath_parse(dom, xpath, type):
    result = dom.xpath(xpath)[0]
    if type == "title":
        return result
    if type == "num":
        return result
        # return int(result)
    elif type == "line":
        return result
        # return result.split("\：").strip()
    else:
        return result


def crawl_yesterday(url, xpath_dict):
    dom = download(url)
    ans = {}
    for key, conf in xpath_dict.items():
        val = {}
        for k, v in conf.items():
            val[k] = xpath_parse(dom, v.get("xpath"), v.get("type"))
        ans[key] = val
    return ans


baidu = "http://www.baidu.com"
zhujianwei = "http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=307749"
num_xpath = '//td[@align="center"]/text() | //td[@align="middle"]/text()'

yesterday = "http://www.beijingfangshi.com/wx_0.html"
xpath_dict = {
    "stock": {
        "title": {
            "xpath": "/html/body/div[2]/h3",
            "type": "title"
        },
        "dwelling": {
            "xpath": "/html/body/div[3]/font/b",
            "type": "num"
        },
        "online": {
            "xpath": "/html/body/div[3]/font/b",
            "type": "num"
        }
    },
    "new": {
        "title": {
            "xpath": "/html/body/div[4]/h3",
            "type": "title"
        },
        "dwelling": {
            "xpath": "/html/body/div[5]/text()[1]",
            "type": "line"
        },
        "source": {
            "xpath": "/html/body/div[5]/text()[2]",
            "type": "line"
        }
    },
    "salable": {
        "title": {
            "xpath": "/html/body/div[6]/h3",
            "type": "title"
        },
        "dwelling": {
            "xpath": "/html/body/div[7]/text()[1]",
            "type": "line"
        },
        "source": {
            "xpath": "/html/body/div[7]/text()[2]",
            "type": "line"
        }
    },
}

keys = {
    "key0": "可售期房统计",
    "key1": "预售许可",
    "key2": "期房网上认购",
    "key3": "期房网上签约",
    "key4": "未签约现房统计",
    "key5": "现房项目情况",
    "key6": "现房网上认购",
    "key7": "现房网上签约",
    "key8": "存量房网上签约",
    "key9": "存量房网上签约",
}

titles = [
    {
        "key0": [
            "可售房屋套数",
            "可售房屋面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key1": [
            "批准预售许可证",
            "批准预售面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key2": [
            "网上认购套数",
            "网上认购面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key3": [
            "网上签约套数",
            "网上签约面积 (M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key4": [
            "未签约套数",
            "未签约面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key5": [
            "现房项目个数",
            "初始登记面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key6": [
            "网上认购套数",
            "网上认购面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key7": [
            "网上签约套数",
            "网上签约面积(M2)",
            "其中 住宅套数",
            "面积(M2)",
            "商业单元",
            "面积(M2)",
            "办公单元",
            "面积(M2)",
            "车位个数",
            "面积(M2)"
        ]
    },
    {
        "key8": [
            "网上签约套数",
            "网上签约面积(m2)",
            "住宅签约套数",
            "住宅签约面积(m2)"
        ]
    },
    {
        "key9": [
            "网上签约套数",
            "网上签约面积(m2)",
            "住宅签约套数",
            "住宅签约面积(m2)"
        ]
    }
]

xpath_zhujainwei = {
    "all_num": "//div[2]/table[2]/tbody/tr/td/table/tbody/tr/td[2]"
}


def today():
    now = datetime.datetime.now()
    year = now.year
    mon = now.month
    day = now.today().day

    today_str = "%d%02d%02d" % (year, mon, day)
    return today_str

def current_date():
    now = datetime.datetime.now()
    year = now.year
    mon = now.month
    day = now.today().day
    end_day = now.replace(day=1)
    last_mon = end_day - datetime.timedelta(days=1)
    last = last_mon.month

    # print year, mon, day - 1, last
    last_mon_str = "%d年%d月" % (year, last)
    yesterday_str = "%d/%d/%d" % (year, mon, day - 1)
    return last_mon_str, yesterday_str


def translate_keys(keys):
    list_keys = []
    last_mon, yesterday = current_date()
    for k, v in keys.items():
        if k in ["key1", "key8"]:
            keys[k] = "%s %s" % (last_mon, v)
        elif k in ["key2", "key3", "key6", "key7", "key9"]:
            keys[k] = "%s %s" % (yesterday, v)
        list_keys.append(keys.get(k))
    return keys, list_keys


def build_result(nums, keys):
    real_keys, list_keys = translate_keys(keys)
    # print json.dumps(list_keys).decode("unicode-escape").encode("utf-8")
    # exit()
    ans = []
    idx = 0
    for title in titles:
        item = {}
        for k, rows in title.items():
            key = real_keys.get(k)
            val = {}
            for row in rows:
                val[row] = nums[idx]
                idx = idx + 1
            k_1 = key.decode('utf-8').encode(sys.getfilesystemencoding())
            item[k_1] = val
        ans.append(item)
    return ans


if __name__ == '__main__':
    # for title in titles:
    #     for k, vs in title.items():
    #         for v in vs:
    #             print v.decode('utf-8').encode(sys.getfilesystemencoding())
    #             exit()

    # print today()
    # exit()
    # ans = crawl_yesterday(yesterday, xpath_dict)
    # print json.dumps(ans)
    # get_all_url(yesterday)

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    r = get(zhujianwei, headers)
    real_nums = parse_num(r, num_xpath)
    # print json.dumps(real_nums)
    # exit()
    # print json.dumps(real_nums)

    # last_mon, yesterday = current_date()
    # print last_mon, yesterday

    ans = build_result(real_nums, keys)
    # print ans
    # print json.dumps(ans).decode("unicode-escape")

    file_path = "%s.json" % (today())
    with open(file_path, 'w') as f:
        f.write(json.dumps(ans).decode("unicode-escape").encode("utf-8"))
