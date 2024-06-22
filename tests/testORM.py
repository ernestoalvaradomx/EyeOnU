import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from src.frameprocessing.models.userTestModel import User
from src.util.database.db import db

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
        
    def test_home_200(self):
        response = self.app.get('/test-ORM/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Home')

    def test_listUser_200(self):
        response = self.app.get('/test-ORM/users')
        self.assertEqual(response.status_code, 200)

    def test_getUser_200(self):
        response = self.app.get('/test-ORM/users/2')
        self.assertEqual(response.status_code, 200)

    def test_createUser_200(self):
        newUser = User(name="Julieta", 
                       lastName="Estrada",
                       age=22)
        response = self.app.post('/test-ORM/users', json=newUser.toJson())
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], f"User {newUser.name} has been created successfully.")

if __name__ == '__main__':
    unittest.main()
