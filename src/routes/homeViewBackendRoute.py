from flask import Flask, Blueprint, request,  jsonify

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
        @self.homeViewBackendRoute.route("/individuals", methods=['GET'])
        def listInvividual() -> list[Individual]:
            result = self.homeViewBackendService.findAllIndividual()
            return jsonify(result), 200
        
        @self.homeViewBackendRoute.route("/alerts", methods=['GET'])
        def listAlert() -> list[Alert]:
            result = self.homeViewBackendService.findAllAlert()
            return jsonify(result), 200
    
    def getBlueprint(self):
        return self.homeViewBackendRoute
