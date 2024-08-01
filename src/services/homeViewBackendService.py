from flask_sqlalchemy import SQLAlchemy

from src.models.incidentModel import Incident
from src.models.sightingModel import Sighting
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
    
    def findAllIncidenByIdIndividual(self, idIndividual) -> list[Incident]:
        response: list[Incident] = Incident.query.join(Alert).join(Sighting).filter_by(individual_id=idIndividual).all()

        incidentsList = []
        for incident in response:
            incident.alert.sighting.individual = None
            incidentsList.append(incident.toJson())
        return incidentsList
    
    def createIncident(self, data) -> None:
        alert: Alert = Alert.query.get(data["idAlert"])
        alert.is_read = True # La alerta ya fue revisada
        self.db.session.commit()

        newAlert = Incident(alert_id=data["idAlert"], user_id=data["idUser"])
        self.db.session.add(newAlert)
        self.db.session.commit()


