#!/usr/bin/python
#-*- coding:  utf8 -*-

import urllib

url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'

print 'laddar ner med urllib'

urllib.urlretrieve (url, 'testfile.zip')
