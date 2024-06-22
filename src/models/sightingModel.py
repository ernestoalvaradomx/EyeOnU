from sqlalchemy.sql import func
from src.util.database.db import db
from sqlalchemy import ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped

class Sighting(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    # This doesn't have to be binary, only a representation of the area in which the face of the individual appears within the frame
    pixel_area:Mapped[LargeBinary] = mapped_column(LargeBinary)
    frame_id:Mapped[int] = mapped_column(ForeignKey("frame.id"))
    individual_id:Mapped[int] = mapped_column(ForeignKey("individual.id"))
    frame:Mapped["Frame"]= relationship('Frame', backref='frame')
    individual:Mapped["Individual"]= relationship('Individual', backref='individual')
    alert:Mapped["Alert"]= relationship('Alert', backref='alert')