from sqlalchemy.sql import func

from sqlalchemy import Column, Integer, String, ForeignKey, Date,Binary, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from __future__ import annotations
from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship



class Base(DeclarativeBase):
    pass

# XXX: https://flask-appbuilder.readthedocs.io/en/latest/quickhowto.html
class RawFrame(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    pixels:Mapped[LargeBinary] = Column(LargeBinary)
    # XXX: https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    time:Mapped[DateTime] =  Column(DateTime(timezone=True), default=func.now())
    frame: Mapped["Frame"] = relationship(back_populates="raw_frame")



    def __repr__(self):
        return '<id {}>'.format(self.id)

class Frame(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    raw_frame_id: Mapped[int] = mapped_column(ForeignKey("raw_frame.id"))
    raw_frame:Mapped["RawFrame"]= relationship(back_populates="frame")
    sightings:Mapped[List[Sighting]]= relationship(back_populates="frame")

    def __repr__(self):
        return ""

class Sighting(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    pixel_area:Mapped[LargeBinary] = Column(LargeBinary)
    frame_id: Mapped[int] = mapped_column(ForeignKey("frame.id"))
    frame:Mapped["Frame"]= relationship(back_populates="sightings")
    individual_id: Mapped[int] = mapped_column(ForeignKey("individual.id"))
    individual:Mapped["Individual"]= relationship(back_populates="sightings")

    def __repr__(self):
        return ""

class Individual(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    mugshot:Mapped[LargeBinary] = Column(LargeBinary)
    sightings:Mapped[List[Sighting]]= relationship(back_populates="individual")

    def __repr__(self):
        return ""