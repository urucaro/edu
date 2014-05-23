#!/usr/bin/python
#-*- coding:  utf8 -*-
import os,  pprint, argparse,  sys,  urllib2
from bs4 import BeautifulSoup

def create_dir (p):
    if not os.path.isdir (p):
            os.mkdir (p)
    return p

class Environment (object):
    def __init__ (self,  p):
        """Create an environment based on the prefix 'p'"""
        assert os.path.isdir (p)
        self.prefix = p
        self.series_dir = create_dir (os.path.join (p,  'series'))
        self.subs_dir = create_dir (os.path.join (p,  'subs'))

class SeriesDatabase (object):
    """Database holding information about series, seasons and episodes"""
    def __init__(self, x):
        """Initialize the database of series placed in'x'"""
        assert os.path.isdir (x)
        self.env = Environment (x)
        self.basepath = self.env.series_dir

    def filepath (self,  id):
        """The path to the file (serie) with filename 'id' """
        fn = os.path.join(self.basepath, '%s.py' % id)
        return fn

    def ids (self):
        """List of all serie's identitys"""
        fns = os.listdir (self.basepath)
        return [fn.split('.')[0] for fn in fns if fn.split('.')[1]  == 'py' ]

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
        
    def episode(self, serie_id,  season_id,  episode_id):
        """returns an instance of the class 'Episode' """
        serie_obj = Serie(self, serie_id)
        season_obj = serie_obj.season( season_id)
        episode_obj = season_obj.episode(episode_id)
        return episode_obj
        
    def show_details(self):
        print self.basepath

class Serie (object):
    """The series title, its seasons, episodes, episodes names etc."""
    def __init__(self, db_obj, id):
        assert db_obj.has (id)
        self.db = db_obj
        self.id = id
        self.data = db_obj.serie_data (id)
        self.seasons = self.data ['seasons']
        self.title =  self.data ['title']
        self.path = db_obj.filepath (id)
        self.sorted_season_numbers = None # To lazy access

    def has (self,  season_id):
        """Is there a season with 'season_id' in the serie """
        seasons = self.data ['seasons']   
        status = season_id in seasons
        return status
        

    def season_nrs (self):
        """a list with the season numbers"""
        if not self.sorted_season_numbers:#För att det bara skall göras en gång
            seasons = self.data ['seasons']
            season_nrs = seasons.keys ()
            season_nrs.sort ()
            self.sorted_season_numbers = season_nrs
        return self.sorted_season_numbers 

    def episodes (self):
        """list with all the episodes in the serie"""
        episode_list = []
        seasonsc = self.seasons
        for key, content in seasonsc.iteritems():
            for ep in content:
                episode_list.append (content [ep] ['title'].replace ('_', ' '))
        return episode_list

    def season (self, id):
        """Creates an instance of the class season with identity 'id' """
        result = Season (self, id)
        return result


    def show_details(self):
        """SHows the deails of the serie such as title,id nr and the titles of all the episodes"""
        print 'The series title is "%s" and its id nr is %s'% (self.title,  self.id)
        print 'It contains %s seasons' % len(self.season_nrs ())
        print 'The episodes in the serie are:'
        pprint.pprint ((self.episodes()))
        
        


class Season (object):
    """Holding Season data in a particular serie"""
    def __init__ (self,  serie_obj , season_id):
        assert isinstance (serie_obj,  Serie)#Inte nödvändigt här utan bara för att visa hur man kan göra
        assert serie_obj.has (season_id)
        self.id = season_id
        self.serie_obj = serie_obj
        self.db = self.serie_obj.db
        self.data = serie_obj.seasons[season_id]
        self.sorted_ep_nrs = None # lazy access
        
    def season_nr(self):
        """A string which tells what season it is of the total number in the serie"""
        print 'This is season %s of %s'(self.id, len(self.serie.season_nrs))
    
    def episodes_nrs (self):
        """A list with all the episode nrs given a season_id"""
        if not self.sorted_ep_nrs:
            sorted_ep_nrs = self.data.keys()
            sorted_ep_nrs.sort(key = lambda x: int(x))#key kräver en funktion 
        return sorted_ep_nrs
        
    def episodes_titles(self):
        """a list with all the eoisodes in given season"""
        titles = [self.data[ep]['title'] for  ep in self.data]
        return titles
        
    def has(self, episode_id):
        """does this episode_id exist in this serie and season"""
        result = episode_id in self.data   
        return result
        
    def episode(self, episode_id):
        """Returns an instance of the class 'Episode' given a season object and an episode id"""
        episode_obj = Episode (self,  episode_id)
        return episode_obj
       
    def show_details(self):
        """Shows some details as the season nr, the number of episodes and their titles"""
        print self.id
        print self.episodes_nrs ()
        print self.episodes_titles ()
        
    

