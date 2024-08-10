import cv2
from src.models.rawFrameModel import RawFrame

from PIL import Image
import matplotlib.pyplot as plt
import os
from datetime import datetime
from io import BytesIO


FILE_NAME='src/prueba_frames/captured_frame.jpg'
ONLINE_STREAM="rtsp://rtspstream:fd4cb722051a235e5a8605a663beedf3@zephyr.rtsp.stream/movie"
LOCAL_STREAM="rtsp://localhost:8554/live.stream"

def capture_frame(id_cam):
    camara = cv2.VideoCapture(id_cam)
    if not camara.isOpened():
        raise Exception("Error: Could not open camara.")
    ret, frame = camara.read()
    if not ret:
        raise Exception("Error: Failed to capture frame.")
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
    raw_frame = RawFrame(frame_bytes)
    # Guarda los bytes del frame en un archivo
    with open(FILE_NAME, 'wb') as f:
        f.write(frame_bytes)
    return raw_frame

def main():
    frame = capture_frame(LOCAL_STREAM)
    print(frame)

    # Verificar la existencia de captured_frame.jpg antes de abrirlo
    filename = FILE_NAME
    if os.path.exists(filename):
        # Mostrar la imagen usando matplotlib
        plt.imshow(Image.open(BytesIO(frame.pixels)))
        plt.title(f'Creation Time: {frame.creation_time}')
        plt.axis('off')  # Desactiva los ejes
        plt.show()
    else:
        print(f"Error: El archivo '{filename}' no se encontró en la ubicación especificada.")

if __name__ == "__main__":
    main()
