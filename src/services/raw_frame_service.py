import cv2
from models import RawFrame
class RawFrameService:
    @staticmethod
    def capture_frame(id_cam ):
        camara = cv2.VideoCapture(id_cam)
        if not camara.isOpened():
            raise Exception("Error: Could not open camara.")
        ret, frame = camara.read() 
        if not ret:
            raise Exception("Error: Failed to capture frame.")
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        raw_frame = RawFrame(bytes=frame_bytes)
        return raw_frame

