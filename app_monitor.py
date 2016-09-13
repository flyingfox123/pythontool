# coding=utf-8
import threading
import time
import json
from Log import logger
import GetMySqlConnection
import Mail
import GetHttpResponse
import Message

# 邮件发送名单
mailto_list = ["zhangyufeng@my56.com", "410487930@qq.com"]

# 短信通知名单
sentNumber = "18653125450"

# 数据库配置及执行的sql文件
dbHost = "10.186.116.213"
dbUser = "root"
dbPassWd = "root"
dbDataBase = "manyidb"
dbExecuteSql = "select * from t_param"

# webapp应用访问的配置
appHost = "app.my56app.com"
appUrl = "/baseWeb/index.html"
appMethod = "GET"
appPort = 80
appTimeout = 30

"""
声明对象，将对象转为json
"""


class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


"""
监控mysql、webapp类
"""


class Monitor:
    MYSQL_TRY_NUM = 0
    WEBAPP_TRY_NUM = 0

    def mysql_monitor(self):
        try:
            conn = GetMySqlConnection.getMySqlConn(dbHost, dbUser, dbPassWd, dbDataBase)
            cur = conn.cursor()

            # 获得表中有多少条数据
            aa = cur.execute(dbExecuteSql)

            # 打印表中的数据
            info = cur.fetchmany(aa)
            print conn
            # if (len(info) > 0):
            #     print "aa"
            conn.close
        except Exception, e:
            print self.MYSQL_TRY_NUM
            if self.MYSQL_TRY_NUM >= 3:
                self.MYSQL_TRY_NUM = 0
                Mail.send_mail(mailto_list, "MySql Exception", "MySql异常，请处理")
                messageParam = self.getMySqlExceptionParam()
                Message.message_send(messageParam)
            else:
                self.MYSQL_TRY_NUM += 1
            print e
        finally:
            if conn != None:
                conn.close()

    def webApp_monitor(self):

        response = GetHttpResponse.getHttpResponse(appHost, appUrl, appPort, appMethod, appTimeout)
        print response
        if response == None or response.status != 200:
            print self.WEBAPP_TRY_NUM
            if self.WEBAPP_TRY_NUM >= 3:
                self.WEBAPP_TRY_NUM = 0
                Mail.send_mail(mailto_list, "webapp Exception", "应用服务器发生异常，无法访问")
                messageParam = self.getAppExceptionParam()
                Message.message_send(messageParam)
                logger.info(response)
            else:
                self.WEBAPP_TRY_NUM += 1

    def getAppExceptionParam(self):
        me = Object()
        me.reqHeader = Object()
        me.reqHeader.reqCode = "10000011"
        me.reqHeader.transactionId = "248a2042-4fa5-476f-a7c8-aa0a05a135d4"
        me.reqHeader.tokenId = "20150114151849xRvZQKK0O1"
        me.reqHeader.reqTime = "20160830141613"

        me.data = Object()
        me.data.mobile = sentNumber
        me.data.content = "应用服务器发生异常，无法访问"
        me.data.sign = "【满易行】"
        me.data.channelID = "0"
        return me.to_JSON()

    def getMySqlExceptionParam(self):
        me = Object()
        me.reqHeader = Object()
        me.reqHeader.reqCode = "10000011"
        me.reqHeader.transactionId = "248a2042-4fa5-476f-a7c8-aa0a05a135d4"
        me.reqHeader.tokenId = "20150114151849xRvZQKK0O1"
        me.reqHeader.reqTime = "20160830141613"

        me.data = Object()
        me.data.mobile = sentNumber
        me.data.content = "MySql数据库访问故障"
        me.data.sign = "【满易行】"
        me.data.channelID = "0"
        return me.to_JSON()

    def task(self):
        while True:
            logger.info("monitor running")
            self.webApp_monitor()
            self.mysql_monitor()
            time.sleep(2 * 60)

    def run_monitor(self):
        monitor = threading.Thread(target=self.task)
        monitor.start()


if __name__ == "__main__":
    monitor = Monitor()
    monitor.run_monitor()
