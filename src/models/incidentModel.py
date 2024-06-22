from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from src.models.alertModel import Alert
from src.models.userModel import User

class Incident(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    creation_time:Mapped[DateTime] =  mapped_column(DateTime(timezone=True), default=func.now())
    alert_id: Mapped[int] = mapped_column(ForeignKey("alert.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    alert:Mapped[Alert]= relationship('Alert', backref='alert')
    user:Mapped[User]= relationship('User', backref='user')