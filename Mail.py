# -*- coding: UTF-8 -*-
'''
通过qq邮箱发送邮件
需要一个安全的连接，例如SSL，因此接下来我们会使用SSL的方式去登录，但是在那之前，我们需要做一些准备，打开qq邮箱，点击设置->
账户，找到POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务，开启IMAP/SMTP服务，然后根据要求使用手机发送到指定号码，获取授权码
'''
import smtplib
from email.mime.text import MIMEText

mailto_list = ["zhangyufeng@my56.com","410487930@qq.com"]
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "410487930"  # 用户名
mail_pass = "rzoamznufnylbgbb"  # 手机接收到的授权码
mail_postfix = "qq.com"  # 发件箱的后缀


def send_mail(to_list, sub, content):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP_SSL(mail_host,465)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
    if send_mail(mailto_list, "database　Exception", "数据库服务器异常"):
        print "发送成功"
    else:
        print "发送失败"