#!/usr/bin/env python
# coding=utf8

import httplib, urllib


httpClient = None

def message_send(messageParam):
    try:
        params = urllib.urlencode({'json': messageParam})
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

        httpClient = httplib.HTTPConnection("www.dttpay.com", 8085, timeout=30)
        httpClient.request("POST", "/commanager/req/request.action", params, headers)

        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
        print response.getheaders()  # 获取头信息
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()