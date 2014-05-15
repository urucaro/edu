#!/usr/bin/python
#-*- coding:  utf8 -*-


import urllib2

page = 'http://www.addic7ed.com/updated/1/39289/0'

referer ='http://www.addic7ed.com/serie/30_Rock/5/13/addic7ed'

#headers = {'User-Agent' : 'Mozilla 5.10', 'Referer' : 'http://www.addic7ed.com/serie/30_Rock/5/13/addic7ed'} 


req = urllib2.Request(page,  headers ={'User-Agent' : 'Mozilla 5.10', 'Referer' : 'http://www.addic7ed.com/serie/30_Rock/5/13/addic7ed'})

print req 
#req.add_header('Referer', referer)
response = urllib2.urlopen(req)

data = response.read()

print response.info()

if response.info().has_key('Content-Disposition'):
    print 'bra'
    
with open('subtitle.srt', 'wb') as subtitle:
    subtitle.write(data)
