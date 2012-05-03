#!/usr/bin/env python

#Hitman. Or The Professional. (c) 2010 - 2011 Jrabbit Under GPL v3 or later.
import sys
import os
import anydbm
import urlparse
import platform
from subprocess import *
import json
import time

import gntplib
import baker
import feedparser
try:
    from urlgrabber.grabber import URLGrabber
except ImportError:
    raise
    print "It appears you do not have pycurl (http://pycurl.sourceforge.net/) \
    installed."
try:
    import urlgrabber.progress
except ImportError:
    raise
    print "Windows lusers: Please fix your termios \
    ANSI capability in your terminal"

@baker.command(name="down")
def put_a_hit_out(name):
    """Download a feeds most recent enclosure that we don't have"""
    feed = resolve_name(name)
    d = feedparser.parse(feed)
    print d.feed.title
    if d.entries[0].enclosures:
        if 'verbose' in get_settings():
            print d.entries[0].enclosures[0]
        # print d.feed.updated_parsed
        # Doesn't work everywhere, may nest in try or
        # use .headers['last-modified']
        url = str(d.entries[0].enclosures[0]['href'])
        if url.split('/')[-1] not in anydbm.open(os.path.join(directory(), 'downloads'), 'c'):
            download(url, name, feed)
            growl("Mission Complete: %s downloaded" % d.feed.title)
            print "Mission Complete: %s downloaded" % d.feed.title
        else:
            growl("Mission Aborted: %s already downloaded" % d.feed.title)
            print "Mission Aborted: %s already downloaded" % d.feed.title

@baker.command(name="select")
def selective_download(name, oldest, newest=0):
    "Note: RSS feeds are counted backwards, default newest is 0, the most recent."
    feed = resolve_name(name)
    d = feedparser.parse(feed)
    if not d.entries[1]:
        print "Error: This feed does not list old items."
        return
    try:
        d.entries[int(oldest)]
    except IndexError:
        print "Error feed does not contain this many items."
        print "Hitman thinks there are %d items in this feed." % len(d.entries)
        return
    for url in [q.enclosures[0]['href'] for q in d.entries[int(newest):int(oldest)]]:
        # iterate over urls in feed from newest to oldest feed items.
        url = str(url)
        if url.split('/')[-1] not in anydbm.open(os.path.join(directory(), 'downloads'), 'c'):
            download(url, name, feed)

def resolve_name(name):
    """Takes a given input from a user and finds the url for it"""
    feeds = get_feeds()
    aliases = get_aliases()
    if name in aliases:
        return feeds[aliases[name]]
    elif name in feeds:
        return feeds[name]
    else:
        print "Cannot find feed named: %s" % name
        return

@baker.command(default=True)
def hitsquad():
    "\'put a hit out\' on all known rss feeds [Default action without arguements]"
    feeds = get_feeds()
    for name, feed in feeds.iteritems():
        put_a_hit_out(name)
    if len(feeds) == 0:
        baker.usage()


def growl(text):
    """send a growl notification if on mac osx (use GNTP or the growl lib)"""
    if platform.system() == 'Darwin':
        gntplib.publish("Hitman", "Status Update", "Hitman", text=text)
        # if Popen(['which', 'growlnotify'], stdout=PIPE).communicate()[0]:
        #     os.system("growlnotify -t Hitman -m %r" % str(text))
    elif platform.system() == 'Linux':
        try: 
            import pynotify
            pynotify.init("Hitman")
            n = pynotify.Notification("Hitman Status Report", text)
            n.set_timeout(pynotify.EXPIRES_DEFAULT)
            n.show()
        except ImportError:
            if Popen(['which', 'notify-send'], stdout=PIPE).communicate()[0]:
                #Do an OSD-Notify
                #notify-send "Totem" "This is a superfluous notification"
                os.system("notify-send \"Hitman\" \"%r\" " % str(text))
    elif platform.system() == 'Haiku':
        os.system("notify --type information --app Hitman \
        --title 'Status Report' '%s'" % str(text))
    elif platform.system() == 'Windows':
        try:
            gntplib.publish("Hitman", "Status Update", "Hitman", text=text)
        except:
            print "Install Growl For windows if you want notifications! \n http://www.growlforwindows.com/gfw/"
    else:
        pass
        #Can I test for growl for windows?


def download(url, name, feed):
    """url - the file to be downloaded
    name - the name of the feed [TODO: remove]
    feed - the feed url"""
    db = anydbm.open(os.path.join(directory(), 'downloads'), 'c')
    g = URLGrabber(reget='simple')
    print "Downloading %s" % url
    settings = get_settings()
    if 'dl' in settings:
        save_name = os.path.join(settings['dl'], name)
        dl_dir = settings['dl']
    else:
        dl_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    try:
        if 'prefer_wget' in settings:
                Popen(['wget', '-c', url], cwd=dl_dir, stout=PIPE).wait()
        elif 'prefer_curl' in settings:
                Popen(['curl', '-C', '-', '-O', '-L', url], cwd=dl_dir, stout=PIPE).wait()
        else:
            old_pwd = os.getcwd()
            os.chdir(dl_dir)
            # TODO: fidn urlgrabber equiv to pwd
            if urlgrabber.progress:
                prog = urlgrabber.progress.text_progress_meter()
                g.urlgrab(url, progress_obj=prog)
                os.chdir(old_pwd)
