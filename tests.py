import json
import unittest
from server import test_mode, db, app

TODO_TITLE = 'todo1'
TODO_TITLE2 = 'todo2'


class TodoTest(unittest.TestCase):
    def setUp(self):
        self.app = test_mode()
        self.client = self.app.test_client

        with self.app.app_context():
            db.init_app(app)
            db.create_all()

    def test_create_and_read(self):
        self.client().put('/create', data=json.dumps(dict(title=TODO_TITLE)), content_type='application/json')
        self.client().put('/create', data=json.dumps(dict(title=TODO_TITLE2)), content_type='application/json')
        res = self.client().get('/items')
        data = json.loads(res.data).get('content')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].get('title'), TODO_TITLE)
        self.assertEqual(data[1].get('title'), TODO_TITLE2)

    def test_update(self):
        self.client().put('/create', data=json.dumps(dict(title=TODO_TITLE)), content_type='application/json')
        self.client().put('/update/1')
        res = self.client().get('/items')
        data = json.loads(res.data).get('content')
        self.assertEqual(data[0].get('done'), True)

    def test_delete(self):
        self.client().put('/create', data=json.dumps(dict(title=TODO_TITLE)), content_type='application/json')
        self.client().put('/create', data=json.dumps(dict(title=TODO_TITLE2)), content_type='application/json')
        res = self.client().get('/items')
        data = json.loads(res.data).get('content')
        self.assertEqual(len(data), 2)
        self.client().delete('/delete/1')
        res2 = self.client().get('/items')
        data2 = json.loads(res2.data).get('content')
        self.assertEqual(len(data2), 1)
        self.assertEqual(data2[0].get('title'), TODO_TITLE2)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