class Episode (object):
    """Holding data of an episode in a given database, serie and  season"""
    def __init__ (self, season_obj, episode_id):
        assert season_obj.has (episode_id) 
        self.id = episode_id
        self.season_id = season_obj.id
        self.season_obj = season_obj
        self.db = self.season_obj.db
        self.data = self.season_obj.data [self.id]
        
    def __getattr__(self, key):
        return self.data [key]
       
    def show_details(self):
        """Prints the episode's in number, title and url"""
        print self.id,  self.title,  self.url  #de två sista hittas genom __getattr__
        
    def get_sub(self):
        """Fetches the subtitles from addic7ed from url specified in given database (db) for that episode"""
        url_split = urlparse.urlsplit (self.url)
        head,  tail = url_split.path.rsplit ('/', 1)
        new_path =  head,  'addic7ed'
        referer = urlparse.urlunsplit(url_split._replace(path=urlparse.urljoin(*new_path)))
        
        domain = self.url
        response = urllib2.urlopen(domain)#Opens the url
        html = response.read ()#loads the html code
        soup = BeautifulSoup (html)#interprets (parse?) the html code
        links = []
        for x in soup.find_all (class_ ="buttonDownload"):
            links.append (x.attrs['href'])
        
        domain = 'http://www.addic7ed.com/'
        urls = []
        for link in links:
            urls.append (urlparse.urljoin (domain, link))
        
        page = urls[0]
        req = urllib2.Request(page,  headers ={'User-Agent' : 'Mozilla 5.10', 'Referer' : referer})
        response = urllib2.urlopen (req)
        data = response.read()
        
        test = response.info()
        print test
        
        if response.info().has_key('Content-Disposition'):
            with open(os.path.join(self.db.env.subs_dir ,'%s.srt' % self.title), 'wb') as f:
                f.write(data)
        else:
            return response.info()


def show_serie(db,  args):
    
    if not args.serie:
        try:
            assert not args.season and not args.episode
            db.show_details ()
        except AssertionError:
            print  '-season or -episode are invalid if no -serie is given'
            sys.exit (-1)
    else:
        serie = Serie (db, args.serie)
        if not args.season:
            try:
                assert not args.episode
                serie.show_details ()
            except AssertionError:
                print '-episode is invalid if no -serie and -season is given'
                sys.exit (-1)
        else:
            try:
             season = serie.season (args.season)
             if not args.episode:
                season.show_details ()
             else:
                 try:
                     episode = season.episode (args.episode)
                     episode. show_details ()
                 except AssertionError:
                     print 'There is no such Episode in given season'
                     print 'The episodes that exists are %s'  % ' ,'.join(season.episodes_nrs())
                     sys.exit (-1)
            except AssertionError:
                print 'there is no such season in given serie'
                sys.exit (-1)


#-----------------------------------------------------------------------------------------------------------
if __name__=='__main__':#gör att det bara körs om det är huvudprogrammet

    def test():
        prefix = '/home/carolina/proj/edu/data'
        db = SeriesDatabase (prefix)


    parser = argparse.ArgumentParser('Get serie, season or episode data from a database') 
    parser.add_argument('-p' ,'--prefix',  help = 'The path to your database')
    parser.add_argument('-s', '--serie', default = '',  help = 'The ID of the serie')
    parser.add_argument('-t','--season', default = '',  help = 'A specific season of the serie')
    parser.add_argument('-e','--episode', default = '',  help = 'A specific episode in a season of the serie (name or number)')

    parser.add_argument('todo', nargs = '?',    help = 'show, search, or getsub')    

    args = parser.parse_args()
    if args.prefix:
        database = SeriesDatabase(args.prefix)
    elif not args.prefix and args.todo == 'test':
        print 'jättebra'        
    elif not args.prefix or args.todo:
        parser.error ('You have to give the path to the database') 


    comm = args.todo or 'show'#makes the default to be 'show'

    if comm == 'show':
        show_serie (database, args)
    elif comm == 'getsub':
        pass        
    elif comm == 'search':
        pass
    elif comm == 'test':
        test()
    else :
        print 'There is no such option'


