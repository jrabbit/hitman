#!/usr/bin/env python

# Hitman. Or The Professional.
# (c) 2010 - 2011, 2015 - 2017 Jack Laxson <Jrabbit>
# Licensed under GPL v3 or later.

import json
import logging
import os
import platform
import time
from subprocess import Popen, PIPE


import six
import click
import feedparser
import requests
import semidbm

from clint.textui import progress

logger = logging.getLogger(__name__)

folder = click.get_app_dir("hitman")

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('--debug', default=False, is_flag=True)
@click.option('--verbose/--silent', default=True)
def cli_base(ctx, verbose, debug):
    # only the first basicConfig() is respected.
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    if verbose:
        logging.basicConfig(level=logging.INFO)
    if ctx.invoked_subcommand is None:
        hitsquad(ctx)


@cli_base.command("down")
@click.argument("name")
def put_a_hit_out(name):
    """Download a feed's most recent enclosure that we don't have"""

    feed = resolve_name(name)
    if six.PY3:
        feed = feed.decode()
    d = feedparser.parse(feed)
    # logger.info(d)
    # logger.info(feed)
    print(d['feed']['title'])
    if d.entries[0].enclosures:
        with Database("settings") as s:
            if 'verbose' in s:
                print(d.entries[0].enclosures[0])

        # print d.feed.updated_parsed
        # Doesn't work everywhere, may nest in try or
        # use .headers['last-modified']
        url = str(d.entries[0].enclosures[0]['href'])
        with Database("downloads") as db:
            if url.split('/')[-1] not in db:
                with Database("settings") as settings:
                    if 'dl' in settings:
                        dl_dir = settings['dl']
                    else:
                        dl_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                requests_get(url, dl_dir)
                db[url.split('/')[-1]] = json.dumps({'url': url, 'date': time.ctime(), 'feed': feed})
                growl("Mission Complete: %s downloaded" % d.feed.title)
                print("Mission Complete: %s downloaded" % d.feed.title)
            else:
                growl("Mission Aborted: %s already downloaded" % d.feed.title)
                print("Mission Aborted: %s already downloaded" % d.feed.title)


@cli_base.command("select")
@click.argument("newest", default=0)
@click.argument("oldest")
@click.argument("name")
def selective_download(name, oldest, newest):
    """Note: RSS feeds are counted backwards, default newest is 0, the most recent."""
    if six.PY3:
        name = name.encode("utf-8")
    feed = resolve_name(name)
    if six.PY3:
        feed = feed.decode()
    d = feedparser.parse(feed)
    logger.debug(d)
    try:
        d.entries[int(oldest)]
    except IndexError:
        print("Error feed does not contain this many items.")
        print("Hitman thinks there are %d items in this feed." % len(d.entries))
        return
    for url in [q.enclosures[0]['href'] for q in d.entries[int(newest):int(oldest)]]:
        # iterate over urls in feed from newest to oldest feed items.
        url = str(url)
        with Database("downloads") as db:
            if url.split('/')[-1] not in db:
                # download(url, name, feed)
                with Database("settings") as settings:
                    if 'dl' in settings:
                        dl_dir = settings['dl']
                    else:
                        dl_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                requests_get(url, dl_dir)


def resolve_name(name):
    """Takes a given input from a user and finds the url for it"""
    logger.debug("resolve_name: %s", name)
    with Database("feeds") as feeds, Database("aliases") as aliases:
        if name in aliases.keys():
            return feeds[aliases[name]]
        elif name in feeds.keys():
            return feeds[name]
        else:
            print("Cannot find feed named: %s" % name)
            return


def hitsquad(ctx):
    """'put a hit out' on all known rss feeds [Default action without arguements]"""
    with Database("feeds") as feeds:
        for name, feed in zip(list(feeds.keys()), list(feeds.values())):
            logger.debug("calling put_a_hit_out: %s", name)
            ctx.invoke(put_a_hit_out, name=name)
        if len(list(feeds.keys())) == 0:
            ctx.get_help()


