from distutils.core import setup
setup(
    name='hitman',
    version='1.0dev',
    author='jrabbit',
    author_email='jackjrabbit+hitman@gmail.com',
    url='https://github.com/jrabbit/hitman',
    license='GPL v3',
    long_description="Hitman: The professional RSS enclosure downloader. Supports OPML. Supports various downloads methods: system wget, system curl, urlgrabber (pycurl based).",
    py_modules = ['BeautifulSoup', 'feedparser'],
    scripts= ['hitman.py'],
    packages=['urlgrabber'],
    requires=['pycurl'],
    classifiers=['Environment :: Console', 'License :: OSI Approved :: GNU General Public License (GPL)', 'Topic :: Internet :: WWW/HTTP']
)