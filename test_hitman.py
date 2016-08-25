import unittest
import tempfile
import shutil
import os
from StringIO import StringIO

import mock
import pxml

from hitman import Database, requests_get, baker, list_feeds, export_opml, import_opml

# class TestDatabase(unittest.TestCase):
#     d = {'data': 'value', 'cheese': 'many'}

#     def setUp(self):
#         self.mydb = Database("test")
#         self.mydb.db['data'] = 'value'
#         self.mydb.db['cheese'] = 'many'
#         # self.mydb.db.update(self.d) # doesn't fucking work on travis
#         # option to use `semidbm`
#         # self.mydb.db.sync()

#     def test_write(self):
#         self.assertEqual(dict(self.mydb.db), self.d)

#     def test_with(self):
#         with Database("test") as db:
#             db.update(self.d)
#             self.assertEqual(db, self.d)

#     def tearDown(self):
#         self.mydb.db.clear()
#         self.mydb.db.close()


class ClosableDict(dict):
    """a thin shim to make the tests run"""
    def __init__(self, *args, **kwargs):
        super(ClosableDict, self).__init__(*args, **kwargs)
    def close(self):
        pass

class TestOPML(unittest.TestCase, pxml.XmlTestMixin):
    outOPML ="""<opml version="1.0">
<body>
    <outline text="Democracy Now! Video" xmlUrl="http://www.democracynow.org/podcast-video.xml" type="rss" />
</body>
</opml>
"""
    inOPML =""""""
    opml_file = "fixtures/example.opml"

    @mock.patch('semidbm.open')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_export(self, patched_stdout, patched_dbm):
        our_d = ClosableDict()
        our_d["Democracy Now! Video"] = "http://www.democracynow.org/podcast-video.xml"
        patched_dbm.return_value = our_d
        export_opml()
        patched_dbm.assert_called()
        out = patched_stdout.getvalue()
        self.assertXmlEqual(out, self.outOPML)
        # print(patched_stdout.getdata())

    @mock.patch('hitman.add_feed')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_import(self, patched_stdout, patched_add):
        import_opml(self.opml_file)
        patched_add.asser_called_once_with("http://www.democracynow.org/podcast.xml")
        self.assertEqual(patched_stdout.getvalue(), "Added Democracy Now! Audio\n")


class TestList(unittest.TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('semidbm.open')
    def test_list(self, patched_dbm, patched_stdout):
        our_d = ClosableDict()
        our_d["Democracy Now! Video"] = "http://www.democracynow.org/podcast-video.xml"
        patched_dbm.return_value = our_d
        list_feeds()
        out = patched_stdout.getvalue()
        # print(out)

class TestCalls(unittest.TestCase):
    def test_main(self):
        func = baker.test()
        self.assertEqual(func, "hitsquad()")
        
    def test_main_args(self):
        baker.test(['s', 'add'])


class TestDownloaders(unittest.TestCase):
    def setUp(self):
        self.dest = tempfile.mkdtemp()

    @mock.patch("clint.textui.progress.Bar")
    def test_requests_get(self, patched_bar):
        url = "https://httpbin.org/image/png"
        requests_get(url, self.dest)
        f = os.path.join(self.dest, 'png')
        self.assertTrue(os.path.exists(f))
    def test_requests_resume(self):
        pass
    def tearDown(self):
        shutil.rmtree(self.dest)

