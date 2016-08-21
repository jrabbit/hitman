from setuptools import setup
setup(
    name='hitman',
    version='1.2b1',
    author='Jack Laxson',
    author_email='jackjrabbit+hitman@gmail.com',
    url='https://github.com/jrabbit/hitman',
    license='GPL v3',
    long_description="Hitman: The professional RSS enclosure (Podcast) downloader. Supports OPML. Supports various downloads methods: requests and urlgrabber (pycurl based).",
    description="The professional RSS enclosure (Podcast) downloader.",
    scripts= ['hitman.py'],
    install_requires=['requests', 'clint', 'feedparser>=5.1.3', 'beautifulsoup4>=4.3.2', 'baker==1.3'],
    classifiers=['Environment :: Console', 
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 
    'Topic :: Internet :: WWW/HTTP', 'Operating System :: BeOS',
    'Topic :: Multimedia', 'Operating System :: OS Independent', 'Programming Language :: Python :: 2 :: Only',
    'Programming Language :: Python :: 2.7', ]
)

