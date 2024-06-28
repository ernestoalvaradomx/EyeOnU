from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Integer, LargeBinary
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from typing import List

class Individual(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    mugshot:Mapped[LargeBinary] = mapped_column(LargeBinary)
    sightings:Mapped[List["Sighting"]]= relationship( back_populates='individual')
