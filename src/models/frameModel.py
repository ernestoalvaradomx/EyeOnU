from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from typing import List

class Frame(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    raw_frame_id:Mapped[int] = mapped_column(Integer, ForeignKey("raw_frame.id"))
    
    raw_frame:Mapped["RawFrame"] = relationship(back_populates='frame')
    sightings:Mapped[List["Sighting"]]= relationship(back_populates='frame')
