import cv2
import numpy as np
import requests

from urllib.request import urlopen
from urllib.error import URLError

from src.models.rawFrameModel import RawFrame

class RawFrameService:
    @staticmethod
    def captureFrame(id_cam) -> RawFrame:
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