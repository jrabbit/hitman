import os
import shutil
import tempfile
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import pxml
import six
from click.testing import CliRunner
from hitman import Database, export_opml, requests_get


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
    outOPML =b"""<opml version="1.0">
<body>
    <outline text="Democracy Now! Video" xmlUrl="http://www.democracynow.org/podcast-video.xml" type="rss" />
</body>
</opml>
"""
    inOPML =""""""

    @mock.patch('semidbm.open')
    def test_export(self, patched_dbm):
        our_d = ClosableDict()
        our_d["Democracy Now! Video"] = "http://www.democracynow.org/podcast-video.xml"
        patched_dbm.return_value = our_d
        runner = CliRunner()
        result = runner.invoke(export_opml)

        self.assertXmlEqual(result.output.encode("utf-8"), self.outOPML)

    def test_import(self):
        pass

# class TestCalls(unittest.TestCase):
#     def test_main(self):
#         func = baker.test()
#         self.assertEqual(func, "hitsquad()")
        
#     def test_main_args(self):
#         baker.test(['s', 'add'])


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



if __name__ == '__main__':
    unittest.main()
