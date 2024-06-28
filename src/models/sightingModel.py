from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class Sighting(db.Model):
    __tablename__ = 'sighting'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # This doesn't have to be binary, only a representation of the area in which the face of the individual appears within the frame
    pixel_area = db.Column(db.LargeBinary)
    frame_id = db.Column(db.Integer, db.ForeignKey('frame.id'))
    individual_id = db.Column(db.Integer, db.ForeignKey('individual.id'))
    frame = relationship('Frame', back_populates='sightings')
    individual = relationship('Individual', back_populates='sightings')
    alert = relationship('Alert', back_populates='sighting')
    