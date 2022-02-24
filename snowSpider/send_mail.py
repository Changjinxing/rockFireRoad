# coding=utf-8

from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import mimetypes

from email.mime.multipart import MIMEMultipart
import os
import smtplib

from email import Encoders as email_encoders


class Message(object):
    def __init__(self, password, from_addr, to_addr, subject="", html="", text=None, cc_addr=[], attachment=[]):
        self.password = password
        self.from_addr = from_addr
        self.subject = subject

        if to_addr:
            if isinstance(to_addr, list):
                self.to_addr = to_addr
            else:
                self.to_addr = [d for d in to_addr.split(',')]
        else:
            self.to_addr = []

        if cc_addr:
            if isinstance(cc_addr, list):
                self.cc_addr = cc_addr
            else:
                self.cc_addr = [d for d in cc_addr.split(',')]
        else:
            self.cc_addr = []

        if html is not None:
            self.body = html
            self.body_type = "html"
        else:
            self.body = text
            self.body_type = "plain"

        self.parts = []
        if isinstance(attachment, list):
            for file in attachment:
                self.add_attachment(file)

    def add_attachment(self, file_path, mimetype=None):
        """
            If *mimetype* is not specified an attempt to guess it is made. If nothing
            is guessed then `application/octet-stream` is used.
        """
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(file_path)

        if mimetype is None:
            mimetype = 'application/octet-stream'

        type_maj, type_min = mimetype.split('/')
        with open(file_path, 'rb') as fh:
            part_data = fh.read()

            part = MIMEBase(type_maj, type_min)
            part.set_payload(part_data)
            email_encoders.encode_base64(part)

            part_filename = os.path.basename(file_path)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % part_filename)
            part.add_header('Content-ID', part_filename)

            self.parts.append(part)

    def __to_mime_message(self):
        """Returns the message as
        :py:class:`email.mime.multipart.MIMEMultipart`."""

        ## To get the message work in iOS, you need use multipart/related, not the multipart/alternative
        msg = MIMEMultipart('related')
        msg['Subject'] = self.subject
        msg['From'] = self.from_addr
        msg['To'] = ','.join(self.to_addr)

        if len(self.cc_addr) > 0:
            msg['CC'] = ','.join(self.cc_addr)

        body = MIMEText(self.body, self.body_type)
        msg.attach(body)

        # Add Attachment
        for part in self.parts:
            msg.attach(part)

        return msg

    def send(self, smtp_server='smtp.163.com'):

        smtp = smtplib.SMTP()
        print "connect beg"
        smtp.connect("smtp.163.com", "25")
        print "connect done"
        state = smtp.login(self.from_addr, self.password)

        if state[0] == 235:
            print "sending...."
            smtp.sendmail(from_addr=self.from_addr, to_addrs=self.to_addr + self.cc_addr,
                          msg=self.__to_mime_message().as_string())
            smtp.close()


import datetime

from_addr = "jinxingbay@163.com"
mail_to = "jinxingbay@163.com"
password = "MZJXWUCIJPBGRQTV"


def send_go():
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    attach_files = ['./screenshot_final/save.png']
    print attach_files
    mail_msg = """
        <p>Hi Lockey:</p>
        <p><img src="cid:test1.jpg"></p>####要特别注意这里，正文插入图片的特殊格式！！！
        <hr/>
        <p style="text-indent:16px">Here is the latest paper link from The Economist, you can click <a href="https://lockeycheng.github.io/iooi/index.html">Go</a> for a full view!</p>
        <hr/>
        <p>Best Regards</p>
        <p>
            Any question please mail to <a href='mailto:iooiooi23@163.com'>Lockey23</a>.
        </p>
        <p>Sent at {} PST</p>
        """.format(time_now)
    subject = '[Halo] - ' + 'A new paper published!'
    msg = Message(
        password=password,
        from_addr=from_addr,
        to_addr=[mail_to],
        cc_addr=[mail_to],
        subject=subject,
        attachment=attach_files,
        html=mail_msg
    )
    msg.send()
    print "success"


if __name__ == '__main__':
    send_go()
