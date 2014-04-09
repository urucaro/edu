#!/usr/bin/python
#-*- coding:  utf8 -*-

import urllib2
#import urllib
from bs4 import BeautifulSoup

domain =("http://www.addic7ed.com")
page_shows=("http://www.addic7ed.com/shows.php")

response = urllib2.urlopen(domain)#Opens the url
response_shows = urllib2.urlopen(page_shows)#Opens the url

html = response.read()#loads the html code
html_shows = response_shows.read()#loads the html code

soup = BeautifulSoup(html)#interprets (parse?) the html code with beautifulsoup
soup_shows = BeautifulSoup(html_shows)#interprets (parse?) the html code with beautifulsoup


#print soup.b
#print soup.head.title

#print soup.find_all('select')

select = soup.find(id = "qsShow") #Finds the entire tag named select with the id value "qsShow"
options = soup.find(id="qsShow").find_all('option') #Finds all the tags named option within the tag named select and the id value "qsShow"
#The "select" keeps the html structure whilst "testar" is more of a list with all the tags named option as elements in it

#print select
#print options

values = list(select.stripped_strings)#Picks out the strings in "select" 

#print values

testar = soup_shows.find("table",  class_ ="tabel90")
values_testar = list(testar.stripped_strings)#Picks out the strings in "testar" 
testarigen = soup_shows.find_all("td", class_="newsDate")


#print values_testar
#print testar
print testarigen







#f = { 'eventName' : 'myEvent', 'eventDescription' : "cool event"}
#url = urllib.urlencode(f)
#print url

#def innerHTML(element):
#    return element.decode_contents(formatter="html")


    


