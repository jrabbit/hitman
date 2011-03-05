from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup
setup(
    name='hitman',
    version='1.0.1dev',
    author='jrabbit',
    author_email='jackjrabbit+hitman@gmail.com',
    url='https://github.com/jrabbit/hitman',
    license='GPL v3',
    long_description="Hitman: The professional RSS enclosure downloader. Supports OPML. Supports various downloads methods: system wget, system curl, urlgrabber (pycurl based).",
    scripts= ['hitman.py'],
    packages=['urlgrabber'],
    install_requires=['pycurl', 'feedparser', 'BeautifulSoup'],
    classifiers=['Environment :: Console', 'License :: OSI Approved :: GNU General Public License (GPL)', 'Topic :: Internet :: WWW/HTTP', 'Operating System :: BeOS','Topic :: Multimedia' ]
)

