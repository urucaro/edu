#!/usr/bin/python
#-*- coding:  utf8 -*-

import urllib2
import urllib
from bs4 import BeautifulSoup
#import itertools
from pprint import *
import os   



domain ="http://www.addic7ed.com"
serie_url_format = '%s/ajax_getSeasons.php?showID=%s' 
season_url_format = '%s/ajax_getEpisodes.php?showID=%s&season=%s'
episode_url_format = '%s/serie/%s/%s/%s/%s'

# Following function opens the original domain and fetches the list of shows
def series ():
    response = urllib2.urlopen(domain)#Opens the url
    html = response.read ()#loads the html code
    soup = BeautifulSoup (html)#interprets (parse?) the html code 
    select = soup.find(id = "qsShow") #Finds the entire tag named select with the id'
    options = select.find_all ("option")
#    vs = []
#    for option in options:
#        vs.append (option ['value'])
#        print option
    values = [(o ['value'], list (o.stripped_strings) [0] ) for o in options][1:] #the first is just...
   # ...the default "select a show" and therefor omitted
#    result = list (select.stripped_strings)#Picks out the strings in "select"
#    options = soup.find(id="qsShow").find_all('option') #Finds all the tags
    return values # returns a list with the series showID and title

def seasons (s):
    id = s [0]
    serie_url = serie_url_format % (domain, id)
    resp = urllib2.urlopen (serie_url)
    html = resp.read ()#loads the html code
    soup = BeautifulSoup (html)#interprets (parse?) the html code
    select = soup.find(id = "qsiSeason") #Finds the entire tag named select with the id'
    seasons_ids = list (select.stripped_strings) [1:]#Picks out the strings in "select"
    return seasons_ids
    
def episodes (sid,  sea):
    url = season_url_format % (domain, sid,  sea)
    resp = urllib2.urlopen (url)
    html = resp.read (resp)
    soup = BeautifulSoup (html,  from_encoding = 'utf-8')
    select = soup.find (id = 'qsiEp')
    ep_id = list (select.stripped_strings)[1:]
    return ep_id
    
def transform (serie_name,  episode_list, season_nr):
    new_episode_list = {}
    serie_name = serie_name.encode('utf-8').replace(' ', '_')
    for episode in episode_list:
        episode_nr = episode.split('.', 1) [0]
        episode_name = episode.split('.', 1) [1].strip().encode('utf-8').replace (' ', '_')
        
        url_epname = urllib.quote (episode_name)
        url_seriename = urllib.quote (serie_name)
        
        url = episode_url_format % (domain, url_seriename, season_nr, episode_nr, url_epname)
        new_episode_list [episode_nr] = {'title': episode_name, 'url': url}
    return new_episode_list
    
    
    
    
    
    
all_series = series ()
db = {}
count = 0
for serie in all_series:
    count += 1
    print "serie: %d" % count
    db [serie [0]] = {'title': serie [1], 'seasons': {}}
    all_serie_seasons = seasons (serie)
    for season in all_serie_seasons:
        all_season_episodes = episodes (serie [0],  season)
        db [serie[0]]['seasons'] [season] = all_season_episodes



path = ('/home/carolina/proj/edu/data/addic7ed')
for key, value in db.iteritems(): # iterates through the db and takes one of the series 
    p = os.path.join (path, "%s.py" % key )
    serie_seasons = value ['seasons']
    serie_name = value ['title']
    for k, v in serie_seasons.iteritems():
        v_new = transform(serie_name, v, k)
        serie_seasons [k] = v_new

    with file (p ,  "w+")  as f: #names the files with the showID number
        f.write (pformat(value)) # f is a file object which was created in the previous line 
                                        # write writes the string of (string) to file
                                        #pformat is from pprint which makes the file nicer to read
                                        #
                                        



print "Program end"

