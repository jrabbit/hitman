#Hitman. Or The Professional. (c) 2010 Jrabbit Under GPL v3 or later.
import yaml
import feedparser
import sys
import os
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
    pass

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
    g = URLGrabber(reget='simple') #Donno if this is sane/works.
    data = g.urlgrab(url)
    save_name = urlparse.urlparse(url) 
    # get jsut a file.ext
    f = open(os.path.join(dl_folder, feed_name, save_name), 'w')
    f.write(data)

def add_feed(url):
    """add to yaml config file or db"""
    pass

def get_feeds():
    """read out all feed information,
    return as a dictionary indexed by feed name proper"""
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        addfeed(sys.argv[1])
    hitsquad()