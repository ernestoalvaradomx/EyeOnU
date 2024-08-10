from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ARRAY, DateTime, ForeignKey, Integer, LargeBinary, String, Boolean
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class Sighting(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    frame_id:Mapped[int] = mapped_column(ForeignKey("frame.id"))
    individual_id:Mapped[int] = mapped_column(ForeignKey("individual.id"))
    collection_id:Mapped[String] = mapped_column(String)
    body_coordinates:Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    face_coordinates:Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    object_coordinates:Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    is_read:Mapped[Boolean] = mapped_column(Boolean)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())

    frame:Mapped["Frame"]= relationship(back_populates='sightings')
    individual:Mapped["Individual"]= relationship(back_populates='sightings')
    alert:Mapped["Alert"]= relationship(back_populates='sighting')

    def __init__(self, frame_id, individual_id, collection_id, body_coordinates, face_coordinates, object_coordinates, is_read):
        self.frame_id = frame_id
        self.individual_id = individual_id
        self.collection_id = collection_id
        self.body_coordinates = body_coordinates
        self.face_coordinates = face_coordinates
        self.object_coordinates = object_coordinates
        self.is_read = is_read

    def toJson(self):
        return {
        "id":self.id,
        "frame_id":self.frame_id,
        "individual_id":self.individual_id,
        "collection_id":self.collection_id,
        "body_coordinates":self.body_coordinates,
        "face_coordinates":self.face_coordinates,
        "object_coordinates":self.object_coordinates,
        "is_read":self.is_read,
        "individual":self.individual.toJson() if self.individual else None,
        "creation_time":self.creation_time.strftime("%Y-%m-%d %H:%M:%S")
    }
