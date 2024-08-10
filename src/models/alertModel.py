from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class Alert(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    sighting_id:Mapped[int] = mapped_column(ForeignKey("sighting.id"))
    is_read:Mapped[Boolean] = mapped_column(Boolean)
    
    sighting:Mapped["Sighting"] = relationship(back_populates='alert')
    incident:Mapped["Incident"] = relationship(back_populates='alert')

    def toJson(self):
        return {
        "id":self.id,
        "creation_time":self.creation_time.strftime("%H:%M"),
        "sighting_id":self.sighting_id,
        "is_read":self.is_read,
        "sighting":self.sighting.toJson() if self.sighting else None
    }