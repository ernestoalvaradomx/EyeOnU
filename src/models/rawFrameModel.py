from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, LargeBinary, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from src.models.frameModel import Frame

class RawFrame(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    pixels:Mapped[LargeBinary] = mapped_column(LargeBinary)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    frame:Mapped["Frame"] = relationship(back_populates='raw_frame')

    def __init__(self, pixels):
        self.pixels = pixels

    def toJson(self):
        return {
        'id':self.id,
        'pixels':self.pixels,
        'creationTime':self.creationTime,
    }