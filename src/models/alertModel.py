from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from .sightingModel import Sighting
from .incidentModel import Incident

class Alert(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    sighting_id:Mapped[int] = mapped_column(ForeignKey("sighting.id"))
    sighting:Mapped[Sighting] = relationship('Sighting', backref='sighting')
    incident:Mapped[Incident] = relationship('Incident', backref='incident')