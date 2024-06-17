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
    creation_time:Mapped[DateTime] =  Column(DateTime(timezone=True), default=func.now())
    frame: Mapped["Frame"] = relationship(back_populates="raw_frame")



    def __repr__(self):
        return '<id {}>'.format(self.id)

class Frame(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    raw_frame_id: Mapped[int] = mapped_column(ForeignKey("raw_frame.id"))
    raw_frame:Mapped["RawFrame"]= relationship(back_populates="frame")
    # Individuals who have been identified
    sightings:Mapped[List[Sighting]]= relationship(back_populates="frame")

    def __repr__(self):
        return ""

class Sighting(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    # This doesn't have to be binary, only a representation of the area in which the face of the individual appears within the frame
    pixel_area:Mapped[LargeBinary] = Column(LargeBinary)
    frame_id: Mapped[int] = mapped_column(ForeignKey("frame.id"))
    frame:Mapped["Frame"]= relationship(back_populates="sightings")
    individual_id: Mapped[int] = mapped_column(ForeignKey("individual.id"))
    individual:Mapped["Individual"]= relationship(back_populates="sightings")
    alert:Mapped["Alert"]= relationship(back_populates="sighting")

    def __repr__(self):
        return ""

class Individual(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    mugshot:Mapped[LargeBinary] = Column(LargeBinary)
    sightings:Mapped[List[Sighting]]= relationship(back_populates="individual")

    def __repr__(self):
        return ""

class Alert(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    creation_time:Mapped[DateTime] =  Column(DateTime(timezone=True), default=func.now())
    sighting_id: Mapped[int] = mapped_column(ForeignKey("sighting.id"))
    sighting:Mapped["Alert"]= relationship(back_populates="alert")
    incident:Mapped["Incident"]= relationship(back_populates="alert")

    def __repr__(self):
        return ""


class Incident(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    creation_time:Mapped[DateTime] =  Column(DateTime(timezone=True), default=func.now())
    alert_id: Mapped[int] = mapped_column(ForeignKey("alert.id"))
    alert:Mapped["Alert"]= relationship(back_populates="incident")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped["User"]= relationship(back_populates="incident")

    def __repr__(self):
        return ""

class User(Base):
    id:Mapped[int] = Column(Integer, primary_key=True)
    creation_time:Mapped[DateTime] =  Column(DateTime(timezone=True), default=func.now())
    user:List[Mapped[Incident]]= relationship(back_populates="user")

    def __repr__(self):
        return ""