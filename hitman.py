#Hitman. Or The Professional. (c) 2010 Jrabbit Under GPL v3 or later.
import feedparser
import sys
import os
import anydbm
import urlparse
from urlgrabber.grabber import URLGrabber

def put_a_hit_out(name):
    """Download a feeds most recent enclosure that we don't have"""
    feeds = get_feeds()
    url = feeds[name] 
    d = feedparser.parse(url)
    print d.feed.title
    if len(d.entries[0].enclosures):
        print d.entries[0].enclosures[0]
        print d.feed.updated_parsed
    download(d.entries[0].enclosures[0])
    growl("Mission Complete: %s downloaded") % d.feed.title
    print "Mission Complete: %s downloaded" % d.feed.title

def hitsquad():
    """"\'put a hit out\' on all known rss feeds"""
    feeds = get_feeds()
    for name, feed in feeds.iteritems():
        put_a_hit_out(name)

def growl():
    """send a growl notification if on mac osx (use GNTP or the growl lib)"""
    if platform.system() == 'Darwin':
        #growl proper
        pass
    elif platform.system() == 'Linux':
        #Do an OSD-Notify
        pass
    else:
        #Can I test for growl for windows?
        pass

def download(url):
    """should do continues"""
    db = anydbm.open('downloads', 'c')
    g = URLGrabber(reget='simple') #Donno if this is sane/works.
    try:
        data = g.urlgrab(url)
    except:
        db[url] = 'Error'
    save_name = urlparse.urlparse(url) 
    # get jsut a file.ext
    f = open(os.path.join(dl_folder, feed_name, save_name), 'w')
    f.write(data)
    db[url] = 'Downloaded'

def add_feed(url, name):
    """add to yaml config file or db"""
    db = anydbm.open('feeds', 'c')
    db[name] = url
    db.close()

def alias_feed(name, alias):
    """write aliases to db"""
    db = anydbm.open('aliases', 'c')
    db[alias] = name
    db.close()

def get_feeds():
    """read out all feed information,
    return as a dictionary indexed by feed name proper"""
    db = anydbm.open('feeds', 'c')
    return db

if __name__ == "__main__":
    if len(sys.argv) > 2:
        addfeed(sys.argv[1], sys.argv[2])
    hitsquad()