#Thanks http://thejuhyd.blogspot.com/2007/04/youtube-downloader-in-python.html
            else:
                g.urlgrab(url)
                os.chdir(old_pwd)
        db[url.split('/')[-1]] = json.dumps({'url': url,
        'date': time.ctime(), 'feed': feed})
    except KeyboardInterrupt:
        print "Downloads paused. They will resume on restart of hitman.py"
        try:
            os.chdir(old_pwd)
        except:
            print "Couldn't return to old pwd, sorry!"
        sys.exit()


def add_feed(url):
    """add to db"""
    db = anydbm.open(os.path.join(directory(), 'feeds'), 'c')
    name = str(feedparser.parse(url).feed.title)
    db[name] = url
    db.close()
    return name

@baker.command(name="rm")
def del_feed(name):
    """remove from database (and delete aliases)"""
    aliases = get_aliases()
    feeds = get_feeds()
    if aliases[name]:
        proper_name = aliases[name]
    elif feeds[name]:
        proper_name = feeds[name]
    for k, v in aliases:
        if v == proper_name:
            del aliases[k]
    #deleted from aliases
    del feeds[proper_name]
    #deleted from feeds db
    feeds.close()

@baker.command(name="unalias")
def del_alias(alias):
    """sometimes you goof up."""
    db = anydbm.open(os.path.join(directory(), 'aliases'), 'c')
    print "removing alias of %s to %s" % (alias, db.pop(alias))
    db.close()

@baker.command(name="alias")
def alias_feed(name, alias):
    """write aliases to db"""
    db = anydbm.open(os.path.join(directory(), 'aliases'), 'c')
    if alias in db:
        print "Something has gone horribly wrong with your aliases!\
         Try deleting the %s entry." % name
        return
    db[alias] = name
    db.close()


def get_downloads():
    db = anydbm.open(os.path.join(directory(), 'downloads'), 'c')
    return db


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

@baker.command(name="list")
def list_feeds():
    """List all feeds in plain text and give their aliases"""
    feeds = get_feeds()
    aliases_db = get_aliases()
    for feed in feeds:
        name = feed
        url = feeds[feed]
        aliases = []
        for k, v in aliases_db.items():
            if v == name:
                aliases.append(k)
        if aliases:
            print name, " : %s Aliases: %s" % (url, aliases)
        else:
            print  name, " : %s" % url

@baker.command(name="export")
def export_opml():
    "Export an OPML feed list"
    feeds = get_feeds()
    #Thanks to the canto project- used under the GPL
    print """<opml version="1.0">"""
    print """<body>"""
    #Accurate but slow.
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

@baker.command(name="import")
def import_opml(url):
    """Import an OPML file locally or from a URL. Uses your text attributes as aliases."""
    #Test if URL given is local, then open, parse out feed urls,
    #add feeds, set text= to aliases and report success, list feeds added
    from bs4 import BeautifulSoup
    from urllib2 import urlopen
    try:
        f = file(url).read()
    except IOError:
        f = urlopen(url).read()
    soup = BeautifulSoup(f, "xml")
    links = soup.find_all('outline', type="rss" or "pie")
    #This is very slow, might cache this info on add
    for link in links:
        #print link
        add_feed(link['xmlurl'])
        print link['text']


def is_feed(url):
    d = feedparser.parse(url)
    if d.bozo and d.bozo_exception:
        return False
    else:
        return True


def directory():
    """Construct hitman_dir from os name"""
    home = os.path.expanduser('~')
    if platform.system() == 'Linux':
        hitman_dir = os.path.join(home, '.hitman')
    elif platform.system() == 'Darwin':
        hitman_dir = os.path.join(home, 'Library', 'Application Support',
         'hitman')
    elif platform.system() == 'Windows':
        hitman_dir = os.path.join(os.environ['appdata'], 'hitman')
    else:
        hitman_dir = os.path.join(home, '.hitman')
    if not os.path.isdir(hitman_dir):
        os.mkdir(hitman_dir)
    return hitman_dir

@baker.command
def add(url):
    """"Add a atom or RSS feed by url. 
    If it doesn't end in .atom or .rss we'll do some guessing."""
    if url[-3:] == 'xml' or url[1][-4:] == 'atom':
        print "Added your feed as %s" % str(add_feed(url))
    elif is_feed(url):
         print "Added your feed as %s" % str(add_feed(url))

@baker.command(name="set")   
def set_settings(key, value=False):
    if value in ['0', 'false', 'no', 'off', 'False']:
        del get_settings()[key]
        print "Disabled setting"
    else:
        get_settings()[name] = value
        print "Setting saved"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        baker.run()
    else:
        hitsquad()
