import os
import json

import feedparser
import hitman

#get hitman directory
#hitman.directory()

def is_file_latest(file, url):
    d = feedparser.parse(url)
    # print d,url,file
    if d.entries[0].enclosures:
        if file == d.entries[0].enclosures[0]['href'].split('/')[-1]:
            return True
        else:
            return False

def clean_downloads():
    settings = hitman.get_settings()
    if 'dl' in settings:
       dl_dir = settings['dl']
    else:
       dl_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    listing = os.listdir(dl_dir)
    for localfile,data in  hitman.get_downloads().iteritems():
       # db[localfile] = JSON obj {'url': url,
       # 'date': time.ctime(), 'feed': feed_url}
       if localfile in listing:
           values = json.loads(data)
           #check if file is the latest
           if is_file_latest(localfile, values['feed']):
               pass
           else:
               os.remove(os.path.join(dl_dir, localfile))    


if __name__ == "__main__":
   clean_downloads()
