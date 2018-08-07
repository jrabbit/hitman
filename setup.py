from setuptools import setup
setup(
    name='hitman',
    version='1.2b4',
    author='Jack Laxson',
    author_email='jackjrabbit+hitman@gmail.com',
    url='https://github.com/jrabbit/hitman',
    license='GPL v3',
    long_description="Hitman: The professional RSS enclosure (Podcast) downloader. Supports OPML. Supports various downloads methods: requests and urlgrabber (pycurl based).",
    description="The professional RSS enclosure (Podcast) downloader.",
    scripts=['hitman.py'],
    install_requires=['semidbm', 'requests', 'clint', 'six',
                      'feedparser>=5.1.3', 'beautifulsoup4>=4.3.2', 'click>=6'],
    extras_require={'platform_system=="Windows"':["win10toast"]},
    entry_points='''
        [console_scripts]
        hitman=hitman:cli_base
    ''',
    classifiers=['Environment :: Console',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Topic :: Internet :: WWW/HTTP', 'Operating System :: BeOS',
                 'Topic :: Multimedia', 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.6' ]
)
