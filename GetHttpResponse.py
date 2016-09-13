#!/usr/bin/env python
# coding=utf8

import httplib

httpClient = None


def getHttpResponse(host, url, port, method, timeout):
    try:
        httpClient = httplib.HTTPConnection(host=host, port=port, timeout=timeout)
        httpClient.request(method=method, url=url)
        response = httpClient.getresponse()
        # print response.status
        # print response.reason
        # print response.read()
        return response
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
