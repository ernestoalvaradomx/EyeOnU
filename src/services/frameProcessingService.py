import json
from PIL import Image, ImageDraw
import io
import os
import requests
import hashlib

from sqlalchemy import Null
from src.models.rawFrameModel import RawFrame
from src.models.sightingModel import Sighting
from src.models.frameModel import Frame
from src.util.aws import rekognition
from src.util.gemini import model

# def plotBoundingBoxes(img, objectAndPositions):
#     width, height = img.size
#     # print(img.size)

#     # Create a drawing object
#     draw = ImageDraw.Draw(img)

#     # Define a list of colors
#     # colors = ['blue']

#     # Iterate over the noun phrases and their positions
#     for i, (object, (y1, x1, y2, x2)) in enumerate(
#         objectAndPositions):
#         if object != 'objects':
#           # Select a color from the list
#           # color = colors[i % len(colors)]
#           color = 'orange'

#           # Convert normalized coordinates to absolute coordinates
#           absX1 = int((x1 / 1000) * width)
#           absY1 = int((y1 / 1000) * height)
#           absX2 = int((x2 / 1000) * width)
#           absY2 = int((y2 / 1000 )* height)

#           # print(abs_x1, abs_y1, abs_x2, absY2)

#           # Draw the bounding box
#           draw.rectangle(
#               ((absX1, absY1), (absX2, absY2)), outline=color, width=4
#           )

#           # Draw the text
#           draw.text((absX1 + 8, absY1 + 8), object, fill=color)

#     return img

def boxesWithLabel(text: str) -> dict:
  text = text.split("```\n")[0]
  return json.loads(text.strip("```").strip("python").strip("json").replace("'", '"').replace('\n', '').replace(',}', '}'))

def getNormalizedCoordinates(img, coordinates: list[str]) -> list[int]:
    width, height = img.size

    coordinates = [int(x) for x in coordinates]

    # Convert normalized coordinates to absolute coordinates
    absX1 = int((coordinates[1] / 1000) * width)
    absY1 = int((coordinates[0] / 1000) * height)
    absX2 = int((coordinates[3] / 1000) * width)
    absY2 = int((coordinates[2] / 1000 )* height)

    return [absX1, absY1, absX2, absY2]

def hashImage(imgBytes: bytes) -> str:
    hashMD5 = hashlib.md5()
    hashMD5.update(imgBytes)
    hashMD5 = hashMD5.hexdigest()
    # print(hashMD5)

    return hashMD5

def deleteFace(FaceId: str) -> dict:
    return rekognition.delete_faces(
            CollectionId='individualFaces',
            FaceIds=[FaceId]
        )

def uploadFace(img: Image, sighting: Sighting) -> Sighting:
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        imgBytes = output.getvalue()

    response = rekognition.index_faces(
        CollectionId='individualFaces',
        Image={'Bytes': imgBytes},
        ExternalImageId=hashImage(imgBytes),
        DetectionAttributes=['ALL']
    )

    sighting.collection_id = response['FaceRecords'][0]['Face']['FaceId']

    return sighting

def faceRekognition(img: Image, sighting: Sighting) -> Sighting:
    img = img.crop(sighting.face_coordinates)
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        imgBytes = output.getvalue()

    response = rekognition.search_faces_by_image(
        CollectionId='individualFaces',
        Image={'Bytes': imgBytes},
        MaxFaces=1,
        FaceMatchThreshold=95
    )

    if response['FaceMatches']:
        matchFace = response['FaceMatches'][0]
        id = matchFace['Face']['FaceId']
        similarity = matchFace['Similarity']
        # print("id: ", id, "similarity: ", similarity)

        sighting.collection_id = id
    else:
        # print("no se encontro ninguna coincidencia")
        sighting = uploadFace(img, sighting)

    return sighting

def freameProcessing(rawFrame: RawFrame) -> Frame:
    img = Image.open(io.BytesIO(rawFrame.pixels))
    response = model.generate_content([
        img,
        (
            "Detect people and their faces and dangerous objects in their"
            " hands. When you reference an object put its name and"
            " bounding box in the format: {'people': [{'person':"
            " [y_min, x_min, y_max, x_max],'face': [y_min, x_min,"
            " y_max, x_max],'dangerousObject': [y_min, x_min, y_max,"
            " x_max]]} in format .json"
        ),
    ])
    # print(response.text)

    responseDic = boxesWithLabel(response.text)

    sightings = []
    if len(responseDic['people']) <= 0:
        # print("there are not people in the image")
        return Frame(sightings=sightings)
        
    for o in responseDic['people']:
        sighting = Sighting(id=Null, frame_id=Null, individual_id=Null, collection_id=Null, 
                            body_coordinates=Null, face_coordinates=Null, object_coordinates=Null)
        sighting.body_coordinates = getNormalizedCoordinates(img, o['person'])
        sighting.face_coordinates = getNormalizedCoordinates(img, o['face'])
        if len(o['dangerousObject']) > 0:
            # print("danger")
            sighting.object_coordinates = getNormalizedCoordinates(img, o['dangerousObject'])
        sightings.append(faceRekognition(img, sighting))

    frame = Frame()
    frame.sightings = sightings
    return frame