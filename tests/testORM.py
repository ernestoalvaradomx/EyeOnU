import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from unittest.mock import patch
from src.models.userTestModel import UserTest

class TestORM(unittest.TestCase):

    def setUp(self): # Se ejecuta al iniciar cada prueba
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self): # Se ejecuta al finalizar cada prueba
        pass  
        
    def test_home_200(self):
        response = self.app.get('/test-ORM/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Home')

    def test_listUser_200(self):
        response = self.app.get('/test-ORM/users')
        self.assertEqual(response.status_code, 200)

    def test_getUser_200(self):
        response = self.app.get('/test-ORM/users/1')
        self.assertEqual(response.status_code, 201)

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_createUser_200(self, mock_add, mock_commit):
        newUser = UserTest(name="Julieta", 
                       lastName="Estrada",
                       age=22)
        response = self.app.post('/test-ORM/users', json=newUser.toJson())
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], f"User {newUser.name} has been created successfully.")

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_updateUser_200(self, mock_add, mock_commit):
        updateUser = UserTest(name="Leo", 
                       lastName="Llera",
                       age=23)
        response = self.app.put('/test-ORM/users/1', json=updateUser.toJson())
        data = response.get_json()
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], f"User {updateUser.name} has been updated successfully.")

    @patch('app.db.session.delete')
    @patch('app.db.session.commit')
    def test_deleteUser_200(self, mock_add, mock_commit):
        response = self.app.delete('/test-ORM/users/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "User has been deleted successfully.")

if __name__ == '__main__':
    unittest.main()
