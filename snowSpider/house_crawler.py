# -*- coding: utf-8 -*-

import datetime
import json
import smtplib
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import lxml
import requests
from PIL import Image
from lxml import html
from selenium import webdriver

import html2png

local_path_prefix = "/Users/jinxing.zhang/Documents/git"
# local_path_prefix = "/root/code"

zhujianwei = "http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=307749"
num_xpath = '//td[@align="center"]/text() | //td[@align="middle"]/text()'
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


def download(url, h):
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


def get_today_info():
    now = datetime.datetime.now()
    year = now.year
    mon = now.month
    day = now.today().day
    return now, year, mon, day


def today_str():
    now, year, mon, day = get_today_info()
    return "%d%02d%02d" % (year, mon, day)


def today_info():
    now, year, mon, day = get_today_info()
    return year, mon, day, "%d%02d%02d" % (year, mon, day)


def current_date():
    now, year, mon, day = get_today_info()
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
    for i in range(0, 10):
        k = "key%d" % i
        v = keys.get(k)
        if k in ["key1", "key8"]:
            keys[k] = "%s %s" % (last_mon, v)
        elif k in ["key2", "key3", "key6", "key7", "key9"]:
            keys[k] = "%s %s" % (yesterday, v)
        list_keys.append(keys.get(k))
    # print json.dumps(list_keys)
    # exit()
    return keys, list_keys


def build_result(nums, keys):
    real_keys, list_keys = translate_keys(keys)
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
    return ans, list_keys


def crawl_and_save():
    # crawl 住建委
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    r = download(zhujianwei, headers)
    # print r
    real_nums = parse_num(r, num_xpath)
    ans, real_keys = build_result(real_nums, keys)
    # save data local json file
    # todo: mysql saving
    file_path = "./data/%s.json" % (today_str())
    with open(file_path, 'w') as f:
        f.write(json.dumps(ans).decode("unicode-escape").encode("utf-8"))
    return real_nums, real_keys


def read_file(path):
    f = open(path)
    return f.read()


def read_file_codecs(path):
    import codecs
    f = codecs.open(path, 'r+')
    return f.read()

html_file_path = "zhujianwei.html"
format_html_str = read_file(html_file_path)


# render html and save
def format_and_save_html(nums, keys):
    file_path = "static/%s.html" % (today_str())
    with open(file_path, 'w') as f:
        f.write(format_html_str.format(nums, keys))
    return "file://%s/rockFireRoad/snowSpider/static/%s.html" % (local_path_prefix, today_str()), file_path


def crop_img(img):
    # for img in os.listdir(img_path):
    if img.lower().endswith('.png'):
        print('%s裁剪中。。' % img)
        # im = Image.open('./screen_shot/%s'% img)
        im = Image.open(img)
        x = 296
        y = 0
        w = 1960
        h = 1570
        region = im.crop((x, y, x + w, y + h))
        final_path = "./screenshot_final/%s.png" % (today_str())
        region.save(final_path)
        return final_path


# html to png, then save and crop
def save_and_crop_png(url):
    save_fn = "screenshot/%s.png" % (today_str())

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument("--window-size=1280,1024")
    option.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
    # driver = webdriver.Chrome(chrome_options=option)

    driver.get(url)
    print(driver.title)

    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(scroll_width, scroll_height)
    driver.save_screenshot(save_fn)
    driver.quit()

    return crop_img(save_fn)


email_host = 'smtp.163.com'  # 服务器地址 163邮箱"smtp.163.com"  qq邮箱"smtp.qq.com"都需要开通smtp权限
sender = 'jinxingbay@163.com'  # 发件人（自己的邮箱）
password = 'MZJXWUCIJPBGRQTV'  # 密码（自己邮箱的登录密码）


