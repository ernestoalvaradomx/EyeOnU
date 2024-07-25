import unittest
import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from dotenv import load_dotenv
from sqlalchemy import Null

from src.services.frameProcessingService import freameProcessing, deleteFace

from src.models.rawFrameModel import RawFrame

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        load_dotenv()

    def setUp(self): # Se ejecuta al iniciar cada prueba
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self): # Se ejecuta al finalizar cada prueba
        pass  

    def test_freameProcessing_200(self):
        url = 'https://e00-elmundo.uecdn.es/assets/multimedia/imagenes/2024/04/23/17138798885408.jpg'
        img = requests.get(url).content
        data = freameProcessing(RawFrame(pixels=img))

        self.assertEqual(data.sightings[0].collection_id, '13996c4e-0c81-46f1-88d4-7082441b3408')

    def test_freameProcessingUploadFace_200(self):
        url = 'https://mx.web.img3.acsta.net/c_310_420/pictures/15/05/15/16/30/134942.jpg'
        img = requests.get(url).content
        data = freameProcessing(RawFrame(pixels=img))

        # print(data.sightings[0].collection_id)
        
        response = deleteFace([data.sightings[0].collection_id])
        self.assertEqual(response['DeletedFaces'], [data.sightings[0].collection_id])

    def test_freameProcessingDangerousObject_200(self):
        url = 'https://es.web.img3.acsta.net/r_1280_720/medias/nmedia/18/70/46/05/19119896.jpg'
        img = requests.get(url).content
        data = freameProcessing(RawFrame(pixels=img))

        # print("len: ", len(data.sightings))

        dangerousObject = any(sighting.object_coordinates for sighting in data.sightings if sighting.object_coordinates)
        self.assertEqual(True, dangerousObject)
        
        faceIdList = [sighting.collection_id for sighting in data.sightings]
        response = deleteFace(faceIdList)
        self.assertEqual(response['DeletedFaces'], faceIdList)

if __name__ == '__main__':
    unittest.main()