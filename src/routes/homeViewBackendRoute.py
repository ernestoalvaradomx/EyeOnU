from flask import Flask, Blueprint, request,  jsonify

from src.models.sightingModel import Sighting
from src.models.incidentModel import Incident
from src.models.alertModel import Alert
from src.models.individualModel import Individual
from src.services.homeViewBackendService import HomeViewBackendService

class HomeViewBackendRoute():
    def __init__(self, app: Flask=None, homeViewBackendService: HomeViewBackendService=None):
        self.app = app
        self.homeViewBackendService = homeViewBackendService
        self.homeViewBackendRoute = Blueprint('homeViewBackendRoute', __name__)
        self.registerRoutes()
    
    def registerRoutes(self):
        # TODO: Borrar
        @self.homeViewBackendRoute.route("/individuals", methods=['GET'])
        def listInvividual() -> list[Individual]:
            result = self.homeViewBackendService.findAllIndividual()
            return jsonify(result), 200
        
        @self.homeViewBackendRoute.route("/alerts", methods=['GET'])
        def listAlert() -> list[Alert]:
            result = self.homeViewBackendService.findAllAlert()
            return jsonify(result), 200
        
        @self.homeViewBackendRoute.route("/sightings", methods=['GET'])
        def listSighting() -> list[Sighting]:
            result = self.homeViewBackendService.findAllSighting()
            return jsonify(result), 200
        
        @self.homeViewBackendRoute.route("/incidents", methods=['GET'])
        def listIncident() -> list[Incident]:
            if request.is_json:
                data = request.get_json()
                result = self.homeViewBackendService.findAllIncidenByIdIndividual(data['idIndividual'])
                return jsonify(result), 200
            else:
                return jsonify({"error": "The request body is not in JSON format"}), 400
            
        @self.homeViewBackendRoute.route("/incident", methods=['POST'])
        def createIncident():
            if request.is_json:
                data = request.get_json()
                self.homeViewBackendService.createIncident(data)
                return jsonify({"response": True}), 200
            else:
                return jsonify({"error": "The request body is not in JSON format"}), 400
    
    def getBlueprint(self):
        return self.homeViewBackendRoute
