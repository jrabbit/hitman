Hitman.
=======
The professional RSS enclosure downloader.
-------------------------------------------
![build status](https://api.travis-ci.org/jrabbit/hitman.svg) ![published version](https://img.shields.io/pypi/v/hitman.svg)


+   Should run on recent python (2.7.x or 3-3.6+)
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
