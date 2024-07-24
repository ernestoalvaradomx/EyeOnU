import threading
import time

from flask import Flask
from datetime import datetime
from flask_socketio import SocketIO

from src.util.database.db import db

from src.models.sightingModel import Sighting
from src.models.incidentModel import Incident
from src.models.alertModel import Alert

class ReincidentAlertDeamon:
    def __init__(self, interval: int=60, app: Flask=None, socketio: SocketIO=None):
        self.isRunning = True
        self.interval = interval
        self.app = app
        self.socketio = socketio
        self.thread = threading.Thread(target=self.sendNotification(), daemon=True)
        self.thread.start()

    def run(self):
        with self.app.app_context():
            while self.isRunning:
                print(f"Running createSightings at {datetime.now()}")
                self.sendNotification()
                time.sleep(self.interval)
                print(f"Finished createSightings at {datetime.now()}")

    def stop(self):
        self.isRunning = False

    def sendNotification(self):
        sightingList: list[Sighting] = Sighting.query.filter(is_read=False).all()
        if len(sightingList) > 0:
            for sighting in sightingList:
                incidentList = Incident.query.join(Alert).join(Sighting).filter(individual_id=sighting.individual_id).all()
                if len(incidentList) > 0:
                    alertCreate = Alert(sighting_id=sighting.id) # Crea alerta
                    db.session.add(alertCreate)
                    db.session.commit()

                    self.socketio.emit('notification', {'': '', 'data': ''}, broadcast=True) # Genera un evento

                sighting.is_read = True
                db.session.commit()

            


