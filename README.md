Hitman.
=======
The professional RSS enclosure downloader.
-------------------------------------------
![build status](https://api.travis-ci.org/jrabbit/hitman.svg) ![published version](https://img.shields.io/pypi/v/hitman.svg) [![Code Health](https://landscape.io/github/jrabbit/hitman/master/landscape.svg?style=flat)](https://landscape.io/github/jrabbit/hitman/master)


+   Should run on recent python (2.7.x or 3-3.6)
+   Lets you reference feeds based on user defined aliases [ex: "trms", "maddow"]
+   Supports OPML.
+   Supports various download methods: requests, urlgrabber (pycurl based)
+   Cross-platform folder support, progress meter for UNIX operating systems, but only works on windows if you enable Termios support.
+   Tells you when a download is done (OSD-notify, Growl, Growl for Windows)
+   A fun assassin theme

![hitman jacket](http://upload.wikimedia.org/wikipedia/en/7/76/Hit_mancons.jpg)

Basic usage
-----------

Add a feed.
`hitman.py add http://www.democracynow.org/podcast-video.xml`

Alias it.
`hitman.py alias "Democracy Now! Video" dn`

Download latest enclosures (episodes) of every feed.
`hitman.py`

Import your RSS feeds (via [OPML](http://support.google.com/reader/bin/answer.py?hl=en&answer=70572))
`hitman.py import myfeeds.opml`
