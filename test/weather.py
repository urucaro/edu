#!/usr/bin/python
#-*- coding:  utf8 -*-

import httplib
import urlparse




connection = httplib.HTTPConnection("www.piratebay.org")

connection.request("GET", "/")

resp = connection.getresponse()

headers = resp.getheaders()

print resp.status

if (resp.status == 302):
    loc = resp.getheader('location')    
    u = urlparse.urlparse(loc)
    print loc
    address = u.netloc
    print address
    connection = httplib.HTTPConnection(address)
    connection.request("GET", "/")
    resp = connection.getresponse()




