__author__ = "JentZhang"

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from utils.BaseFunction import *


class SendEmail(object):
    """
    邮件发送类
    """

    def __init__(self):
        """
        构造函数：初始化基本信息
        :param host:邮件服务器地址
        :param user:邮件用户名
        :param passwd:邮件登录口令
        """
        self.user = ""
        self.passwd = ""
        self.host = ""

        server = smtplib.SMTP_SSL()
        server.connect(self.host, 465)
        server.login(self.user, self.passwd)
        self.server = server

        #

    def sendTxtMail(self, to_list, sub, content, is_html=False):
        """
        发送文件或html邮件
        :param to_list:
        :param sub:
        :param content:
        :param subtype:
        :return:
        """
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        if is_html:
            subtype = "html"
        else:
            subtype = "plain"
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ";".join(to_list)
        try:
            self.server.sendmail(self.user, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    def sendAttachMail(self, to_list, sub, content, attach_path=[], is_html=False):
        """
        发送带附件的文件或html邮件
        :param to_list:收件人列表
        :param sub:主题
        :param content:邮件内容
        :param attach_path:附件路径列表
        :param is_html:是否是html格式
        :return:
        """
        if is_html:
            subtype = "html"
        else:
            subtype = "plain"

        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ";".join(to_list)
        # 邮件正文内容
        msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))

        # 构造附件
        if len(attach_path) > 0:
            for path in attach_path:
                with open(r'' + path, 'rb') as f:
                    attach = MIMEText(f.read(), 'base64', 'utf-8')
                    attach["Content-Type"] = 'application/octet-stream'
                    # 根据路径获取文件名称
                    filepath, shotname, extension = get_filePath_fileName_fileExt(r'' + path)
                    attach["Content-Disposition"] = 'attachment;filename="{0}"'.format(
                        shotname + extension)
                    msg.attach(attach)

        try:
            self.server.sendmail(self.user, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    def sendImageMail(self, to_list, sub, content, pic_path, is_html=False):
        """
        发送到图片附件的邮件
        :param to_list:
        :param sub:
        :param content:
        :param is_html:
        :return:
        """
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        if is_html:
            subtype = "html"
        else:
            subtype = "plain"

        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ";".join(to_list)
        # 邮件正文内容
        msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))

        # 构造附件
        if len(pic_path) > 0:
            for path in pic_path:
                with open(r'' + path, 'rb') as f:
                    image = MIMEImage(f.read())
                    # 根据路径获取文件名称
                    filepath, shotname, extension = get_filePath_fileName_fileExt(r'' + path)
                    image.add_header('Content-Disposition',
                                     'attachment;filename="{0}"'.format(shotname + extension))
                    msg.attach(image)

        try:
            self.server.sendmail(self.user, to_list, msg.as_string())
            return True
        except Exception as  e:
            print(str(e))
            return False

    def __del__(self):
        """
        析构函数：释放资源
        :return:
        """
        self.server.quit()
        self.server.close()


if __name__ == '__main__':
    # FromAddr = "postmaster@zhangtao1994.com"
    # Password = "tao15955146767!"

    mailto_list = ['1002723914@qq.com', 'tao_zhang@mail.m818.com']
    mail = SendEmail()

    if mail.sendTxtMail(mailto_list, "下午好a", "<p>hello world！</p><br><br><h1>HelloWorld</h1>", is_html=True):
        print("发送成功")
    else:
        print("发送失败")


        # if mail.sendAttachMail(mailto_list, sub="带附件邮件-带两个附件20190111", content="hello world！<br><br><h1>你好，发送文本文件测试<h1>",
        #                        attach_path=['test.txt',],
        #                        is_html=True):
        #     print("发送成功")
        #
        # else:
        #     print("发送失败")

        # if mail.sendImageMail(mailto_list, "测试邮件-带一个图片的附件201901", "hello world！<br><br><h1>你好，发送文本文件测试<h1>",
        #                       pic_path=['timg.jpg','0003.jpg'], is_html=True):
        #     print("发送成功")
        #
        # else:
        #     print("发送失败")
