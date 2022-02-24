# coding=utf-8

import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_host = 'smtp.163.com'  # 服务器地址 163邮箱"smtp.163.com"  qq邮箱"smtp.qq.com"都需要开通smtp权限
sender = 'jinxingbay@163.com'  # 发件人（自己的邮箱）
password = 'MZJXWUCIJPBGRQTV'  # 密码（自己邮箱的登录密码）
receiver = 'jinxingbay@163.com'  # 收件人


# from_addr = "jinxingbay@163.com"
# mail_to = "jinxingbay@163.com"
# password = "MZJXWUCIJPBGRQTV"


def send_mail(subject, img_path):
    msg = MIMEMultipart()
    msg['Subject'] = subject  # 标题
    msg['From'] = sender  # 邮件中显示的发件人别称
    msg['To'] = receiver  # ...收件人...

    signature = '''
        \n\t this is auto test report!
        \n\t you don't need to follow
    '''
    # text = MIMEText(signature, 'plain')  # 签名
    # msg.attach(text)

    # # 正文-图片 只能通过html格式来放图片，所以要注释25，26行
    # mail_msg = '''
    #     <p>\n\t this is auto test report!</p>
    #     <p>\n\t you don't need to follow</p>
    #     <p><a href="http://blog.csdn.net/wjoxoxoxxx">我的博客：</a></p>
    #     <p>截图如下：</p>
    #     <p><img src="cid:image1"></p>
    # '''
    # msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))
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
    # # 附件-文件
    # file = MIMEBase(maintype, subtype)
    # file.set_payload(open(r'320k.txt', 'rb').read())
    # file.add_header('Content-Disposition', 'attachment', filename='test.txt')
    # encoders.encode_base64(file)
    # msg.attach(file)

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


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    subject = now + 'test email'
    img_path = "./screenshot_final/save.png"
    send_mail(subject, img_path)
