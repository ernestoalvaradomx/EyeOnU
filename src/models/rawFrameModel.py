from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, LargeBinary, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class RawFrame(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    pixels:Mapped[LargeBinary] = mapped_column(LargeBinary)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    frame:Mapped["Frame"] = relationship('Frame', backref='raw_rame')

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