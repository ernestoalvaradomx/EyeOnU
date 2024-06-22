from src.util.database.db import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

class User(db.Model):
    id = mapped_column(Integer, primary_key=True, nullable=False)
    name = mapped_column(String(100), nullable=False)
    lastName = mapped_column(String(100), nullable=False)
    age = mapped_column(Integer, nullable=False)

    def __init__(self, name, lastName, age):
        self.name = name
        self.lastName = lastName
        self.age = age

    def toJson(self):
        return {
        'id':self.id,
        'name':self.name,
        'lastName':self.lastName,
        'age':self.age
    }
    