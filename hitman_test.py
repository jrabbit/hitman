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
