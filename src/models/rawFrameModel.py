from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, String, LargeBinary, DateTime
from sqlalchemy.orm import mapped_column, relationship

class RawFrame(db.Model):
    id = mapped_column(Integer, primary_key=True, nullable=False)
    pixels = mapped_column(LargeBinary)
    creationTime =  mapped_column(DateTime(timezone=True), default=func.now())
    frame = relationship('Frame', backref='rawFrame')

    def __init__(self, pixels, creationTime, frame):
        self.pixels = pixels
        self.creationTime = creationTime
        self.frame = frame

    def toJson(self):
        return {
        'id':self.id,
        'pixels':self.pixels,
        'creationTime':self.creationTime,
        'frame':self.frame
    }