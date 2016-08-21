import unittest
import tempfile
import shutil
import os
from StringIO import StringIO

import mock
import pxml

from hitman import Database, requests_get, baker, export_opml

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

class TestOPML(unittest.TestCase, pxml.XmlTestMixin):
    outOPML ="""<opml version="1.0">
<body>
    <outline text="Democracy Now! Video" xmlUrl="http://www.democracynow.org/podcast-video.xml" type="rss" />
</body>
</opml>
"""
    inOPML =""""""

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_export(self, patched_stdout):
        export_opml()
        out = patched_stdout.getvalue()
        self.assertXmlEqual(out, self.outOPML)
        # print(patched_stdout.getdata())
    def test_import(self):
        pass

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

