import unittest

from hitman import Database


class TestDatabase(unittest.TestCase):
    d = {'data': 'value', 'cheese': 'many'}

    def setUp(self):
        self.mydb = Database("test")
        self.mydb.db.update(self.d)

    def test_write(self):
        self.assertEqual(self.mydb.db, self.d)

    def test_with(self):
        with Database("test") as db:
            db.update(self.d)
            self.assertEqual(db, self.d)

    def tearDown(self):
        self.mydb.db.clear()
        self.mydb.db.close()

class TestOPML(unittest.TestCase):
    outOPML ="""<opml version="1.0">
<body>
    <outline text="Democracy Now! Video" xmlUrl="http://www.democracynow.org/podcast-video.xml" type="rss" />
</body>
</opml>
"""
    inOPML =""""""
    def setUp(self):
        pass
    def test_export(self):
        pass
    def test_import(self):
        pass
    def tearDown(self):
        pass