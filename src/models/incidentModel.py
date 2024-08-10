from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class Incident(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    alert_id: Mapped[int] = mapped_column(ForeignKey("alert.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    description: Mapped[String] = mapped_column(String)
    
    alert:Mapped["Alert"]= relationship(back_populates='incident')
    user:Mapped["User"]= relationship(back_populates='incidents')

    def toJson(self):
        return {
        "id":self.id,
        "creation_time":self.creation_time.strftime("%H:%M"),
        "alert_id":self.alert_id,
        "user_id":self.user_id,
        "description":self.description,
        "alert":self.alert.toJson() if self.alert else None
    }