def growl(text):
    """send a growl notification if on mac osx (use GNTP or the growl lib)"""
    if platform.system() == 'Darwin':
        import pync
        pync.Notifier.notify(text, title="Hitman")

    elif platform.system() == 'Linux':
        notified = False
        try:
            logger.debug("Trying to import pynotify")
            import pynotify
            pynotify.init("Hitman")
            n = pynotify.Notification("Hitman Status Report", text)
            n.set_timeout(pynotify.EXPIRES_DEFAULT)
            n.show()
            notified = True
        except ImportError:
            logger.debug("Trying notify-send")
            # print("trying to notify-send")
            if Popen(['which', 'notify-send'], stdout=PIPE).communicate()[0]:
                # Do an OSD-Notify
                # notify-send "Totem" "This is a superfluous notification"
                os.system("notify-send \"Hitman\" \"%r\" " % str(text))
                notified = True
        if not notified:
            try:
                logger.info("notificatons gnome gi???")
                import gi
                gi.require_version('Notify', '0.7')
                from gi.repository import Notify
                Notify.init("Hitman")
                # TODO have Icon as third argument.
                notification = Notify.Notification.new("Hitman", text)
                notification.show()
                Notify.uninit()
                notified = True
            except ImportError:
                logger.exception()
    elif platform.system() == 'Haiku':
        os.system("notify --type information --app Hitman --title 'Status Report' '%s'" % str(text))
    elif platform.system() == 'Windows':
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(text, "Hitman")
            # gntplib.publish("Hitman", "Status Update", "Hitman", text=text)
        except Exception:
            logger.exception()
            # print("Exception")
    else:
        pass
        # Can I test for growl for windows?


def requests_get(url, dl_dir):
    logger.debug("Sending HEAD req to %s", url)
    h = requests.head(url, allow_redirects=True)
    h.raise_for_status()
    save = os.path.join(dl_dir, url.split('/')[-1])
    logger.debug("headers: %s", h.headers)
    size = int(h.headers['content-length'])
    if os.path.exists(save) and 'accept-ranges' in h.headers:
        # http://stackoverflow.com/questions/12243997/how-to-pause-and-resume-download-work
        pass
        print("Cowardly refusing to resume %s" % save)
    else:
        print("Downloading: %s" % url.split('/')[-1])
        with progress.Bar(label="Download", expected_size=size) as bar, open(save, 'wb') as f:
            r = requests.get(url, stream=True)
            r.raise_for_status()
            counter = 0
            for chunk in r.iter_content(512):
                f.write(chunk)
                counter += len(chunk)
                bar.show(counter)


def add_feed(url):
    """add to db"""
    with Database("feeds") as db:
        title = feedparser.parse(url).feed.title
        name = str(title)
        db[name] = url
        return name


@cli_base.command("rm")
@click.argument("name")
def del_feed(name):
    """remove from database (and delete aliases)"""
    with Database("aliases") as aliases, Database("feeds") as feeds:
        if aliases[name]:
            proper_name = aliases[name]
        elif feeds[name]:
            proper_name = feeds[name]
        for k, v in aliases:
            if v == proper_name:
                del aliases[k]
        # deleted from aliases
        del feeds[proper_name]
        # deleted from feeds db


@cli_base.command("unalias")
@click.argument("alias")
def del_alias(alias):
    """sometimes you goof up."""
    with Database("aliases") as mydb:
        try:
            print("removing alias of %s to %s" % (alias, mydb.pop(alias)))
        except KeyError:
            print("No such alias key")
            print("Check alias db:")
            print(zip(list(mydb.keys()), list(mydb.values())))


@cli_base.command("alias")
@click.argument("alias")
@click.argument("name")
def alias_feed(name, alias):
    """write aliases to db"""
    with Database("aliases") as db:
        if alias in db:
            print("Something has gone horribly wrong with your aliases! Try deleting the %s entry." % name)
            return
        else:
            db[alias] = name


