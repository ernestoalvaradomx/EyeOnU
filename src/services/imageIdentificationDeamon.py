import threading
import time
import io

from flask import Flask
from datetime import datetime
from PIL import Image

from src.util.database.db import db

from src.services.raw_frame_service import RawFrameService
from src.services.frameProcessingService import freameProcessing

from src.models.sightingModel import Sighting
from src.models.individualModel import Individual
from src.models.rawFrameModel import RawFrame
from src.models.frameModel import Frame

class ImageIdentificationDeamon:
    def __init__(self, app: Flask=None, interval: int=60, rawFrameService: RawFrameService=None):
        self.isRunning = True
        self.interval = interval
        self.app = app
        self.rawFrameService = rawFrameService
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        with self.app.app_context():
            while self.isRunning:
                print(f"Running createSightings at {datetime.now()}")
                self.createSightings()
                time.sleep(self.interval)
                print(f"Finished createSightings at {datetime.now()}")

    def stop(self):
        self.isRunning = False

    def getMugShot(self, imgBytesRawFrame: bytes, sighting: Sighting) -> bytes:
        img = Image.open(io.BytesIO(imgBytesRawFrame))
        img = img.crop(sighting.face_coordinates)
        with io.BytesIO() as output:
            img.save(output, format='JPEG')
            imgBytes = output.getvalue()
        return imgBytes

    def createSightings(self):
        # rawFrame = self.rawFrameService.capture_frame(0)
        rawFrame = self.rawFrameService.captureFrameTest() # funcion para prueba
        sightings: list[Sighting] = freameProcessing(rawFrame).sightings
        # print("Len: ", len(sightings))

        if len(sightings) > 0:
            rawFrameCreate = RawFrame(pixels=rawFrame.pixels)
            db.session.add(rawFrameCreate)
            db.session.commit()
            # print("rawFrameCreate.id", rawFrameCreate.id)

            frameCreate = Frame(raw_frame_id=rawFrameCreate.id)
            db.session.add(frameCreate)
            db.session.commit()
            # print("frameCreate.id", frameCreate.id)
            
            for sighting in sightings: 
                sighting.frame_id = frameCreate.id

                individual = Individual.query.filter_by(collection_id=sighting.collection_id).first()
                if individual:
                    sighting.individual_id = individual.id
                    # print("individual_id existe")
                else:
                    individualCreate = Individual(collection_id=sighting.collection_id, 
                                                  mugshot=self.getMugShot(rawFrame.pixels, sighting))
                    db.session.add(individualCreate)
                    db.session.commit()
                    # print("individualCreate.id", individualCreate.id)

                    sighting.individual_id = individualCreate.id

                sightingCreate = Sighting(frame_id=sighting.frame_id, individual_id=sighting.individual_id, 
                                          collection_id=sighting.collection_id, body_coordinates=sighting.body_coordinates, 
                                          face_coordinates=sighting.face_coordinates, object_coordinates=sighting.object_coordinates)
                db.session.add(sightingCreate)
            db.session.commit()            