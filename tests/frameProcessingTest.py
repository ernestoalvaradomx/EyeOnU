import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import requests
from app import app
from src.services.frameProcessingService import freameProcessing, deleteFace
from dotenv import load_dotenv
from src.models.rawFrameModel import RawFrame
from sqlalchemy import Null

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        load_dotenv()

    def setUp(self): # Se ejecuta al iniciar cada prueba
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self): # Se ejecuta al finalizar cada prueba
        pass  
        
    def test_home_200(self):
        response = self.app.get('/frame-processing/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Home')

    def test_freameProcessing_200(self):
        url = 'https://e00-elmundo.uecdn.es/assets/multimedia/imagenes/2024/04/23/17138798885408.jpg'
        img = requests.get(url).content
        data = freameProcessing(RawFrame(pixels=img, creationTime=Null))

        self.assertEqual(data.sightings[0].collection_id, '13996c4e-0c81-46f1-88d4-7082441b3408')

    def test_freameProcessingUploadFace_200(self):
        url = 'https://mx.web.img3.acsta.net/c_310_420/pictures/15/05/15/16/30/134942.jpg'
        img = requests.get(url).content
        data = freameProcessing(RawFrame(pixels=img, creationTime=Null))

        print(data.sightings[0].collection_id)
        
        response = deleteFace(data.sightings[0].collection_id)
        self.assertEqual(response['DeletedFaces'], [data.sightings[0].collection_id])

if __name__ == '__main__':
    unittest.main()
