import cv2
import numpy as np
import requests

from urllib.request import urlopen
from urllib.error import URLError

from src.models.rawFrameModel import RawFrame

class RawFrameService:
    def __init__(self):
        self.imageTestId = 0
        self.urls = [
            'https://images.mubicdn.net/images/film/25580/cache-33736-1568750405/image-w1280.jpg?size=800x',
            'https://media.glamour.mx/photos/6660c97a58a6da682679023d/16:9/w_2560%2Cc_limit/bad-boys-con-will-smith-fecha-de-estreno.jpg',
            'https://i.ytimg.com/vi/r7jbePATC-U/maxresdefault.jpg'
        ]
        self.rawFrameList = self.getImagesTest()

    def getImagesTest(self) -> list[RawFrame]:
        rawFrameList = []
        for url in self.urls:
            img = requests.get(url).content
            rawFrameList.append(RawFrame(pixels=img))
        return rawFrameList
    
    def captureFrameTest(self) -> RawFrame:
        rawFrame = self.rawFrameList[self.imageTestId]
        self.imageTestId += 1
        if self.imageTestId >= len(self.urls):
            self.imageTestId = 0
        return rawFrame

    @staticmethod
    def capture_frame(id_cam) -> RawFrame:
        if id_cam is None:
            id_cam = 0  # Si id_cam no está definido, se usa la cámara por defecto (índice 0)

        try:
            # Intentar abrir id_cam como una URL
            if isinstance(id_cam, str):
                camara = urlopen(id_cam, timeout=10)  # Ajusta el timeout según necesites
                bytes = bytearray(camara.read())
                frame = cv2.imdecode(np.asarray(bytes), cv2.IMREAD_COLOR)
            else:
                # Si no es una cadena, asumimos que es un número de cámara local
                camara = cv2.VideoCapture(int(id_cam))
                if not camara.isOpened():
                    raise Exception("Error: Could not open camera.")
                ret, frame = camara.read()
                if not ret:
                    raise Exception("Error: Failed to capture frame.")

        except (URLError, ValueError):
            # Manejar excepciones al abrir la URL o si id_cam no es convertible a int
            raise Exception("Error: Could not open camera or invalid id_cam.")

        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        raw_frame = RawFrame(pixels=frame_bytes)
        return raw_frame