#!/usr/bin/python
#-*- coding:  utf8 -*-
import os,  pprint, argparse,  sys



class SeriesDatabase (object):
    """Database holding information about series, seasons and episodes"""
    def __init__(self, x):
        """Initialize the database of series placed in'x'"""
        assert os.path.isdir (x)
        self.basepath = x

    def filepath (self,  id):
        fn = os.path.join(self.basepath, '%s.py' % id)
        return fn

    def ids (self):
        """List of all serie's identitys"""
        fns = os.listdir (self.basepath)
        return [fn.split('.')[0] for fn in fns if fn.split('.')[1]  == 'py' ]#

    def has (self,  id):
        """Is there a serie with identity 'id' in the database"""
        fn = self.filepath(id)
        status = os.path.isfile(fn)
        return status

    def serie_data (self,  id):
        """Serie's data content"""
        assert self.has (id)
        fn = self.filepath(id)
        result = []
        with file (fn)  as f:
            body = f.read()
            result = eval(body)
        return result

    def serie (self,  id):
        """Serie with identity 'id'"""
        assert self.has (id)
        result = Serie (self,  id)
        return result
        
    def show_details(self):
        print self.basepath

class Serie (object):
    """The series title, its seasons, episodes, episodes names etc."""
    def __init__(self, db, id):
        assert db.has (id)
        self.db = db
        self.id = id
        self.contents = db.serie_data (id)
        self.path = db.filepath (id)
        self.sorted_season_numbers = None

    def serie_name (self):
        """the serie title"""
        name = self.contents ['title']
        return name
        
    def has (self,  season_id):
        """Is there a season with 'season_id' in the serie """
        seasons = self.contents ['seasons']
        result = season_id in seasons
        return result     
        

    def season_nrs (self):
        """a list with the season numbers"""
        if not self.sorted_season_numbers:#För att det bara skall göras en gång
            seasons = self.contents ['seasons']
            season_nrs = seasons.keys ()
            season_nrs.sort ()
            self.sorted_season_numbers = season_nrs
        return self.sorted_season_numbers 

    def seasons (self):
        """a dictionary with the seasons and a list with the season numbers"""
        seasons_contents = self.contents ['seasons']
        return seasons_contents, self.season_nrs ()

    def episodes (self):
        """list with all the episodes in the serie"""
        episode_list = []
        seasonsc = self.seasons () [0]
        season_episodes = []
        for key, content in seasonsc.iteritems():
            season_episodes.append(key)            
            for ep in content:
                episode_list.append (ep)
                season_episodes.append(ep)
        return episode_list, season_episodes
        
    def show_details(self):
        print self.id
        print self.contents
        print'här visar vi säsongsinformation'

    def season (self, id):
        """Creates an instance of the class season with identity 'id' """
        result = None
        if self.has (id):
            result = Season (self, id)
        return result

    def episode (self,  season_id,  episode_id):
        """Creates an instance of the class episode with identity 'season_id' and 'episode_id' '"""
        season_obj = self.season (season_id)
        result = Episode (season_obj,  episode_id) ## season_obj.episode (id)
        return result
        

class Season (object):
    """Holding Season data in a particular serie"""
    def __init__ (self,  serie_obj , season_id):
        assert isinstance (serie_obj,  Serie)#Inte nödvändigt här utan bara för att visa hur man kan göra
        assert serie_obj.has (season_id)
        self.id = season_id
        self.serie = serie_obj
        
    def season_nr(self):
        print 'This is season %s of %s'(self.id, len(self.serie.season_nrs))
    
    def episodes (self):
        """A list with all the episodes given a season_id"""
        episodes_list = self.serie.contents ['seasons'] [self.id]
        return episodes_list
        
    def episode(self, episode_id):
        episode_obj = Episode (self,  episode_id)
        return episode_obj
        
    def show_details(self):
        print self.id
        print 'här visar vi information om säsongen'
        
    

class Episode (object):
    def __init__ (self, season_obj, episode_id):
        self.id = episode_id
        self.season_id = season_obj.id
        
    def episode_name(self):   
    
        pass
        
    def episode_url(self):
        
        pass
        
    def show_details(self):
        print 'här visar vi information om avsnittet'



def show_serie(db,  args):
    
    if not args.serie:
        try:
            assert not args.season and not args.episode
            db.show_details ()
        except AssertionError:
            print  '-season or -episode are invalid if no -serie is given'
            sys.exit (-1)
    else:
        serie = Serie (database, args.serie)
        if not args.season:
            try:
                assert not args.episode
                serie.show_details ()
            except AssertionError:
                print '-episode is invalid if no -serie and -season is given'
                sys.exit (-1)
        else:
            season = serie.season (args.season)
            if not args.episode:
                season.show_details()
            else:
                episode = serie.episode(args.season, args.episode)
                episode. show_details()
                
                
#    if args.season:
#        if args.season and not args.serie:
#            parser.error ('if a season is specified so must a serie')
#        else:
#            if args.season in serie.season_nrs():
#                print 'ok'
#            else:
#                print 'no such season exist in that serie'
#                print 'The seasons for that series are:',  ', '.join(serie.season_nrs())



if __name__=='__main__':#gör att det bara körs om det är huvudprogrammet



    parser = argparse.ArgumentParser('Get serie, season or episode data from a database') 
    parser.add_argument('-p' ,'--prefix',  help = 'The path to your database')
    parser.add_argument('-s', '--serie', default = '',  help = 'The ID of the serie')
    parser.add_argument('-t','--season', default = '',  help = 'A specific season of the serie')
    parser.add_argument('-e','--episode', default = '',  help = 'A specific episode in a season of the serie (name or number)')

    parser.add_argument('todo', nargs = '?',    help = '''show, search, add, delete or getsub''')    

    args = parser.parse_args()
    if args.prefix:
        database = SeriesDatabase(args.prefix)
    else:
        parser.error ('You have to give the path to the database') 


    comm = args.todo or 'show'#makes the default to be 'show'

    if comm == 'show':
        show_serie (database, args)
    elif comm == 'add':
        pass
    elif comm == 'delete':
        pass
    elif comm == 'getsub':
        pass    
    else:
        print 'There is no such option'






#    db = SeriesDatabase ('/home/carolina/proj/edu/data/addic7ed')
#    s = Serie (db, '78')
#    s = db.serie ('78')

#
#  h = SeriesDatabase(args.prefix)
#        f = Serie(h, args.serie)
#        f.season(args.season)



#    pprint. pprint (s.serie_name())
#    pprint. pprint (s.seasons())
#    pprint. pprint (s.episodes())
#    n = len(s.episodes())
#    print n

#    pprint .pprint (db.ids())
#    pprint .pprint (db.has('78'))
#    pprint .pprint (db.serie_data('78'))
#    pprint .pprint (db.serie('78'))
#    pprint. pprint (Serie(db, 78))
