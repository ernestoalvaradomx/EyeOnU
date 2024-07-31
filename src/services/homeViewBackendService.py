from flask_sqlalchemy import SQLAlchemy

from src.models.alertModel import Alert
from src.models.individualModel import Individual

class HomeViewBackendService():
    def __init__(self, db:SQLAlchemy):
        self.db = db

    def findAllIndividual(self) -> list[Individual]:
       response: list[Individual] = Individual.query.all()
       individualList = [individual.toJson() for individual in response]
       return individualList
    
    def findAllAlert(self) -> list[Alert]:
        response: list[Alert] = Alert.query.filter_by(is_read=False).all() # Trae todas las alertas que no han sido leidas
        alertList = [alert.toJson() for alert in response]
        return alertList

