from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, LargeBinary, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from src.models.frameModel import Frame

class RawFrame(db.Model):
    __tablename__ = 'raw_frame' 
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pixels = db.Column(db.LargeBinary)
    creation_time = db.Column(db.DateTime(timezone=True), default=func.now())
    frame = relationship('Frame', back_populates='raw_frame')

    def __init__(self, pixels):
        self.pixels = pixels

    def to_json(self):
        return {
            'id': self.id,
            'pixels': self.pixels,
            'creation_time': self.creation_time.strftime('%Y-%m-%d %H:%M:%S') if self.creation_time else None,
        }