def send_mail(subject, img_path, receiver):
    msg = MIMEMultipart()
    msg['Subject'] = subject  # 标题
    msg['From'] = sender  # 邮件中显示的发件人别称
    msg['To'] = receiver  # ...收件人...

    # 指定图片为当前目录
    fp = open(img_path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    # 附件-图片
    image = MIMEImage(open(img_path, 'rb').read(), _subtype=subtype)
    image.add_header('Content-Disposition', 'attachment', filename='img.jpg')
    msg.attach(image)
    print "beg..."
    # 发送
    smtp = smtplib.SMTP()
    smtp.connect(email_host, 25)
    print "connect done"
    smtp.login(sender, password)
    print "login done, sending..."
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('success')


# send png
def send_png(png_path, receiver):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    subject = "房屋交易 - %s" % today_str()
    send_mail(subject, png_path, receiver)


def send_mail(multi, subject, img_paths, receiver):
    msg = MIMEMultipart()
    msg['Subject'] = subject  # 标题
    msg['From'] = sender  # 邮件中显示的发件人别称
    msg['To'] = receiver  # ...收件人...

    for img_path in img_paths:
        img_name = img_path.split("/")[-1]
        # print img_path, img_name
        # exit()
        # 指定图片为当前目录
        # fp = open(img_path, 'rb')
        # msgImage = MIMEImage(fp.read())
        # fp.close()
        # # 定义图片 ID，在 HTML 文本中引用
        # msgImage.add_header('Content-ID', '<image1>')
        # msg.attach(msgImage)

        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        # 附件-图片
        image = MIMEImage(open(img_path, 'rb').read(), _subtype=subtype)
        image.add_header('Content-Disposition', 'attachment', filename=img_name)
        msg.attach(image)
    print "beg..."
    # 发送
    smtp = smtplib.SMTP()
    smtp.connect(email_host, 25)
    print "connect done"
    smtp.login(sender, password)
    print "login done, sending..."
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('success')


# send png
def send_pngs(png_paths, receiver):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    subject = "房屋交易 - %s" % today_str()
    send_mail(True, subject, png_paths, receiver)


def save_file(save_fp, data):
    with open(save_fp, 'w') as f:
        f.write(data)


def get_wangqian_qushi_and_send():
    url = "http://www.beijingfangshi.com/wx_w1.html"
    save_fn = "./screenshot/%s_fangshi.png" % today_str()
    corp_save_fn = "./screenshot_final/%s_fangshi.png" % today_str()

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
    r = download(url, headers)
    # print r.text.encode('utf8','ignore')
    html_save_fp = "./static/%s_fangshi.html" % today_str()
    save_file(html_save_fp, r.text.encode('utf8', 'ignore'))

    local_html_url = "file://%s/rockFireRoad/snowSpider/static/%s_fangshi.html" % (local_path_prefix, today_str())

    print url, local_html_url, save_fn, html_save_fp
    html2png.download_and_save(local_html_url, save_fn)
    html2png.crop_img(save_fn, corp_save_fn, True, 0, 0, 2680, 1400)

    return corp_save_fn, html_save_fp


def send_html(subject, html_paths, receiver):
    msg = MIMEMultipart()
    msg['Subject'] = subject  # 标题
    msg['From'] = sender  # 邮件中显示的发件人别称
    msg['To'] = receiver  # ...收件人...

    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    for html_path in html_paths:
        name = html_path.split("/")[-1]
        # 附件-文件
        file = MIMEBase(maintype, subtype)
        file.set_payload(open(html_path, 'rb').read())
        file.add_header('Content-Disposition', 'attachment', filename=name)
        encoders.encode_base64(file)
        msg.attach(file)

    print "beg..."
    # 发送
    smtp = smtplib.SMTP()
    smtp.connect(email_host, 25)
    print "connect done"
    smtp.login(sender, password)
    print "login done, sending..."
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('success')


# send png
def send_htmls(html_paths, receiver):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    subject = "房屋交易 - html - %s" % today_str()
    send_html(subject, html_paths, receiver)


request_sample = {
    "source": "zjw",
    "year": 2022,
    "mon": 3,
    "day": 8,
    "month": {
        "online": 9158,
        "onlineArea": 788782.44,
        "signArea": 739063.69,
        "sign": 8260
    },
    "daily": {
        "online": 692,
        "onlineArea": 60159.68,
        "signArea": 54855.99,
        "sign": 616
    },
    "yearCanSell": {
        "car": 1,
        "business": 2,
        "office": 3,
        "area": 1.2,
        "house": 1,
        "num": 2,
        "nArea": 3.2
    },
    "monthMaySellCert": {
        "car": 1,
        "business": 2,
        "office": 3,
        "area": 1.2,
        "house": 1,
        "num": 2,
        "nArea": 3.2
    },
    "realEstateProject": {
        "car": 1,
        "business": 2,
        "office": 3,
        "area": 1.2,
        "house": 1,
        "num": 2,
        "nArea": 3.2
    },
    "future": {
        "sign": {
            "car": 1,
            "business": 2,
            "office": 3,
            "area": 1.2,
            "house": 1,
            "num": 2,
            "nArea": 3.2
        },
        "buy": {
            "car": 1,
            "business": 2,
            "office": 3,
            "area": 1.2,
            "house": 1,
            "num": 2,
            "nArea": 3.2
        }
    },
    "secondHand": {
        "sign": {
            "car": 1,
            "business": 2,
            "office": 3,
            "area": 1.2,
            "house": 1,
            "num": 2,
            "nArea": 3.2
        },
        "noSign": {
            "car": 1,
            "business": 2,
            "office": 3,
            "area": 1.2,
            "house": 1,
            "num": 2,
            "nArea": 3.2
        },
        "buy": {
            "car": 1,
            "business": 2,
            "office": 3,
            "area": 1.2,
            "house": 1,
            "num": 2,
            "nArea": 3.2
        }
    }
}


def key_encode(key):
    return key
    # return key.decode('utf-8').encode('unicode-escape').replace("\\\\", "\\").decode("utf-8")


def translate(type, data):
    # print data
    if type == 'saving':
        return {
            "online": data[key_encode(u'住宅签约套数')],
            "onlineArea": data[key_encode(u'住宅签约面积(m2)')],
            "signArea": data[key_encode(u'网上签约面积(m2)')],
            "sign": data[key_encode(u'网上签约套数')]
        }
    if type in ['second_sign']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'网上签约套数')],
            "nArea": data[key_encode(u'网上签约面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['second_buy']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'网上认购套数')],
            "nArea": data[key_encode(u'网上认购面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['second_no_sign']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'未签约套数')],
            "nArea": data[key_encode(u'未签约面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['future_sign']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'网上签约套数')],
            "nArea": data[key_encode(u'网上签约面积 (M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['future_buy']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'网上认购套数')],
            "nArea": data[key_encode(u'网上认购面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['year_can_sell']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'可售房屋套数')],
            "nArea": data[key_encode(u'可售房屋面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['month_may_sell_cert']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'批准预售许可证')],
            "nArea": data[key_encode(u'批准预售面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }
    if type in ['real_estate_project']:
        return {
            "car": data[key_encode(u'车位个数')],
            "business": data[key_encode(u'商业单元')],
            "office": data[key_encode(u'办公单元')],
            "area": data[key_encode(u'面积(M2)')],
            "num": data[key_encode(u'现房项目个数')],
            "nArea": data[key_encode(u'初始登记面积(M2)')],
            "house": data[key_encode(u'其中 住宅套数')]
        }


# parse data to request
def parse_data_2_request(daily_data_file_path, year, mon, day):
    ans = request_sample
    context = json.loads(read_file(daily_data_file_path))
    # print key_encode('住宅签约套数')
    # print context[8]
    # print json.dumps(context)
    # exit()
    ans['year'] = year
    ans['mon'] = mon
    ans['day'] = day

    ori_month = context[8].values()[0]
    ori_daily = context[9].values()[0]
    ans['daily'] = translate('saving', ori_daily)
    ans['month'] = translate('saving', ori_month)


    ori_second_sign = context[7].values()[0]
    ori_second_nosign = context[4].values()[0]
    ori_second_buy = context[6].values()[0]

    secondHand = {
        'sign': translate('second_sign', ori_second_sign),
        'noSign': translate('second_no_sign', ori_second_nosign),
        'buy': translate('second_buy', ori_second_buy)
    }
    ans['secondHand'] = secondHand

    ori_future_sign = context[3].values()[0]
    ori_future_buy = context[2].values()[0]
    future = {
        'sign': translate('future_sign', ori_future_sign),
        'buy': translate('future_buy', ori_future_buy)
    }
    ans['future'] = future

    ori_year_can_sell = context[0].values()[0]
    year_can_sell = translate("year_can_sell", ori_year_can_sell)
    ans['yearCanSell'] = year_can_sell

    ori_month_may_sell_cert = context[1].values()[0]
    month_may_sell_cert = translate('month_may_sell_cert', ori_month_may_sell_cert)
    ans['monthMaySellCert'] = month_may_sell_cert

    ori_real_estate_project = context[5].values()[0]
    real_estate_project = translate('real_estate_project', ori_real_estate_project)
    ans['realEstateProject'] = real_estate_project

    return ans


def usage_for_parse_data_to_request():

    year, mon, day, day_str = today_info()

    # daily_data_path = "./data/%s.json" % (day_str)
    daily_data_path = "./data/%s.json" % ('20220316')
    request_body = parse_data_2_request(daily_data_path, year, mon, day)
    print json.dumps(request_body)

    requests = []
    mon = 3
    for day in range(1, 32):
        daily_data_path = "./data/%d%02d%02d.json" % (year, mon, day)
        # print daily_data_path
        # exit()
        request = parse_data_2_request(daily_data_path, year, mon, day)
        requests.append(request)
    return requests


if __name__ == '__main__':
    # usage_for_parse_data_to_request()
    # exit()

    nums, keys = crawl_and_save()
    html_path, zjw_html = format_and_save_html(nums, keys)
    png_file_path = save_and_crop_png(html_path)

    receiver = 'jinxingbay@163.com'  # 收件人
    # receiver = 'jinxing.zhang@hulu.com'  # 收件人
    # send_png(png_file_path, receiver)

    # 房市儿
    fangshi_png, fs_html = get_wangqian_qushi_and_send()
    # send_png(fangshi_png, receiver)

    png_paths = [
        png_file_path,
        fangshi_png
    ]

    send_pngs(png_paths, receiver)

    html_paths = [
        zjw_html,
        fs_html
    ]
    send_htmls(html_paths, receiver)
