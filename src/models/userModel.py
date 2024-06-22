from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from typing import List
from src.models.incidentModel import Incident

class User(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    user:List[Mapped[Incident]]= relationship('Incident', backref='incident')