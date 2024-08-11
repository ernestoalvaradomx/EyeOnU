import cv2
from src.models.rawFrameModel import RawFrame

from src.services.rawFrameService import RawFrameService
from PIL import Image
import matplotlib.pyplot as plt
import os
from datetime import datetime
from io import BytesIO


FILE_NAME='src/prueba_frames/captured_frame.jpg'
ONLINE_STREAM="rtsp://rtspstream:fd4cb722051a235e5a8605a663beedf3@zephyr.rtsp.stream/movie"
LOCAL_STREAM="rtsp://localhost:8554/live.stream"

def main():
    frame = RawFrameService.captureFrame(LOCAL_STREAM)
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
