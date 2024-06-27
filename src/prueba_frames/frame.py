import cv2
from src.models.rawFrameModel import RawFrame

from PIL import Image
import matplotlib.pyplot as plt
import os

def capture_frame(id_cam):
    camara = cv2.VideoCapture(id_cam)
    if not camara.isOpened():
        raise Exception("Error: Could not open camara.")
    ret, frame = camara.read()
    if not ret:
        raise Exception("Error: Failed to capture frame.")
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
    raw_frame = RawFrame(id=1, pixels=frame_bytes)
    # Guarda los bytes del frame en un archivo
    with open('captured_frame.jpg', 'wb') as f:
        f.write(frame_bytes)
    return raw_frame

def main():
    frame = capture_frame(0)
    print(frame.to_dict())

    # Verificar la existencia de captured_frame.jpg antes de abrirlo
    filename = 'captured_frame.jpg'
    if os.path.exists(filename):
        # Mostrar la imagen usando PIL (Pillow)
        imagen = Image.open(filename)
        imagen.show()

        # Mostrar la imagen usando matplotlib
        plt.imshow(frame.pixels)
        plt.title(f'Creation Time: {frame.creation_time}')
        plt.axis('off')  # Desactiva los ejes
        plt.show()
    else:
        print(f"Error: El archivo '{filename}' no se encontró en la ubicación especificada.")

if __name__ == "__main__":
    main()
