import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from unittest.mock import patch

class TestHomeViewBackend(unittest.TestCase):

    def setUp(self): # Se ejecuta al iniciar cada prueba
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self): # Se ejecuta al finalizar cada prueba
        pass

    def test_listInvividual_200(self):
        response = self.app.get('/home-view/individuals')
        self.assertEqual(response.status_code, 200)

    def test_listAlert_200(self):
        response = self.app.get('/home-view/alerts')
        self.assertEqual(response.status_code, 200)

    def test_listIncident(self):
        data = {"idIndividual": 3}
        response = self.app.get('/home-view/incidents', json=data)
        self.assertEqual(response.status_code, 200)

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_createIncident(self, mock_add, mock_commit):
        data = {
            "idAlert": 76,
            "idUser": 1
        }
        response = self.app.post('/home-view/incident', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["response"], True)

if __name__ == '__main__':
    unittest.main()
