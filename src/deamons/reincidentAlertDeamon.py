import threading
import time

from flask import Flask, jsonify
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
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        with self.app.app_context():
            time.sleep(15) # Inicia en 30s
            while self.isRunning:
                # print(f"Running sendNotification at {datetime.now()}")
                self.sendNotification()
                time.sleep(self.interval)
                # print(f"Finished sendNotification at {datetime.now()}", "\n")

    def stop(self):
        self.isRunning = False

    def sendNotification(self):
        sightingList: list[Sighting] = Sighting.query.filter_by(is_read=False).all()
        if len(sightingList) > 0:
            for sighting in sightingList:
                incidentList: list[Incident] = Incident.query.join(Alert).join(Sighting).filter_by(individual_id=sighting.individual_id).all()
                if len(incidentList) > 0 or sighting.object_coordinates:
                    alertCreate = Alert(sighting_id=sighting.id, is_read=False) # Crea alerta
                    db.session.add(alertCreate)
                    db.session.commit()

                    # alertCreate.sighting = sighting

                    # incidents = []
                    # for incident in incidentList:
                    #     incident.alert.sighting.individual = None
                    #     incidents.append(incident.toJson())

                    # data = {"incidents": incidents, 
                    #         "alert": alertCreate.toJson()}
                    # print("data: ", data)

                    self.socketio.emit('notification', {'data': ''}) # Genera un evento
                    print("SendNotification...")

                sighting.is_read = True
                db.session.commit() 