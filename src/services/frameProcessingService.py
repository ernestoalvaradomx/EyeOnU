import json
from PIL import Image, ImageDraw
import io
import os
import requests
import hashlib
import botocore

from sqlalchemy import Null
from src.models.rawFrameModel import RawFrame
from src.models.sightingModel import Sighting
from src.models.frameModel import Frame
from src.util.aws import rekognition
from src.util.gemini import model

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

def deleteFace(faceIdList: list[str]) -> dict:
    return rekognition.delete_faces(
            CollectionId='individualFaces',
            FaceIds=faceIdList
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
    # print(response)

    if len(response['FaceRecords']) == 0:
        print(response['UnindexedFaces'][0]['Reasons'])
        return sighting

    sighting.collection_id = response['FaceRecords'][0]['Face']['FaceId']

    return sighting

def faceRekognition(img: Image, sighting: Sighting) -> Sighting:
    img = img.crop(sighting.face_coordinates)
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        imgBytes = output.getvalue()

    try:
        response = rekognition.search_faces_by_image(
            CollectionId='individualFaces',
            Image={'Bytes': imgBytes},
            MaxFaces=1,
            FaceMatchThreshold=95
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidParameterException' and 'no faces in the image' in e.response['Error']['Message']:
            # print("no se encontraron caras en la imagen")
            return sighting
        
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
            " x_max] or []]}. If you don't find a dangerous object," 
            " leave 'dangerousObject' as an empty list ([])." 
            " The output should be in JSON format."
        ),
    ])
    print(response.text)

    responseDic = boxesWithLabel(response.text)

    sightings = []
    if len(responseDic['people']) <= 0:
        # print("there are not people in the image")
        return Frame(sightings=sightings)
        
    for o in responseDic['people']:
        sighting = Sighting(frame_id=Null, individual_id=Null, collection_id=Null, 
                            body_coordinates=Null, face_coordinates=Null, object_coordinates=[])
        sighting.body_coordinates = getNormalizedCoordinates(img, o['person'])
        sighting.face_coordinates = getNormalizedCoordinates(img, o['face'])
        if len(o['dangerousObject']) > 0:
            # print("danger")
            sighting.object_coordinates = getNormalizedCoordinates(img, o['dangerousObject'])

        sighting = faceRekognition(img, sighting)
        if sighting.collection_id != Null:
            sightings.append(sighting)
    
    if len(sightings) == 0:
        return Frame(sightings=sightings)

    frame = Frame()
    frame.sightings = sightings
    return frame