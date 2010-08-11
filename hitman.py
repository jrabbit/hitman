#Hitman. Or The Professional. (c) 2010 Jrabbit Under GPL v3 or later.
import feedparser
import sys
import os
import anydbm
import urlparse
from urlgrabber.grabber import URLGrabber
import platform
try:
    import urlgrabber.progress 
    #depends on termios... not avail on win32

def put_a_hit_out(name):
    """Download a feeds most recent enclosure that we don't have"""
    feeds = get_feeds()
    aliases = get_aliases()
    if feeds[name]:
        url = feeds[name]
    elif aliases[name]:
        url = feeds[aliases[name]]
    d = feedparser.parse(url)
    print d.feed.title
    if len(d.entries[0].enclosures):
        print d.entries[0].enclosures[0]
        #print d.feed.updated_parsed // Doesn't work everywhere, may nest in try or use .headers['last-modified']
    download(str(d.entries[0].enclosures[0]['href']))
    growl("Mission Complete: %s downloaded" % d.feed.title)
    print "Mission Complete: %s downloaded" % d.feed.title

def hitsquad():
    """"\'put a hit out\' on all known rss feeds"""
    feeds = get_feeds()
    for name, feed in feeds.iteritems():
        put_a_hit_out(name)

def growl(text):
    """send a growl notification if on mac osx (use GNTP or the growl lib)"""
    if platform.system() == 'Darwin':
        #growl proper
        pass
    elif platform.system() == 'Linux':
        from subprocess import *
        if Popen(['which', 'notify-send'], stdout=PIPE).communicate()[0]:
            #Do an OSD-Notify
            #notify-send "Totem" "This is a superfluous notification"
            os.system("notify-send \"Hitman\" \"%s\" " % text)
        
    else:
        pass
        #Can I test for growl for windows?

def download(url):
    """should do continues"""
    db = anydbm.open(os.path.join(directory(), 'downloads'), 'c')
    g = URLGrabber(reget='simple') #Donno if this is sane/works.
    print "Downloading %s" % url
    try:
        settings = get_settings()
        save_name = urlparse.urlparse(url)
        if settings['prefer_wget']:
            os.system("wget -c %s" % url)
        elif settings['prefer_curl']:
            os.system("curl -C - -O -L %s" % url)
        else:
            if urlgrabber.progress:
                prog = urlgrabber.progress.text_progress_meter()
                g.urlgrab(url, progress_obj=prog)
                #Thanks http://thejuhyd.blogspot.com/2007/04/youtube-downloader-in-python.html
            else:
                g.urlgrab(url)
                print "Sorry termios isn't supported by your OS for a progress meter"
        #g.urlgrab(url, filename='%s' % save_name)
        # get jsut a file.ext
        #f = open(os.path.join(dl_folder, feed_name, save_name), 'w')
        #f.write(data)
        db[url] = 'Downloaded'
    except:
        db[url] = 'Error'
    

def add_feed(url):
    """add to yaml config file or db"""
    db = anydbm.open(os.path.join(directory(), 'feeds'), 'c')
    name = str(feedparser.parse(url).feed.title)
    db[name] = url
    db.close()
    return name

def alias_feed(name, alias):
    """write aliases to db"""
    db = anydbm.open(os.path.join(directory(), 'aliases'), 'c')
    db[alias] = name
    db.close()

def get_aliases():
    db = anydbm.open(os.path.join(directory(), 'aliases'), 'c')
    return db
    
def get_feeds():
    """read out all feed information,
    return as a dictionary indexed by feed name proper"""
    db = anydbm.open(os.path.join(directory(), 'feeds'), 'c')
    return db

def get_settings():
    db = anydbm.open(os.path.join(directory(), 'settings'), 'c')
    return db

def directory():
    #Construct hitman_dir from os name
    home = os.path.expanduser('~') 
    if platform.system() == 'Linux':
        hitman_dir = os.path.join(home, '.hitman')
    elif platform.system() == 'Darwin':
        hitman_dir = os.path.join(home, 'Library', 'Application Support', 'hitman')
    elif platform.system() == 'Windows':
        hitman_dir = os.path.join(os.environ['appdata'], 'hitman')
    else:
        hitman_dir = os.path.join(home, '.hitman')
    if not os.path.isdir(hitman_dir):
        os.mkdir(hitman_dir)
    return hitman_dir

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "Added your feed as %s" % str(add_feed(sys.argv[1]))
    #TODO Subcommands, ghetto or not
    hitsquad()