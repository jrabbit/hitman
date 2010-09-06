#Hitman. Or The Professional. (c) 2010 Jrabbit Under GPL v3 or later.
import sys
import os
import anydbm
import urlparse
import platform
import feedparser
from subprocess import *
try:
    from urlgrabber.grabber import URLGrabber
    
except ImportError:
    raise
    print "It appears you do not have pycurl (http://pycurl.sourceforge.net/) installed."
try:
    import urlgrabber.progress 
except ImportError:
    raise
    print "Windows lusers: Please fix your termios ANSI capability in your terminal"

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
    if d.entries[0].enclosures:
        if 'verbose' in get_settings():
            print d.entries[0].enclosures[0]
        #print d.feed.updated_parsed // Doesn't work everywhere, may nest in try or use .headers['last-modified']
        url = str(d.entries[0].enclosures[0]['href'])
        
        if url not in anydbm.open(os.path.join(directory(), 'downloads'), 'c'):
            download(url, name)
        
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
        if Popen(['which', 'growlnotify'], stdout=PIPE).communicate()[0]:
            os.system("growlnotify -t Hitman -m %r" % str(text))
    elif platform.system() == 'Linux':
        if Popen(['which', 'notify-send'], stdout=PIPE).communicate()[0]:
            #Do an OSD-Notify
            #notify-send "Totem" "This is a superfluous notification"
            os.system("notify-send \"Hitman\" \"%r\" " % str(text))
        
    else:
        pass
        #Can I test for growl for windows?

def download(url, name):
    """should do continues"""
    db = anydbm.open(os.path.join(directory(), 'downloads'), 'c')
    g = URLGrabber(reget='simple') #Donno if this is sane/works.
    print "Downloading %s" % url
    # try:
    settings = get_settings()
    
    if 'dl' in settings:
        save_name = os.path.join(settings['dl'], name)
        os.chdir(save_name)
    try:
        if 'prefer_wget' in settings:
                os.system("wget -c %s" % url )
        elif 'prefer_curl' in settings:
                os.system("curl -C - -O -L %s" % url)
        else:
            if urlgrabber.progress:
                prog = urlgrabber.progress.text_progress_meter()
                g.urlgrab(url, progress_obj=prog)
                #Thanks http://thejuhyd.blogspot.com/2007/04/youtube-downloader-in-python.html
            else:
                g.urlgrab(url)
        db[url] = 'Downloaded'
    except KeyboardInterrupt:
        print "Downloads paused. They will resume on restart of hitman.py"
        sys.exit()
    

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

def export_opml():
    feeds = get_feeds()
    # print feeds
    #  for name in feeds:
    #          print name
    #          print feeds[name]
    #Thanks to the canto project- used under the GPL
    print """<opml version="1.0">"""
    print """<body>"""
    for name in feeds:
        kind = feedparser.parse(feeds[name]).version
        if kind[:4] == 'atom':
            t = 'pie'
        elif kind[:3] == 'rss':
            t = 'rss'
        print """\t<outline text="%s" xmlUrl="%s" type="%s" />""" %\
                (name, feeds[name], "rss")
    print """</body>"""
    print """</opml>"""
    #end canto refrenced code

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
    cmd = sys.argv[1]
    if len(sys.argv) > 1:
        if  sys.argv[1][-3:] == 'xml' or sys.argv[1][-4:] == 'atom' :
            print "Added your feed as %s" % str(add_feed(sys.argv[1]))
        if cmd == 'set':
            if len(sys.argv) > 2:
                name = sys.argv[2]
                value = sys.argv[3]
                if value in ['0', 'false', 'no', 'off', 'False']:
                    del get_settings()[name]
                else:
                    get_settings()[name] = key
        elif cmd == 'help':
            helppage = open('help', 'r')
            print helppage.read()
        elif cmd == 'alias':
            alias_feed(sys.argv[2], sys.argv[3])
            #alias name alias
        elif cmd == 'down':
            if len(sys.argv) > 2:
                 put_a_hit_out(sys.argv[2])
        elif cmd == 'export':
            export_opml()
        else:
            helppage = open('help', 'r')
            print helppage.read()
    else:
        hitsquad()