class Database(object):

    """Please use in a `with` context!"""

    def __init__(self, name):
        super(Database, self).__init__()
        try:
            self.db = semidbm.open(os.path.join(directory(), name), 'c')
        except NotADirectoryError:
            logger.error("Old database type encountered!")

    def __enter__(self):
        return self.db

    def __exit__(self, *args):
        self.db.close()


@cli_base.command("list")
def list_feeds():
    """List all feeds in plain text and give their aliases"""
    with Database("feeds") as feeds, Database("aliases") as aliases_db:
        for feed in feeds:
            name = feed
            url = feeds[feed]
            aliases = []
            for k, v in zip(list(aliases_db.keys()), list(aliases_db.values())):
                if v == name:
                    aliases.append(k)
            if aliases:
                print(name, " : %s Aliases: %s" % (url, aliases))
            else:
                print(name, " : %s" % url)


@cli_base.command("export")
def export_opml():
    """Export an OPML feed list"""
    with Database("feeds") as feeds:
        # Thanks to the canto project- used under the GPL
        print("""<opml version="1.0">""")
        print("""<body>""")
        # Accurate but slow.
        for name in list(feeds.keys()):
            kind = feedparser.parse(feeds[name]).version
            if kind[:4] == 'atom':
                t = 'pie'
            elif kind[:3] == 'rss':
                t = 'rss'
            print("""\t<outline text="%s" xmlUrl="%s" type="%s" />""" % (name, feeds[name], t))
        print("""</body>""")
        print("""</opml>""")
        # end canto refrenced code


@cli_base.command("import")
@click.argument("url")
def import_opml(url):
    """Import an OPML file locally or from a URL. Uses your text attributes as aliases."""
    # Test if URL given is local, then open, parse out feed urls,
    # add feeds, set text= to aliases and report success, list feeds added
    from bs4 import BeautifulSoup
    try:
        f = file(url).read()
    except IOError:
        f = requests.get(url).text
    soup = BeautifulSoup(f, "xml")
    links = soup.find_all('outline', type="rss" or "pie")
    # This is very slow, might cache this info on add
    for link in links:
        # print link
        add_feed(link['xmlUrl'])
        print("Added " + link['text'])


def is_feed(url):
    d = feedparser.parse(url)
    if d.bozo and d.bozo_exception:
        print("feedparser has declared this feed a bozo:")
        print(d.bozo_exception)
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


@cli_base.command()
@click.option("--force", is_flag=True, default=False)
@click.argument("url")
def add(url, force=False):
    """Add a atom or RSS feed by url.
    If it doesn't end in .atom or .rss we'll do some guessing."""
    if url[-3:] == 'xml' or url[1][-4:] == 'atom':
        print("Added your feed as %s" % str(add_feed(url)))
    elif is_feed(url):
        print("Added your feed as %s" % str(add_feed(url)))
    elif force:
        print("Added your feed as %s" % str(add_feed(url)))
    else:
        print("Hitman doesn't think that url is a feed; if you're sure it is rerun with --force")


@cli_base.command("set")
@click.argument("value", default=False)
@click.argument("key")
def set_settings(key, value):
    """Set Hitman internal settings."""
    with Database("settings") as settings:
        if value in ['0', 'false', 'no', 'off', 'False']:
            del settings[key]
            print("Disabled setting")
        else:
            print(value)
            settings[key] = value
            print("Setting saved")


@cli_base.command("config")
@click.argument("key", required=False)
@click.option("--all", is_flag=True)
def get_settings(all,key):
    """View Hitman internal settings. Use 'all' for all keys"""
    with Database("settings") as s:
        if all:
            for k, v in zip(list(s.keys()), list(s.values())):
                print("{} = {}".format(k, v))
        elif key:
            print("{} = {}".format(key, s[key]))
        else:
            print("Don't know what you want? Try --all")


if __name__ == "__main__":
    cli_base() # noqa
