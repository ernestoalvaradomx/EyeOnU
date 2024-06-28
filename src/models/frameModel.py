from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from typing import List

class Frame(db.Model):
    __tablename__ = 'frame'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    raw_frame_id = db.Column(db.Integer, db.ForeignKey('raw_frame.id'))
    raw_frame = relationship('RawFrame', back_populates='frame')
    sightings = relationship('Sighting', back_populates='frame')

