from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, LargeBinary, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from typing import List

class Individual(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    collection_id:Mapped[String] = mapped_column(String)
    mugshot:Mapped[LargeBinary] = mapped_column(LargeBinary)
    sightings:Mapped[List["Sighting"]]= relationship(back_populates='individual')
