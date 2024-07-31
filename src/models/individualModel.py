import base64

from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, LargeBinary, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from typing import List

class Individual(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    collection_id:Mapped[String] = mapped_column(String)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    mugshot:Mapped[LargeBinary] = mapped_column(LargeBinary)
    
    sightings:Mapped[List["Sighting"]]= relationship(back_populates='individual')

    def toJson(self):
        return {
        "id":self.id,
        "collection_id":self.collection_id,
        "creation_time":self.creation_time.strftime("%H:%M"),
        "mugshot":base64.b64encode(self.mugshot).decode('utf-8') # Regresar en base 64
    }