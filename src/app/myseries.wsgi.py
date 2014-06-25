#!/usr/bin/python
#-*- coding:  utf8 -*-


import bottle
import myseries
import os
import sys





def template (tpl_type):
    result_tpl = os.path.join(tpl_dir,tpl_type +'.tpl')
    assert os.path.isfile(result_tpl)
    return result_tpl


def accept (req):
    accepted = dict (req)['HTTP_ACCEPT']
    if 'json' in accepted:
        return 'json'
    else:
        return 'html'
    
def output_representation (data,  acc, tpl = None, other = {}):
    if acc == 'json':
        return repr(data)
    elif acc == 'html':
        assert tpl   
        return bottle.template(tpl,  data = data, other = other)

    
@bottle.route('/favicon.ico', method='GET')
def get_favicon():
    path = os.path.join (prefix,'img')
    return bottle.static_file ('favicon.ico', root = path)
    
@bottle.route('/mystyle.css', method='GET')
def get_mystyle():
    path = os.path.join (prefix,'tpl')
    return bottle.static_file ('mystyle.css', root = path)
    
@bottle.route('/vallmo.jpg', method='GET')
def get_background():
    path = os.path.join (prefix,'img')
    return bottle.static_file ('vallmo.jpg', root = path)    
    

    
@bottle.route('/')
def firstpage ():
    data = None
    acc = accept (bottle.request)
    tpl = template ('firstpage')
    other = {'prefix':prefix}
    show_data = output_representation (data,  acc,  tpl,  other)
    return show_data
    
@bottle.route('/series')
def all_series ():
    series = db.series()
    data = []    
    for k, v in series.iteritems():
        temp = [k, v]
        data.append(temp)
        
    acc = accept (bottle.request)
    tpl = template ('serieslist')
    other = {'heading1': 'Series'}
    show_data = output_representation (data, acc, tpl, other)
    return show_data  
"""kom ihåg här måste du göra en template som fixar urlarna"""

@bottle.route('/series_titles')
def all_series_titles ():
    data = db.series_titles()
    acc = accept (bottle.request)
    tpl = template ('list')

    other = {'heading1':'Series Titles:'}
    show_data = output_representation (data,  acc,  tpl,  other)
    return show_data
    
@bottle.route('/series_numbers')
def all_series_ids ():
    data = db.ids()
    acc = accept (bottle.request)   
    tpl = template ('list')

    other = {'heading1':'Series id number'}
    show_data = output_representation (data,  acc, tpl,  other)
    return show_data


@bottle.route('/serie/<serie_id>/seasons')
def serie_seasons (serie_id = '78'):
    serie = create_serie(serie_id)    
    data = serie.season_nrs ()
    acc = accept (bottle.request)
    tpl = template ('seasonslist')
    other = {'heading1':'Seasons'}
    other ['serie_id'] = serie_id   
   
    if isinstance (serie, myseries.Serie):
        other ['title'] = serie.title
        show_data = output_representation (data, acc,  tpl,  other)
        return show_data
    else:
        return serie

    
@bottle.route('/serie/<serie_id>/<season_id>/titles')
def season_titles (serie_id,  season_id):
    acc = accept (bottle.request)
    season = create_season (serie_id,  season_id)
    other = {'heading1':'Episode Titles'}
    data = season.episodes_titles()
    tpl = template ('list')
    
    if isinstance (season,  myseries.Season):
        other['title']= season.serie_title
        show_data = output_representation (data, acc, tpl,  other)
        return show_data
    else:
        return season  
        
        
#@bottle.route('/serie/<serie_id>/<season_id>/numbers')
#def season_code (serie_id,  season_id):
#    season = create_season (serie_id,  season_id)
#    title = season.serie_title
#    if isinstance (season,  myseries.Season):
#        return bottle.template(os.path.join(tpl_dir,'list.tpl'), header = 'Episodes in',  name = title,  nr = season.id,  result = season.episodes_nrs())
##        return season.episodes_nrs()
#    else:
#        return season
#
#        
#@bottle.route('/serie/<serie_id>/<season_id>/<episode_id>')
#def episode_code (serie_id,  season_id,  episode_id):
#    episode = create_episode (serie_id,  season_id,  episode_id)
#    if isinstance (episode,  myseries.Episode):
#        return bottle.template ('{{name}}', name = episode.title)
#    else:
#        return episode   
        
def create_serie (serie_id):
    try:
        db.has (serie_id)
        return myseries.Serie (db, serie_id)
    except AssertionError:
        return 'There is no such serie'
    

def create_season (serie_id, season_id):
    """Här måste du först skapa en förekomst av serie, sedan måste det bekräftas att den gick att skapa förkomsten
    sedan måste det kollas att den valda säsongen existerar"""
    try:
        serie = create_serie (serie_id)
        if isinstance (serie,  myseries.Serie):
            serie.has (season_id)
            season = myseries.Season (serie, season_id)
            return season
        else:
            return serie
    except AssertionError:
        return 'There is no such season in that serie'
  
    
def create_episode (serie_id,  season_id,  episode_id):
    try:
        season = create_season (serie_id, season_id)
        if isinstance (season,  myseries.Season):
            season.has (episode_id)
            episode = myseries.Episode (season,  episode_id)
            return episode
        else:
            return season
    except AssertionError:
        return 'There is no such episode in that season'


 
if __name__=="__main__":
    if len (sys.argv) > 1:
        prefix = sys.argv [1]

        env_obj = myseries.Environment (prefix)

        tpl_dir = os.path.join (env_obj.prefix, 'tpl')

        db = myseries.SeriesDatabase(prefix)
        bottle.debug(True)
        bottle.run (host='localhost',  port = 8080)
    else:
        print "Usage %s <prefix>" % sys.argv [0]
        sys.exit (-1)
else:
    path = os.path.dirname(os.path.realpath(__file__))
    prefix = os.path.dirname(path)

    env_obj = myseries.Environment (prefix)

    tpl_dir = os.path.join (env_obj.prefix, 'tpl')
    db_dir = env_obj.series_dir

    db = myseries.SeriesDatabase(db_dir)
    
    application = bottle.default_app()
