from setuptools import setup
setup(
    name='hitman',
    version='1.2a4',
    author='jrabbit',
    author_email='jackjrabbit+hitman@gmail.com',
    url='https://github.com/jrabbit/hitman',
    license='GPL v3',
    long_description="Hitman: The professional RSS enclosure (Podcast) downloader. Supports OPML. Supports various downloads methods: requests and urlgrabber (pycurl based).",
    description="The professional RSS enclosure (Podcast) downloader.",
    scripts= ['hitman.py'],
    install_requires=['pycurl>=7.19.5.1', 'feedparser>=5.1.3', 'beautifulsoup4>=4.3.2', 'baker==1.3', 'gntplib>=0.5'],
    classifiers=['Environment :: Console', 
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 
    'Topic :: Internet :: WWW/HTTP', 'Operating System :: BeOS',
    'Topic :: Multimedia', 'Operating System :: OS Independent', 'Programming Language :: Python :: 2 :: Only',
    'Programming Language :: Python :: 2.7', ]
)

