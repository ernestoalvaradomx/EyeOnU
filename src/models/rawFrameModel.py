import base64
from sqlalchemy import Column, Integer, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.util.database.db import db
from sqlalchemy.sql import func

class RawFrame(db.Model):
    __tablename__ = 'raw_frame'

    id = Column(Integer, primary_key=True, nullable=False)
    pixels = Column(LargeBinary)
    creation_time = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, pixels):
        self.pixels = pixels

    def toJson(self):
        return {
            'id': self.id,
            'pixels': base64.b64encode(self.pixels).decode('utf-8'),
            'creation_time': self.creation_time.isoformat(),
        }
