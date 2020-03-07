Hitman.
=======
The professional RSS enclosure downloader.
-------------------------------------------
[![Build Status](https://travis-ci.com/jrabbit/hitman.svg?branch=dev)](https://travis-ci.com/jrabbit/hitman)
[![published version](https://img.shields.io/pypi/v/hitman.svg)](https://pypi.org/project/hitman/)
[![codecov](https://codecov.io/gh/jrabbit/hitman/branch/master/graph/badge.svg)](https://codecov.io/gh/jrabbit/hitman)



+   Should run on recent python (3.7+)
+   Lets you reference feeds based on user defined aliases [ex: "trms", "maddow"]
+   Supports OPML.
+   Tells you when a download is done (OSD-notify, send-notify, Win10 Notifications, Haiku OS, Opt-in terminal bell)
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

Import your RSS feeds (via OPML)
`hitman.py import myfeeds.opml`

[Full docs at rtd.](https://hitman.readthedocs.io/en/latest/)
