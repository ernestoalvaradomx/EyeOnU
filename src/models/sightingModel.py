from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ARRAY, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class Sighting(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    # This doesn't have to be binary, only a representation of the area in which the face of the individual appears within the frame
    frame_id:Mapped[int] = mapped_column(ForeignKey("frame.id"))
    individual_id:Mapped[int] = mapped_column(ForeignKey("individual.id"))
    collection_id:Mapped[String] = mapped_column(String)
    body_coordinates:Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    face_coordinates:Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    object_coordinates:Mapped[ARRAY] = mapped_column(ARRAY(Integer), nullable=True)
    frame:Mapped["Frame"]= relationship(back_populates='sightings')
    individual:Mapped["Individual"]= relationship(back_populates='sightings')
    alert:Mapped["Alert"]= relationship(back_populates='sighting')

    def __init__(self, frame_id, individual_id, collection_id, body_coordinates, face_coordinates, object_coordinates):
        self.frame_id = frame_id
        self.individual_id = individual_id
        self.collection_id = collection_id
        self.body_coordinates = body_coordinates
        self.face_coordinates = face_coordinates
        self.object_coordinates = object_coordinates

    def toJson(self):
        return {
        'id':self.id,
        'frame_id':self.frame_id,
        'individual_id':self.individual_id,
        'collection_id':self.collection_id,
        'body_coordinates':self.body_coordinates,
        'face_coordinates':self.face_coordinates,
        'object_coordinates':self.object_coordinates,
    }
